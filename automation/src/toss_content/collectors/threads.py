"""Threads 레퍼런스 수집.

Meta가 2025년에 Threads API에 키워드 검색을 열었다. 엔드포인트는
``GET https://graph.threads.net/v1.0/keyword_search`` 이고 다음 두 가지가 중요하다.

1. ``threads_keyword_search`` 권한이 **승인되기 전에는** 본인 계정 게시물만 검색된다.
   앱 리뷰를 통과해야 공개 게시물이 검색된다.
2. 레이트리밋이 **7일 롤링 500쿼리**로 빡빡하다. sources.yaml의 Threads 규칙 수 ×
   실행 주기가 이 안에 들어오도록 스케줄을 잡아야 한다.

또한 공개 검색 결과에는 지표가 붙지 않는다. 인사이트(``/insights``)는 자기 소유
게시물에만 열려 있어서, 남의 글은 좋아요 수가 0으로 남는다. 랭킹에서는 이를 감안해
Threads 항목에 최소 점수를 보정해준다(`ranking.py` 참조).

참고: https://developers.facebook.com/docs/threads/keyword-search
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from ..config import CollectConfig, SourceRule
from ..http import HttpError, get_json, post_json
from ..models import MediaType, Platform, Reference
from .base import Collector, Provider, ProviderUnavailable, passes_filters

THREADS_API = "https://graph.threads.net/v1.0"
APIFY_API = "https://api.apify.com/v2"

THREAD_FIELDS = "id,text,permalink,timestamp,username,media_type,media_url,shortcode"

_MEDIA_TYPE_MAP = {
    "TEXT_POST": MediaType.TEXT,
    "IMAGE": MediaType.IMAGE,
    "VIDEO": MediaType.VIDEO,
    "CAROUSEL_ALBUM": MediaType.CAROUSEL,
    "AUDIO": MediaType.VIDEO,
}


def _parse_ts(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))


class ThreadsCollector(Collector):
    platform = Platform.THREADS
    default_provider_order = ("official", "apify")

    @property
    def providers(self) -> dict[str, Provider]:
        return {"official": self._official, "apify": self._apify}

    # ------------------------------------------------------------- official
    def _official(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
        if not token:
            raise ProviderUnavailable("THREADS_ACCESS_TOKEN 미설정")
        if rule.kind == "account":
            # 공식 API로는 남의 계정 타임라인을 통째로 못 읽는다. Apify로 넘긴다.
            raise ProviderUnavailable("Threads 공식 API는 타 계정 타임라인 조회를 지원하지 않음")

        query = rule.value.lstrip("#")
        params = {
            "q": query,
            "search_type": os.environ.get("THREADS_SEARCH_TYPE", "TOP"),
            "fields": THREAD_FIELDS,
            "access_token": token,
        }
        if rule.kind == "hashtag":
            params["search_mode"] = "TAG"

        payload = get_json(f"{THREADS_API}/keyword_search", params=params) or {}
        cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)
        want_insights = os.environ.get("THREADS_FETCH_INSIGHTS", "").lower() in {"1", "true", "yes"}

        refs: list[Reference] = []
        for item in (payload.get("data") or [])[: cfg.per_query_limit]:
            ref = _ref_from_threads(item)
            if ref.created_at < cutoff:
                continue
            if want_insights:
                _attach_insights(ref, token)
            # 공개 검색 결과는 지표가 없어 min_engagement 필터가 전부 걸러버린다.
            # 인사이트를 실제로 받아온 경우에만 필터를 적용한다.
            if want_insights and not passes_filters(ref, cfg):
                continue
            refs.append(ref)
        return refs

    # ---------------------------------------------------------------- apify
    def _apify(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        token = os.environ.get("APIFY_TOKEN", "").strip()
        if not token:
            raise ProviderUnavailable("APIFY_TOKEN 미설정")
        actor = os.environ.get("APIFY_THREADS_ACTOR", "curious_coder~threads-scraper").strip()

        if rule.kind == "account":
            body = {"urls": [f"https://www.threads.net/@{rule.value.lstrip('@')}"]}
        else:
            body = {"searchQueries": [rule.value.lstrip("#")]}
        body["maxItems"] = cfg.per_query_limit

        items = post_json(
            f"{APIFY_API}/acts/{actor}/run-sync-get-dataset-items",
            params={"token": token},
            json_body=body,
            timeout=240,
        ) or []

        cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)
        refs: list[Reference] = []
        for item in items:
            ref = _ref_from_apify_threads(item)
            if ref is None or ref.created_at < cutoff:
                continue
            if passes_filters(ref, cfg):
                refs.append(ref)
        return refs


def _attach_insights(ref: Reference, token: str) -> None:
    """자기 소유 게시물이면 지표를 붙인다. 남의 글이면 권한 오류라 조용히 넘어간다."""
    try:
        payload = get_json(
            f"{THREADS_API}/{ref.post_id}/insights",
            params={"metric": "likes,replies,reposts,quotes,views", "access_token": token},
            max_retries=1,
        ) or {}
    except HttpError:
        return
    for metric in payload.get("data", []) or []:
        value = (metric.get("values") or [{}])[0].get("value", 0)
        match metric.get("name"):
            case "likes":
                ref.like_count = value
            case "replies":
                ref.comment_count = value
            case "reposts" | "quotes":
                ref.share_count += value
            case "views":
                ref.view_count = value


def _ref_from_threads(item: dict) -> Reference:
    username = item.get("username", "unknown")
    media_url = item.get("media_url") or ""
    return Reference(
        platform=Platform.THREADS,
        post_id=str(item["id"]),
        url=item.get("permalink") or f"https://www.threads.net/@{username}",
        author=f"@{username}",
        text=item.get("text") or "",
        created_at=_parse_ts(item.get("timestamp")),
        media_type=_MEDIA_TYPE_MAP.get(item.get("media_type", ""), MediaType.TEXT),
        media_urls=[media_url] if media_url else [],
        raw=item,
    )


def _ref_from_apify_threads(item: dict) -> Reference | None:
    post_id = str(item.get("id") or item.get("pk") or item.get("code") or "")
    if not post_id:
        return None
    created_raw = item.get("timestamp") or item.get("taken_at")
    if isinstance(created_raw, (int, float)):
        created = datetime.fromtimestamp(created_raw, tz=timezone.utc)
    else:
        created = _parse_ts(created_raw)
    username = item.get("username") or (item.get("user") or {}).get("username", "unknown")
    media_urls = [u for u in (item.get("image_urls") or []) if u]
    return Reference(
        platform=Platform.THREADS,
        post_id=post_id,
        url=item.get("url") or item.get("permalink") or "",
        author=f"@{username}",
        text=item.get("text") or item.get("caption") or "",
        created_at=created,
        like_count=int(item.get("like_count") or 0),
        comment_count=int(item.get("reply_count") or 0),
        share_count=int(item.get("repost_count") or 0),
        media_urls=media_urls,
        media_type=MediaType.IMAGE if media_urls else MediaType.TEXT,
        raw=item,
    )
