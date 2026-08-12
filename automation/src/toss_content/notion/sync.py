"""콘텐츠 목록 DB 자동 채우기.

동작: 사용자가 DB에 **주제만 적은 행**을 만들면, 이 모듈이 그 행을 찾아
레퍼런스를 붙이고 카드뉴스 카피를 써서 속성과 본문을 채운다.

    [사람]  주제 한 줄 입력
              ↓
    [자동]  레퍼런스 수집 → 카피 생성 → 속성 기입 + 본문 작성 → 상태 '완료'

**어떤 행을 처리할지**는 상태(status) 칼럼으로 판단한다.
- 상태가 비어 있거나 `trigger_status` 중 하나  → 처리 대상
- 상태가 `done_status`                        → 건너뜀

상태 칼럼이 아예 없는 DB라면, 본문에 자동 생성 표식(`blocks.MARKER`)이 있는지
확인해서 중복 처리를 막는다.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..config import Settings
from ..models import CardNews, Reference
from ..store import Store
from . import blocks as B
from . import schema as S
from .client import NotionClient

log = logging.getLogger(__name__)


@dataclass
class RowResult:
    page_id: str
    topic: str
    status: str  # filled | skipped | failed
    slug: str = ""
    reference_count: int = 0
    skipped_fields: list[str] = field(default_factory=list)
    error: str = ""


def _is_pending(status_value: Any, settings: Settings) -> bool:
    """처리 대상인지 판단."""
    if status_value is None or str(status_value).strip() == "":
        return True  # 상태를 비워두는 게 가장 흔한 '아직 안 함' 표현이다
    value = str(status_value).strip().lower()
    if value in {s.strip().lower() for s in settings.notion.done_status}:
        return False
    return value in {s.strip().lower() for s in settings.notion.trigger_status}


def pending_rows(client: NotionClient, settings: Settings) -> list[dict[str, Any]]:
    """채워야 할 행 목록. (필터를 서버가 아닌 여기서 거는 이유는 아래 주석 참조)"""
    database_id = settings.notion.database_id
    schema = client.get_schema(database_id)
    overrides = settings.notion.properties

    # Notion 필터는 속성 타입별로 문법이 달라(select/status/rich_text …), 상대 DB
    # 스키마를 모르는 상태에서 서버 필터를 만들면 400 위험이 크다. 행 수가 수십~수백
    # 수준인 콘텐츠 목록에서는 받아와서 걸러내는 편이 안전하고 충분히 빠르다.
    rows: list[dict[str, Any]] = []
    for page in client.query(database_id, page_size=100):
        values = S.read_page(page)
        topic = S.get_field(values, "topic", schema, overrides)
        if not topic or not str(topic).strip():
            continue  # 제목 없는 빈 행은 대상 아님

        status = S.get_field(values, "status", schema, overrides)
        if not _is_pending(status, settings):
            continue

        rows.append(
            {
                "page_id": page["id"],
                "topic": str(topic).strip(),
                "status": status,
                "values": values,
                "url": page.get("url", ""),
            }
        )
    return rows


def _already_filled(client: NotionClient, page_id: str) -> bool:
    """본문에 자동 생성 표식이 있는지 — 상태 칼럼이 없는 DB용 중복 방지."""
    try:
        for block in client.get_blocks(page_id):
            if block.get("type") != "callout":
                continue
            text = "".join(
                item.get("plain_text", "")
                for item in (block.get("callout") or {}).get("rich_text") or []
            )
            if B.MARKER in text:
                return True
    except Exception as exc:
        log.warning("본문 확인 실패(계속 진행): %s", exc)
    return False


def fill_row(
    client: NotionClient,
    settings: Settings,
    store: Store,
    row: dict[str, Any],
    schema: dict[str, str] | None = None,
    dry_run: bool = False,
) -> RowResult:
    """행 하나를 채운다."""
    from .. import pipeline

    page_id = row["page_id"]
    topic = row["topic"]
    schema = schema if schema is not None else client.get_schema(settings.notion.database_id)
    overrides = settings.notion.properties
    has_status = S.resolve_property("status", schema, overrides) is not None

    # 상태 칼럼이 없으면 본문 표식으로 중복을 막는다.
    if not has_status and _already_filled(client, page_id):
        return RowResult(page_id, topic, "skipped", error="이미 채워진 행")

    try:
        news, spec_path, _ = pipeline.build_cardnews(
            settings,
            store,
            topic=topic,
            card_count=settings.notion.card_count,
        )
        refs = _referenced(store, news)

        if dry_run:
            log.info("[dry-run] %s → %d장, 레퍼런스 %d건", topic, len(news.cards), len(refs))
            return RowResult(page_id, topic, "filled", news.slug, len(refs))

        properties, skipped = _build_row_properties(news, refs, spec_path, schema, overrides, settings)
        if properties:
            client.update_page(page_id, properties)

        body = B.cardnews_blocks(news, spec_path=str(spec_path))
        body += B.reference_blocks(refs)
        client.append_blocks(page_id, body)

        log.info("Notion 행 채움: %s (%s, %d장)", topic, news.slug, len(news.cards))
        return RowResult(page_id, topic, "filled", news.slug, len(refs), skipped)

    except Exception as exc:
        log.exception("행 처리 실패: %s", topic)
        _mark_failed(client, settings, page_id, schema, exc)
        return RowResult(page_id, topic, "failed", error=str(exc))


def _referenced(store: Store, news: CardNews) -> list[Reference]:
    """카드에 기록된 source_uids로 실제 레퍼런스를 복원."""
    uids: list[str] = []
    for card in news.cards:
        for uid in card.source_uids:
            if uid not in uids:
                uids.append(uid)
    return [r for r in (store.get(uid) for uid in uids) if r]


def _build_row_properties(
    news: CardNews,
    refs: list[Reference],
    spec_path,
    schema: dict[str, str],
    overrides: dict[str, str],
    settings: Settings,
) -> tuple[dict[str, Any], list[str]]:
    cover = news.cards[0] if news.cards else None
    platforms = sorted({r.platform.value for r in refs})

    fields: dict[str, Any] = {
        "status": settings.notion.done_status[0] if settings.notion.done_status else "완료",
        "summary": cover.title if cover else news.topic,
        "copy": "\n\n".join(
            f"{c.index:02d}. {c.title}\n{c.body}".strip() for c in news.cards
        ),
        "references": "\n".join(f"[{r.platform.value}] {r.author} {r.url}" for r in refs),
        "slug": news.slug,
        "card_count": len(news.cards),
        "updated_at": datetime.now(timezone.utc),
        "platform": platforms or None,
        "spec_url": str(spec_path),
    }
    if settings.figma.file_key:
        fields["figma_url"] = f"https://www.figma.com/design/{settings.figma.file_key}/"

    # 값이 빈 필드는 아예 보내지 않는다 (빈 select를 보내면 400이 난다).
    fields = {k: v for k, v in fields.items() if v not in (None, "", [])}
    return S.build_properties(fields, schema, overrides)


def _mark_failed(
    client: NotionClient, settings: Settings, page_id: str, schema: dict[str, str], exc: Exception
) -> None:
    """실패도 DB에 남긴다 — 조용히 사라지면 사람이 눈치채지 못한다."""
    try:
        properties, _ = S.build_properties(
            {"status": settings.notion.failed_status}, schema, settings.notion.properties
        )
        if properties:
            client.update_page(page_id, properties)
        client.append_blocks(
            page_id,
            [B.callout(f"{B.MARKER} 실패 · {type(exc).__name__}: {exc}"[:1900], emoji="⚠️")],
        )
    except Exception as inner:
        log.warning("실패 표시도 실패했습니다: %s", inner)


def run_fill(
    client: NotionClient,
    settings: Settings,
    store: Store,
    limit: int = 5,
    dry_run: bool = False,
) -> list[RowResult]:
    """대기 중인 행을 최대 `limit`개 처리."""
    schema = client.get_schema(settings.notion.database_id)
    rows = pending_rows(client, settings)
    if not rows:
        log.info("채울 행이 없습니다.")
        return []

    log.info("대기 행 %d개 중 %d개 처리합니다.", len(rows), min(len(rows), limit))
    return [
        fill_row(client, settings, store, row, schema=schema, dry_run=dry_run)
        for row in rows[:limit]
    ]


def push_references(
    client: NotionClient,
    settings: Settings,
    refs: list[Reference],
    database_id: str = "",
) -> int:
    """수집한 레퍼런스를 DB에 행으로 적재 (별도 레퍼런스 DB를 쓸 때)."""
    target = database_id or settings.notion.reference_database_id
    if not target:
        log.info("reference_database_id가 없어 레퍼런스 적재를 건너뜁니다.")
        return 0

    schema = client.get_schema(target)
    overrides = settings.notion.properties
    created = 0

    for ref in refs:
        fields = {
            "topic": ref.summary(100) or ref.url,
            "platform": ref.platform.value,
            "summary": ref.summary(500),
            "references": ref.url,
            "updated_at": ref.created_at,
        }
        properties, _ = S.build_properties(fields, schema, overrides)
        if not properties:
            continue
        try:
            client.create_page(target, properties)
            created += 1
        except Exception as exc:
            log.warning("레퍼런스 적재 실패 (%s): %s", ref.uid, exc)
    return created
