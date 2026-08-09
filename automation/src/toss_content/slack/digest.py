"""일일 레퍼런스 다이제스트 전송."""

from __future__ import annotations

import logging

from ..config import Settings
from ..models import Reference
from ..ranking import diversify
from ..store import Store
from . import blocks as B
from .client import SlackClient, from_settings

log = logging.getLogger(__name__)


def pick_digest_refs(
    store: Store, settings: Settings, limit: int | None = None, since_hours: int | None = None
) -> list[Reference]:
    """아직 안 보낸 것 중 상위 N건. 플랫폼 편중을 막기 위해 다변화한다."""
    limit = limit or settings.slack.digest_limit
    since = since_hours if since_hours is not None else settings.collect.lookback_hours
    # 다변화 필터가 걸러낼 여유분까지 넉넉히 뽑는다.
    candidates = store.top(limit=limit * 4, since_hours=since, only_unnotified=True)
    per_platform_cap = max(2, (limit // 2) or 1)
    return diversify(candidates, limit=limit, per_platform_cap=per_platform_cap)


def send_digest(
    settings: Settings,
    store: Store,
    client: SlackClient | None = None,
    limit: int | None = None,
    since_hours: int | None = None,
    channel: str = "",
    mark: bool = True,
) -> dict:
    client = client or from_settings(settings)
    refs = pick_digest_refs(store, settings, limit=limit, since_hours=since_hours)

    target = channel or settings.slack.digest_channel or settings.slack.default_channel
    if client.mode == "bot" and target.startswith("#"):
        target = client.resolve_channel_id(target)

    counts = store.counts_by_platform()
    note = " · ".join(f"{k} {v}건 누적" for k, v in sorted(counts.items())) or "누적 데이터 없음"
    if settings.slack.mention_on_digest:
        note = f"{settings.slack.mention_on_digest} {note}"

    payload = B.digest_blocks(refs, note=note)
    text = f"오늘의 콘텐츠 레퍼런스 {len(refs)}건"
    result = client.post_message(text=text, blocks=payload, channel=target)

    if mark and refs and client.mode != "dry-run":
        store.mark_notified([r.uid for r in refs])
    log.info("다이제스트 전송 완료 (%s 모드, %d건)", client.mode, len(refs))
    return {"sent": len(refs), "mode": client.mode, "result": result}
