"""end-to-end 파이프라인.

    수집 → 랭킹 → 저장 → 슬랙 다이제스트 → 카드뉴스 초안 → 슬랙 승인 → Figma

CLI와 Slack 앱과 GitHub Actions가 모두 여기 있는 함수를 호출한다.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from .cardnews import compose, render_cardnews
from .collectors import collect_all
from .config import Settings
from .models import CardNews, Platform, Reference
from .ranking import diversify, rank
from .slack import blocks as B
from .slack import from_settings as slack_from_settings
from .slack.digest import send_digest
from .store import Store

log = logging.getLogger(__name__)


@dataclass
class CollectResult:
    fetched: int
    inserted: int
    by_platform: dict[str, int]
    top: list[Reference]


def run_collect(
    settings: Settings, store: Store, platforms: list[Platform] | None = None
) -> CollectResult:
    """모든 소스에서 수집 → 점수화 → 저장."""
    refs = collect_all(settings, platforms)
    ranked = rank(refs, settings.ranking)
    inserted = store.upsert_many(ranked)

    by_platform: dict[str, int] = {}
    for ref in ranked:
        by_platform[ref.platform.value] = by_platform.get(ref.platform.value, 0) + 1

    log.info("수집 완료: 총 %d건 (신규 %d건)", len(ranked), inserted)
    return CollectResult(
        fetched=len(ranked),
        inserted=inserted,
        by_platform=by_platform,
        top=ranked[:10],
    )


def run_digest(settings: Settings, store: Store, **kwargs) -> dict:
    """상위 레퍼런스를 슬랙으로."""
    return send_digest(settings, store, **kwargs)


def build_cardnews(
    settings: Settings,
    store: Store,
    topic: str,
    card_count: int = 6,
    ref_limit: int = 8,
    since_hours: int | None = None,
    uids: list[str] | None = None,
) -> tuple[CardNews, Path, list[Path]]:
    """카드뉴스 초안 생성 → spec 저장 → 로컬 프리뷰 렌더."""
    if uids:
        refs = [r for r in (store.get(uid) for uid in uids) if r]
    else:
        since = since_hours if since_hours is not None else settings.collect.lookback_hours
        candidates = store.top(limit=ref_limit * 3, since_hours=since)
        refs = diversify(candidates, limit=ref_limit, per_platform_cap=max(2, ref_limit // 2))

    if not refs:
        log.warning("레퍼런스가 없습니다 — 주제만으로 카드뉴스를 만듭니다.")

    news = compose(topic, refs, card_count=card_count)

    spec_path = settings.out_dir / "cardnews" / f"{news.slug}.json"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_json = json.dumps(news.to_spec(), ensure_ascii=False, indent=2)
    spec_path.write_text(spec_json, encoding="utf-8")
    store.save_cardnews(news.slug, news.topic, spec_json)

    previews: list[Path] = []
    try:
        previews = render_cardnews(news, settings.out_dir / "preview")
    except ImportError:
        log.warning("Pillow가 없어 프리뷰를 건너뜁니다 (pip install pillow).")
    except Exception as exc:
        log.warning("프리뷰 렌더 실패: %s", exc)

    log.info("카드뉴스 초안 생성: %s (%d장)", news.slug, len(news.cards))
    return news, spec_path, previews


def publish_cardnews_draft(
    settings: Settings,
    news: CardNews,
    previews: list[Path],
    channel: str = "",
    figma_url: str = "",
) -> dict:
    """초안을 슬랙에 올려 승인을 받는다. 프리뷰 이미지도 함께 업로드."""
    client = slack_from_settings(settings)
    target = channel or settings.slack.default_channel or settings.slack.digest_channel
    if client.mode == "bot" and target.startswith("#"):
        target = client.resolve_channel_id(target)

    result = client.post_message(
        text=f"카드뉴스 초안 · {news.topic}",
        blocks=B.cardnews_blocks(news, figma_url=figma_url),
        channel=target,
    )

    if client.mode == "bot":
        for path in previews[:10]:
            try:
                client.upload_file(path, channel=target, title=path.name)
            except Exception as exc:
                log.warning("프리뷰 업로드 실패 (%s): %s", path.name, exc)

    return {"mode": client.mode, "result": result}


def export_from_figma(
    settings: Settings, node_ids: list[str], slug: str
) -> list[Path]:
    """Figma 플러그인이 만든 프레임을 PNG로 내려받는다."""
    from .figma import from_settings as figma_from_settings

    client = figma_from_settings(settings)
    out_dir = settings.out_dir / "figma" / slug
    return client.download_images(
        node_ids,
        out_dir=out_dir,
        fmt=settings.figma.export_format,
        scale=settings.figma.export_scale,
    )


def run_daily(settings: Settings, store: Store) -> dict:
    """GitHub Actions가 하루 한 번 돌리는 기본 루틴."""
    collected = run_collect(settings, store)
    digest = run_digest(settings, store)
    return {
        "fetched": collected.fetched,
        "inserted": collected.inserted,
        "by_platform": collected.by_platform,
        "digest": digest,
    }
