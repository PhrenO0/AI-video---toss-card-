"""레퍼런스 랭킹.

목적은 "많이 좋아요 받은 글"이 아니라 **지금 참고할 가치가 큰 글**을 위로 올리는 것.
그래서 절대 참여수보다 *속도*(시간당 참여)와 *신선도*에 가중치를 더 준다.

플랫폼별 지표 가용성이 크게 달라서 그대로 비교하면 안 된다.
- X: 좋아요/RT/노출까지 다 나옴
- Instagram: 좋아요/댓글 나옴, 노출은 없음
- Threads: 공개 검색 결과에 지표가 아예 없음 (0으로 들어옴)

지표가 전무한 항목을 그냥 두면 항상 바닥에 깔리므로, 해당 플랫폼에는
중립 프록시 값을 넣어 "지표 없음"이 곧 "가치 없음"이 되지 않게 한다.
"""

from __future__ import annotations

import math
from datetime import datetime, timezone

from .config import RankingConfig
from .models import MediaType, Platform, Reference

#: 지표를 제공하지 않는 플랫폼에 적용할 중립 참여수 프록시.
#: 이 값은 "평균쯤은 된다고 가정한다"는 뜻이지, 실제 인기도가 아니다.
NO_METRIC_PROXY = 30

_RICH_MEDIA = {MediaType.IMAGE, MediaType.CAROUSEL, MediaType.VIDEO}


def _age_hours(ref: Reference, now: datetime) -> float:
    created = ref.created_at
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)
    return max((now - created).total_seconds() / 3600.0, 0.5)


def _keyword_hits(ref: Reference, boost_keywords: list[str]) -> int:
    if not boost_keywords:
        return 0
    lowered = ref.text.lower()
    return sum(1 for kw in boost_keywords if kw.lower() in lowered)


def score_reference(
    ref: Reference, cfg: RankingConfig, now: datetime | None = None
) -> float:
    now = now or datetime.now(timezone.utc)
    age = _age_hours(ref, now)

    engagement = ref.engagement
    if engagement == 0 and ref.platform is Platform.THREADS:
        engagement = NO_METRIC_PROXY

    # 로그 스케일: 10만 좋아요가 1만 좋아요보다 10배 좋은 레퍼런스는 아니다.
    volume = math.log1p(engagement)
    velocity = math.log1p(engagement / age)

    score = cfg.weight_engagement * volume + cfg.weight_velocity * velocity
    score += cfg.weight_keyword * _keyword_hits(ref, cfg.boost_keywords)
    if ref.media_type in _RICH_MEDIA:
        # 카드뉴스 레퍼런스라 이미지/영상이 붙은 쪽이 실사용 가치가 높다.
        score += cfg.weight_media

    decay = 0.5 ** (age / max(cfg.half_life_hours, 1.0))
    return round(score * decay, 4)


def rank(
    refs: list[Reference], cfg: RankingConfig, now: datetime | None = None
) -> list[Reference]:
    """점수를 매겨 정렬한 새 리스트를 반환한다(원본 객체의 score는 갱신됨)."""
    now = now or datetime.now(timezone.utc)
    for ref in refs:
        ref.score = score_reference(ref, cfg, now)
    return sorted(refs, key=lambda r: (r.score, r.created_at), reverse=True)


def diversify(refs: list[Reference], limit: int, per_platform_cap: int = 0) -> list[Reference]:
    """상위 목록이 한 플랫폼/한 계정으로 도배되지 않게 다듬는다.

    같은 작성자는 최대 2건까지만, 플랫폼별 상한은 `per_platform_cap`(0이면 무제한).
    """
    per_platform: dict[Platform, int] = {}
    per_author: dict[str, int] = {}
    picked: list[Reference] = []

    for ref in refs:
        if len(picked) >= limit:
            break
        if per_platform_cap and per_platform.get(ref.platform, 0) >= per_platform_cap:
            continue
        if per_author.get(ref.author, 0) >= 2:
            continue
        picked.append(ref)
        per_platform[ref.platform] = per_platform.get(ref.platform, 0) + 1
        per_author[ref.author] = per_author.get(ref.author, 0) + 1

    # 상한 때문에 정원을 못 채웠으면 남은 자리는 점수순으로 그냥 채운다.
    if len(picked) < limit:
        chosen = {r.uid for r in picked}
        picked.extend([r for r in refs if r.uid not in chosen][: limit - len(picked)])
    return picked
