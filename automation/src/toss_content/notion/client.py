"""Notion REST API 클라이언트.

**2025-09-03 버전의 큰 변화**: 데이터베이스 안에 여러 개의 *data source*가 들어갈 수
있게 되면서, 행 조회 경로가 바뀌었다.

    (구) POST /v1/databases/{database_id}/query      ← deprecated
    (신) POST /v1/data_sources/{data_source_id}/query

database_id와 data_source_id는 서로 다른 객체다. 사용자가 URL에서 복사해오는 것은
database_id이므로, 이 클라이언트는 database → data_sources 를 한 번 조회해서
data_source_id를 자동으로 찾아준다(`resolve_data_source`).

참고: https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03
"""

from __future__ import annotations

import logging
import re
from typing import Any, Iterator

from ..http import get_json, post_json, request_json

log = logging.getLogger(__name__)

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"

#: Notion rich_text 항목 하나의 최대 길이. 넘기면 400이 난다.
RICH_TEXT_LIMIT = 2000

_ID_RE = re.compile(r"([0-9a-fA-F]{32})")
_DASHED_ID_RE = re.compile(
    r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"
)


class NotionError(RuntimeError):
    pass


def extract_id(url_or_id: str) -> str:
    """Notion URL에서 32자리 ID를 뽑아 대시 형식으로 정규화한다.

    Notion URL은 형태가 여러 가지다.
      https://www.notion.so/워크스페이스/제목-<32자리>
      https://app.notion.com/p/제목-<32자리>?source=copy_link
      https://www.notion.so/<32자리>?v=<뷰id>
    """
    value = (url_or_id or "").strip()
    if not value:
        return ""

    # 쿼리스트링의 뷰 ID를 페이지 ID로 잘못 집지 않도록 먼저 잘라낸다.
    base = value.split("?", 1)[0]

    dashed = _DASHED_ID_RE.search(base)
    if dashed:
        return dashed.group(1).lower()

    matches = _ID_RE.findall(base)
    if not matches:
        return value
    raw = matches[-1].lower()  # 경로 마지막에 오는 것이 대상 ID
    return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"


