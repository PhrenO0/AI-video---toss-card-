"""수집기 공통 뼈대.

한 플랫폼당 여러 개의 **프로바이더**를 둔다. 예를 들어 X는
`official`(X API v2) → `apify` → `rss` 순으로 시도하고,
토큰이 없거나 실패하면 조용히 다음 프로바이더로 넘어간다.
공식 API 정책이 자주 바뀌는 영역이라 이 구조가 가장 오래 버틴다.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Callable, Sequence

from ..config import CollectConfig, SourceRule
from ..models import Platform, Reference

log = logging.getLogger(__name__)

#: 프로바이더 시그니처: (규칙, 수집설정) -> 정규화된 레퍼런스 목록
Provider = Callable[[SourceRule, CollectConfig], list[Reference]]


class ProviderUnavailable(RuntimeError):
    """토큰/설정이 없어 이 프로바이더를 쓸 수 없음. 조용히 다음으로 넘어간다."""


class Collector(ABC):
    platform: Platform
    #: 설정에 우선순위가 없을 때 사용할 기본 순서
    default_provider_order: Sequence[str] = ()

    @property
    @abstractmethod
    def providers(self) -> dict[str, Provider]:
        ...

    def provider_order(self, cfg: CollectConfig) -> list[str]:
        configured = cfg.providers.get(self.platform.value) or []
        order = [p for p in configured if p in self.providers]
        for name in self.default_provider_order:
            if name not in order and name in self.providers:
                order.append(name)
        return order

    def collect(self, rules: Sequence[SourceRule], cfg: CollectConfig) -> list[Reference]:
        """규칙별로 프로바이더를 순서대로 시도하고, 첫 성공 결과를 채택한다."""
        results: dict[str, Reference] = {}
        order = self.provider_order(cfg)
        if not order:
            log.warning("[%s] 사용 가능한 프로바이더가 없습니다.", self.platform.value)
            return []

        for rule in rules:
            for name in order:
                try:
                    found = self.providers[name](rule, cfg)
                except ProviderUnavailable as exc:
                    log.info("[%s/%s] 건너뜀: %s", self.platform.value, name, exc)
                    continue
                except Exception as exc:  # 프로바이더 하나가 죽어도 파이프라인은 계속
                    log.warning(
                        "[%s/%s] '%s' 수집 실패: %s",
                        self.platform.value, name, rule.value, exc,
                    )
                    continue

                for ref in found:
                    ref.provider = name
                    ref.query = rule.label or rule.value
                    results.setdefault(ref.uid, ref)
                log.info(
                    "[%s/%s] '%s' → %d건", self.platform.value, name, rule.value, len(found)
                )
                if found:
                    break  # 이 규칙은 해결됨. 다음 규칙으로.

        return list(results.values())


def passes_filters(ref: Reference, cfg: CollectConfig) -> bool:
    if ref.engagement < cfg.min_engagement:
        return False
    lowered = ref.text.lower()
    return not any(bad.lower() in lowered for bad in cfg.exclude_keywords)
