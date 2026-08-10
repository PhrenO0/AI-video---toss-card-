"""플랫폼별 수집기 레지스트리."""

from __future__ import annotations

import logging

from ..config import Settings
from ..models import Platform, Reference
from .base import Collector
from .instagram import InstagramCollector
from .threads import ThreadsCollector
from .x import XCollector

log = logging.getLogger(__name__)

COLLECTORS: dict[Platform, Collector] = {
    Platform.X: XCollector(),
    Platform.INSTAGRAM: InstagramCollector(),
    Platform.THREADS: ThreadsCollector(),
}


def collect_all(
    settings: Settings, platforms: list[Platform] | None = None
) -> list[Reference]:
    """설정된 모든 규칙을 돌면서 레퍼런스를 모은다."""
    targets = platforms or list(COLLECTORS)
    collected: list[Reference] = []
    for platform in targets:
        collector = COLLECTORS[platform]
        rules = settings.queries_for(platform.value)
        if not rules:
            log.info("[%s] 해당 플랫폼 규칙 없음 — 건너뜀", platform.value)
            continue
        found = collector.collect(rules, settings.collect)
        log.info("[%s] 총 %d건 수집", platform.value, len(found))
        collected.extend(found)
    return collected


__all__ = ["COLLECTORS", "collect_all", "Collector"]