class NotionClient:
    def __init__(self, token: str, version: str = NOTION_VERSION):
        if not token:
            raise NotionError(
                "NOTION_TOKEN이 없습니다. https://www.notion.so/my-integrations 에서 "
                "내부 통합(Internal integration)을 만들고 시크릿을 .env에 넣어주세요."
            )
        self.token = token.strip()
        self.version = version
        self._data_source_cache: dict[str, str] = {}

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.version,
            "Content-Type": "application/json",
        }

    # ------------------------------------------------------------------ auth
    def whoami(self) -> dict[str, Any]:
        return get_json(f"{NOTION_API}/users/me", headers=self._headers)

    # -------------------------------------------------------------- discover
    def search_data_sources(self, query: str = "") -> list[dict[str, Any]]:
        """통합에 공유된 데이터베이스를 찾는다 — DB ID를 모를 때 쓰는 길잡이."""
        payload = post_json(
            f"{NOTION_API}/search",
            headers=self._headers,
            json_body={
                "query": query,
                "filter": {"value": "database", "property": "object"},
                "page_size": 50,
            },
        ) or {}
        results = []
        for item in payload.get("results", []):
            results.append(
                {
                    "database_id": item.get("id", ""),
                    "title": _plain_text(item.get("title", [])),
                    "url": item.get("url", ""),
                    "data_sources": [
                        {"id": ds.get("id"), "name": ds.get("name")}
                        for ds in (item.get("data_sources") or [])
                    ],
                }
            )
        return results

    def get_database(self, database_id: str) -> dict[str, Any]:
        return get_json(
            f"{NOTION_API}/databases/{extract_id(database_id)}", headers=self._headers
        )

    def resolve_data_source(self, database_id: str) -> str:
        """database_id → data_source_id. 이미 data source면 그대로 통과."""
        key = extract_id(database_id)
        if key in self._data_source_cache:
            return self._data_source_cache[key]

        try:
            database = self.get_database(key)
        except Exception as exc:
            # 사용자가 애초에 data_source_id를 준 경우도 있어 한 번 더 확인한다.
            try:
                self.get_data_source(key)
            except Exception:
                raise NotionError(
                    f"데이터베이스를 찾을 수 없습니다: {key}\n"
                    f"· Notion에서 해당 DB → ⋯ → '연결' 에 통합을 추가했는지 확인하세요.\n"
                    f"· 원본 오류: {exc}"
                ) from exc
            self._data_source_cache[key] = key
            return key

        sources = database.get("data_sources") or []
        if not sources:
            raise NotionError(f"데이터베이스에 data source가 없습니다: {key}")
        if len(sources) > 1:
            names = ", ".join(f"{s.get('name')}({s.get('id')})" for s in sources)
            log.warning("data source가 여러 개입니다 — 첫 번째를 사용합니다: %s", names)

        resolved = sources[0]["id"]
        self._data_source_cache[key] = resolved
        return resolved

    def get_data_source(self, data_source_id: str) -> dict[str, Any]:
        return get_json(
            f"{NOTION_API}/data_sources/{extract_id(data_source_id)}", headers=self._headers
        )

    def get_schema(self, database_id: str) -> dict[str, str]:
        """{속성명: 타입} — 어떤 칼럼에 쓸 수 있는지 판단하는 근거."""
        data_source_id = self.resolve_data_source(database_id)
        payload = self.get_data_source(data_source_id)
        return {
            name: prop.get("type", "")
            for name, prop in (payload.get("properties") or {}).items()
        }

    # ----------------------------------------------------------------- query
    def query(
        self,
        database_id: str,
        filter_: dict[str, Any] | None = None,
        sorts: list[dict[str, Any]] | None = None,
        page_size: int = 100,
        max_pages: int = 20,
    ) -> Iterator[dict[str, Any]]:
        """data source의 행을 순회한다 (자동 페이지네이션)."""
        data_source_id = self.resolve_data_source(database_id)
        cursor: str | None = None

        for _ in range(max_pages):
            body: dict[str, Any] = {"page_size": page_size}
            if filter_:
                body["filter"] = filter_
            if sorts:
                body["sorts"] = sorts
            if cursor:
                body["start_cursor"] = cursor

            payload = post_json(
                f"{NOTION_API}/data_sources/{data_source_id}/query",
                headers=self._headers,
                json_body=body,
            ) or {}

            yield from payload.get("results", [])

            if not payload.get("has_more"):
                return
            cursor = payload.get("next_cursor")

    # ----------------------------------------------------------------- write
    def create_page(
        self,
        database_id: str,
        properties: dict[str, Any],
        children: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        data_source_id = self.resolve_data_source(database_id)
        body: dict[str, Any] = {
            "parent": {"data_source_id": data_source_id},
            "properties": properties,
        }
        if children:
            body["children"] = children[:100]  # 생성 시 블록 100개 상한
        return post_json(f"{NOTION_API}/pages", headers=self._headers, json_body=body)

    def update_page(self, page_id: str, properties: dict[str, Any]) -> dict[str, Any]:
        return request_json(
            "PATCH",
            f"{NOTION_API}/pages/{extract_id(page_id)}",
            headers=self._headers,
            json_body={"properties": properties},
        )

    def append_blocks(self, page_id: str, children: list[dict[str, Any]]) -> None:
        """본문 블록 추가. 한 번에 100개까지라 나눠 보낸다."""
        for i in range(0, len(children), 100):
            request_json(
                "PATCH",
                f"{NOTION_API}/blocks/{extract_id(page_id)}/children",
                headers=self._headers,
                json_body={"children": children[i : i + 100]},
            )

    def get_blocks(self, page_id: str, page_size: int = 100) -> list[dict[str, Any]]:
        payload = get_json(
            f"{NOTION_API}/blocks/{extract_id(page_id)}/children",
            headers=self._headers,
            params={"page_size": page_size},
        ) or {}
        return payload.get("results", [])


def _plain_text(rich_text: list[dict[str, Any]]) -> str:
    return "".join(item.get("plain_text", "") for item in rich_text or [])


def from_settings(settings) -> NotionClient:
    return NotionClient(settings.notion_token)
