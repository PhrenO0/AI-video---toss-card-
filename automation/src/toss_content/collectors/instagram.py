"""Instagram 레퍼런스 수집.

Basic Display API가 폐지된 뒤로 남은 공식 경로는 **Instagram Graph API**뿐이고,
비즈니스/크리에이터 계정 + Facebook 페이지 연결이 전제다. 두 가지를 쓴다.

- 해시태그 검색: ``ig_hashtag_search`` → ``/{hashtag-id}/top_media``
  (계정당 **주 30개 고유 해시태그** 제한 — sources.yaml의 해시태그 수를 넘기지 말 것)
- 계정 조사: ``business_discovery`` — 상대 비즈니스 계정 동의 없이 공개 정보 조회

폴백으로 Apify 액터를 둔다.
참고: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from ..config import CollectConfig, SourceRule
from ..http import get_json, post_json
from ..models import MediaType, Platform, Reference
from .base import Collector, Provider, ProviderUnavailable, passes_filters

GRAPH_VERSION = os.environ.get("META_GRAPH_VERSION", "v22.0")
GRAPH_API = f"https://graph.facebook.com/{GRAPH_VERSION}"
APIFY_API = "https://api.apify.com/v2"

MEDIA_FIELDS = (
    "id,caption,media_type,media_url,thumbnail_url,permalink,"
    "like_count,comments_count,timestamp"
)

_MEDIA_TYPE_MAP = {
    "IMAGE": MediaType.IMAGE,
    "VIDEO": MediaType.VIDEO,
    "CAROUSEL_ALBUM": MediaType.CAROUSEL,
}


def _parse_ts(value: str | None) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))


class InstagramCollector(Collector):
    platform = Platform.INSTAGRAM
    default_provider_order = ("official", "apify")

    @property
    def providers(self) -> dict[str, Provider]:
        return {"official": self._official, "apify": self._apify}

    # ------------------------------------------------------------- official
    def _official(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
        ig_user_id = os.environ.get("IG_BUSINESS_USER_ID", "").strip()
        if not token or not ig_user_id:
            raise ProviderUnavailable("IG_ACCESS_TOKEN / IG_BUSINESS_USER_ID 미설정")

        if rule.kind == "account":
            return self._business_discovery(rule, cfg, token, ig_user_id)
        if rule.kind in {"hashtag", "keyword"}:
            return self._hashtag_media(rule, cfg, token, ig_user_id)
        raise ProviderUnavailable(f"지원하지 않는 규칙 종류: {rule.kind}")

    def _hashtag_media(
        self, rule: SourceRule, cfg: CollectConfig, token: str, ig_user_id: str
    ) -> list[Reference]:
        tag = rule.value.lstrip("#").replace(" ", "")
        search = get_json(
            f"{GRAPH_API}/ig_hashtag_search",
            params={"user_id": ig_user_id, "q": tag, "access_token": token},
        ) or {}
        data = search.get("data") or []
        if not data:
            return []
        hashtag_id = data[0]["id"]

        payload = get_json(
            f"{GRAPH_API}/{hashtag_id}/top_media",
            params={
                "user_id": ig_user_id,
                "fields": MEDIA_FIELDS,
                "limit": cfg.per_query_limit,
                "access_token": token,
            },
        ) or {}

        cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)
        refs: list[Reference] = []
        for item in payload.get("data", []) or []:
            ref = _ref_from_graph_media(item, author=f"#{tag}")
            # 해시태그 top_media는 timestamp가 비는 경우가 있어, 있을 때만 기간 필터를 건다.
            if item.get("timestamp") and ref.created_at < cutoff:
                continue
            if passes_filters(ref, cfg):
                refs.append(ref)
        return refs

    def _business_discovery(
        self, rule: SourceRule, cfg: CollectConfig, token: str, ig_user_id: str
    ) -> list[Reference]:
        username = rule.value.lstrip("@")
        field = (
            f"business_discovery.username({username})"
            f"{{username,followers_count,media.limit({cfg.per_query_limit}){{{MEDIA_FIELDS}}}}}"
        )
        payload = get_json(
            f"{GRAPH_API}/{ig_user_id}",
            params={"fields": field, "access_token": token},
        ) or {}
        discovery = payload.get("business_discovery") or {}
        followers = discovery.get("followers_count", 0)
        cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)

        refs: list[Reference] = []
        for item in (discovery.get("media") or {}).get("data", []) or []:
            ref = _ref_from_graph_media(item, author=f"@{username}")
            ref.author_follower_count = followers
            if ref.created_at < cutoff:
                continue
            if passes_filters(ref, cfg):
                refs.append(ref)
        return refs

    # ---------------------------------------------------------------- apify
    def _apify(self, rule: SourceRule, cfg: CollectConfig) -> list[Reference]:
        token = os.environ.get("APIFY_TOKEN", "").strip()
        if not token:
            raise ProviderUnavailable("APIFY_TOKEN 미설정")
        actor = os.environ.get("APIFY_IG_ACTOR", "apify~instagram-scraper").strip()

        if rule.kind == "account":
            body = {
                "directUrls": [f"https://www.instagram.com/{rule.value.lstrip('@')}/"],
                "resultsType": "posts",
            }
        else:
            body = {"search": rule.value.lstrip("#"), "searchType": "hashtag", "resultsType": "posts"}
        body["resultsLimit"] = cfg.per_query_limit

        items = post_json(
            f"{APIFY_API}/acts/{actor}/run-sync-get-dataset-items",
            params={"token": token},
            json_body=body,
            timeout=240,
        ) or []

        cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.lookback_hours)
        refs: list[Reference] = []
        for item in items:
            ref = _ref_from_apify_ig(item)
            if ref is None or ref.created_at < cutoff:
                continue
            if passes_filters(ref, cfg):
                refs.append(ref)
        return refs


def _ref_from_graph_media(item: dict, author: str) -> Reference:
    media_url = item.get("media_url") or item.get("thumbnail_url") or ""
    return Reference(
        platform=Platform.INSTAGRAM,
        post_id=str(item["id"]),
        url=item.get("permalink", ""),
        author=author,
        text=item.get("caption") or "",
        created_at=_parse_ts(item.get("timestamp")),
        like_count=item.get("like_count") or 0,
        comment_count=item.get("comments_count") or 0,
        media_type=_MEDIA_TYPE_MAP.get(item.get("media_type", ""), MediaType.IMAGE),
        media_urls=[media_url] if media_url else [],
        raw=item,
    )


def _ref_from_apify_ig(item: dict) -> Reference | None:
    post_id = str(item.get("id") or item.get("shortCode") or "")
    if not post_id:
        return None
    created_raw = item.get("timestamp") or item.get("takenAtTimestamp")
    if isinstance(created_raw, (int, float)):
        created = datetime.fromtimestamp(created_raw, tz=timezone.utc)
    else:
        created = _parse_ts(created_raw)
    media_urls = item.get("images") or ([item["displayUrl"]] if item.get("displayUrl") else [])
    return Reference(
        platform=Platform.INSTAGRAM,
        post_id=post_id,
        url=item.get("url") or f"https://www.instagram.com/p/{item.get('shortCode', '')}/",
        author=f"@{item.get('ownerUsername', 'unknown')}",
        text=item.get("caption") or "",
        created_at=created,
        like_count=int(item.get("likesCount") or 0),
        comment_count=int(item.get("commentsCount") or 0),
        view_count=int(item.get("videoViewCount") or item.get("videoPlayCount") or 0),
        media_type=_MEDIA_TYPE_MAP.get(
            str(item.get("type", "")).upper(),
            MediaType.CAROUSEL if len(media_urls) > 1 else MediaType.IMAGE,
        ),
        media_urls=media_urls,
        raw=item,
    )
