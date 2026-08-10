"""수집·가공 전 과정에서 공유하는 데이터 모델.

플랫폼(X / Instagram / Threads)마다 응답 스키마가 전부 다르기 때문에,
수집기는 각자 raw 응답을 받아 이 `Reference` 하나로 정규화해서 내보낸다.
이후 랭킹·저장·슬랙·카드뉴스 단계는 플랫폼을 몰라도 동작한다.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Platform(str, Enum):
    X = "x"
    INSTAGRAM = "instagram"
    THREADS = "threads"


class MediaType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    CAROUSEL = "carousel"
    VIDEO = "video"


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Reference:
    """플랫폼 무관 정규화 게시물 1건."""

    platform: Platform
    post_id: str
    url: str
    author: str
    text: str
    created_at: datetime

    like_count: int = 0
    comment_count: int = 0
    share_count: int = 0
    view_count: int = 0

    media_type: MediaType = MediaType.TEXT
    media_urls: list[str] = field(default_factory=list)

    #: 이 게시물을 잡아낸 검색어/계정 (어떤 규칙이 먹혔는지 추적용)
    query: str = ""
    #: 수집에 실제로 사용한 프로바이더 이름 (official / apify / rss ...)
    provider: str = ""
    author_follower_count: int = 0

    collected_at: datetime = field(default_factory=utcnow)
    score: float = 0.0
    raw: dict[str, Any] = field(default_factory=dict)

    @property
    def uid(self) -> str:
        """플랫폼 간 충돌 없는 전역 고유 키."""
        return f"{self.platform.value}:{self.post_id}"

    @property
    def engagement(self) -> int:
        return self.like_count + self.comment_count + self.share_count

    def summary(self, limit: int = 160) -> str:
        one_line = " ".join(self.text.split())
        if len(one_line) <= limit:
            return one_line
        return one_line[: limit - 1] + "…"

    def to_row(self) -> dict[str, Any]:
        """SQLite 저장용 평탄화."""
        return {
            "uid": self.uid,
            "platform": self.platform.value,
            "post_id": self.post_id,
            "url": self.url,
            "author": self.author,
            "text": self.text,
            "created_at": self.created_at.astimezone(timezone.utc).isoformat(),
            "like_count": self.like_count,
            "comment_count": self.comment_count,
            "share_count": self.share_count,
            "view_count": self.view_count,
            "media_type": self.media_type.value,
            "media_urls": json.dumps(self.media_urls, ensure_ascii=False),
            "query": self.query,
            "provider": self.provider,
            "author_follower_count": self.author_follower_count,
            "collected_at": self.collected_at.astimezone(timezone.utc).isoformat(),
            "score": self.score,
            "raw": json.dumps(self.raw, ensure_ascii=False, default=str),
        }

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "Reference":
        return cls(
            platform=Platform(row["platform"]),
            post_id=row["post_id"],
            url=row["url"],
            author=row["author"],
            text=row["text"],
            created_at=datetime.fromisoformat(row["created_at"]),
            like_count=row["like_count"],
            comment_count=row["comment_count"],
            share_count=row["share_count"],
            view_count=row["view_count"],
            media_type=MediaType(row["media_type"]),
            media_urls=json.loads(row["media_urls"] or "[]"),
            query=row["query"] or "",
            provider=row["provider"] or "",
            author_follower_count=row["author_follower_count"] or 0,
            collected_at=datetime.fromisoformat(row["collected_at"]),
            score=row["score"] or 0.0,
            raw=json.loads(row["raw"] or "{}"),
        )


@dataclass
class Card:
    """카드뉴스 한 장."""

    index: int
    kind: str = "body"  # cover | body | outro
    title: str = ""
    body: str = ""
    badge: str = ""
    image_url: str = ""
    #: 이 카드 근거가 된 레퍼런스 uid 목록
    source_uids: list[str] = field(default_factory=list)


@dataclass
class CardNews:
    """카드뉴스 1세트 = Figma 플러그인이 그대로 먹는 spec."""

    slug: str
    topic: str
    cards: list[Card] = field(default_factory=list)
    template: str = "toss_default"
    created_at: datetime = field(default_factory=utcnow)

    def to_spec(self) -> dict[str, Any]:
        """`figma-plugin/`이 소비하는 JSON 스펙."""
        return {
            "version": 1,
            "slug": self.slug,
            "topic": self.topic,
            "template": self.template,
            "createdAt": self.created_at.astimezone(timezone.utc).isoformat(),
            "cards": [asdict(c) for c in self.cards],
        }

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> "CardNews":
        return cls(
            slug=spec["slug"],
            topic=spec.get("topic", ""),
            template=spec.get("template", "toss_default"),
            created_at=datetime.fromisoformat(spec["createdAt"])
            if spec.get("createdAt")
            else utcnow(),
            cards=[Card(**c) for c in spec.get("cards", [])],
        )
