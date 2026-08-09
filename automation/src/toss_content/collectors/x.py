"""X(구 트위터) 레퍼런스 수집.

2026년 기준 X는 신규 개발자용 무료 검색 티어가 없다. 기본은 종량제(pay-per-use)이고
전문 검색(full-archive)은 사실상 엔터프라이즈 전용이다. 따라서 프로바이더를 3개 둔다.

- ``official``  : X API v2 `recent search` / `user timeline` (유료 토큰 필요, 가장 정확)
- ``apify``     : Apify 액터 (토큰 하나로 검색·계정 둘 다, 종량제 대안)
- ``rss``       : RSSHub/Nitter 계열 인스턴스 (무료, 계정 타임라인만, 지표 없음)

참고: https://docs.x.com/x-api/posts/recent-search
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from xml.etree import ElementTree

import requests

from ..config import CollectConfig, SourceRule
from ..http import get_json, post_json
from ..models import MediaType, Platform, Reference
from .base import Collector, Provider, ProviderUnavailable, passes_filters

X_API = "https://api.x.com/2"
APIFY_API = "https://api.apify.com/v2"


def _iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _build_search_query(rule: SourceRule, cfg: CollectConfig) -> str:
    """SourceRule을 X 검색 문법으로 변환."""
    if rule.kind == "account":
        base = f"from:{rule.value.lstrip('@')}"
    elif rule.kind == "hashtag":
        base = f"#{rule.value.lstrip('#')}"
    else:
        base = rule.value
    parts = [f"({base})", "-is:retweet"]
    if cfg.languages and len(cfg.languages) == 1:
        parts.append(f"lang:{cfg.languages[0]}")
    return " ".join(parts)


class XCollector(Collector):
    platform = Platform.X
    default_provider_order = ("official", "apify", "rss")

    @property
    def providers(self) -> dict[str, Provider]:
        return {
            "official": self._official,
            "apify": self._apify,
            "rss": self._rss,
        }

    # ------------------------------------------------------------- official
    def _official(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        token = os.environ.get("X_BEARER_TOKEN", "").strip()
        if not token:
            raise ProviderUnavailable("X_BEARER_TOKEN 미설정")

        start = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)
        payload = get_json(
            f"{X_API}/tweets/search/recent",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "query": _build_search_query(rule, cfg),
                # X API는 10~100만 허용한다.
                "max_results": max(10, min(cfg.per_query_limit, 100)),
                "start_time": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "tweet.fields": "created_at,public_metrics,lang,attachments,entities",
                "expansions": "author_id,attachments.media_keys",
                "user.fields": "username,name,public_metrics",
                "media.fields": "type,url,preview_image_url",
            },
        ) or {}

        includes = payload.get("includes", {})
        users = {u["id"]: u for u in includes.get("users", [])}
        media = {m["media_key"]: m for m in includes.get("media", [])}

        refs: list[Reference] = []
        for post in payload.get("data", []) or []:
            metrics = post.get("public_metrics", {})
            user = users.get(post.get("author_id"), {})
            username = user.get("username", "unknown")
            keys = (post.get("attachments") or {}).get("media_keys", []) or []
            media_items = [media[k] for k in keys if k in media]

            ref = Reference(
                platform=Platform.X,
                post_id=post["id"],
                url=f"https://x.com/{username}/status/{post['id']}",
                author=f"@{username}",
                text=post.get("text", ""),
                created_at=_iso(post["created_at"]),
                like_count=metrics.get("like_count", 0),
                comment_count=metrics.get("reply_count", 0),
                share_count=metrics.get("retweet_count", 0)
                + metrics.get("quote_count", 0),
                view_count=metrics.get("impression_count", 0),
                media_type=_media_type_from_x(media_items),
                media_urls=[
                    m.get("url") or m.get("preview_image_url", "") for m in media_items
                ],
                author_follower_count=(user.get("public_metrics") or {}).get(
                    "followers_count", 0
                ),
                raw=post,
            )
            if passes_filters(ref, cfg):
                refs.append(ref)
        return refs

    # ---------------------------------------------------------------- apify
    def _apify(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        token = os.environ.get("APIFY_TOKEN", "").strip()
        if not token:
            raise ProviderUnavailable("APIFY_TOKEN 미설정")
        actor = os.environ.get("APIFY_X_ACTOR", "apidojo~tweet-scraper").strip()

        body: dict[str, Any] = {
            "maxItems": cfg.per_query_limit,
            "sort": "Top",
            "tweetLanguage": cfg.languages[0] if len(cfg.languages) == 1 else None,
            "start": (
                datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)
            ).strftime("%Y-%m-%d"),
        }
        if rule.kind == "account":
            body["twitterHandles"] = [rule.value.lstrip("@")]
        else:
            body["searchTerms"] = [_build_search_query(rule, cfg)]
        body = {k: v for k, v in body.items() if v is not None}

        items = post_json(
            f"{APIFY_API}/acts/{actor}/run-sync-get-dataset-items",
            params={"token": token},
            json_body=body,
            timeout=180,
        ) or []
        return [r for r in (_ref_from_apify_x(i) for i in items) if r and passes_filters(r, cfg)]

    # ------------------------------------------------------------------ rss
    def _rss(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        """RSSHub/Nitter 계열 인스턴스. 무료지만 계정 타임라인만 되고 지표가 없다."""
        base = os.environ.get("X_RSS_BASE", "").strip().rstrip("/")
        if not base:
            raise ProviderUnavailable("X_RSS_BASE 미설정 (예: https://rsshub.app)")
        if rule.kind != "account":
            raise ProviderUnavailable("RSS 프로바이더는 account 규칙만 지원")

        handle = rule.value.lstrip("@")
        resp = requests.get(f"{base}/twitter/user/{handle}", timeout=30)
        resp.raise_for_status()
        cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)

        refs: list[Reference] = []
        for item in ElementTree.fromstring(resp.content).iter("item"):
            link = (item.findtext("link") or "").strip()
            post_id = link.rstrip("/").rsplit("/", 1)[-1]
            if not post_id:
                continue
            pub = item.findtext("pubDate")
            created = parsedate_to_datetime(pub) if pub else datetime.now(timezone.utc)
            if created.tzinfo is None:
                created = created.replace(tzinfo=timezone.utc)
            if created < cutoff:
                continue
            description = item.findtext("description") or ""
            refs.append(
                Reference(
                    platform=Platform.X,
                    post_id=post_id,
                    url=link,
                    author=f"@{handle}",
                    text=re.sub(r"<[^>]+>", " ", description).strip(),
                    created_at=created,
                    media_urls=re.findall(r'<img[^>]+src="([^"]+)"', description),
                    media_type=MediaType.IMAGE
                    if "<img" in description
                    else MediaType.TEXT,
                )
            )
            if len(refs) >= cfg.per_query_limit:
                break
        # RSS는 지표가 없어 min_engagement 필터를 적용하면 전부 탈락한다.
        return refs


def _media_type_from_x(media_items: list[dict]) -> MediaType:
    if not media_items:
        return MediaType.TEXT
    if any(m.get("type") in {"video", "animated_gif"} for m in media_items):
        return MediaType.VIDEO
    return MediaType.CAROUSEL if len(media_items) > 1 else MediaType.IMAGE


def _ref_from_apify_x(item: dict) -> Reference | None:
    """Apify 액터마다 필드명이 조금씩 달라 관용적으로 파싱한다."""
    post_id = str(item.get("id") or item.get("id_str") or item.get("tweetId") or "")
    if not post_id:
        return None
    author = item.get("author") or item.get("user") or {}
    username = author.get("userName") or author.get("username") or author.get("screen_name") or "unknown"
    created_raw = item.get("createdAt") or item.get("created_at") or ""
    try:
        created = _iso(created_raw) if "T" in created_raw else parsedate_to_datetime(created_raw)
    except (ValueError, TypeError):
        created = datetime.now(timezone.utc)
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)

    media_urls = [
        m.get("media_url_https") or m.get("url", "")
        for m in (item.get("extendedEntities") or item.get("media") or [])
        if isinstance(m, dict)
    ]
    return Reference(
        platform=Platform.X,
        post_id=post_id,
        url=item.get("url") or item.get("twitterUrl") or f"https://x.com/{username}/status/{post_id}",
        author=f"@{username}",
        text=item.get("text") or item.get("full_text") or "",
        created_at=created,
        like_count=int(item.get("likeCount") or item.get("favorite_count") or 0),
        comment_count=int(item.get("replyCount") or item.get("reply_count") or 0),
        share_count=int(item.get("retweetCount") or item.get("retweet_count") or 0),
        view_count=int(item.get("viewCount") or 0),
        media_urls=[u for u in media_urls if u],
        media_type=MediaType.IMAGE if media_urls else MediaType.TEXT,
        author_follower_count=int(author.get("followers") or author.get("followers_count") or 0),
        raw=item,
    )
