"""Notion 속성 읽기/쓰기 어댑터.

**왜 이런 게 필요한가**: 우리는 상대 데이터베이스의 칼럼 구성을 미리 알 수 없다.
칼럼 이름도 타입도 팀마다 다르고, 나중에 바뀌기도 한다. 그런데 Notion은 타입이
안 맞는 값을 보내면 400을 낸다.

그래서 이렇게 처리한다.
1. 실행 시점에 data source 스키마(`{속성명: 타입}`)를 읽는다.
2. 논리적 필드(`topic`, `status`, `summary` …)를 실제 속성명으로 해석한다.
   설정값 → 한국어 기본 별칭 → 영어 별칭 순으로 찾는다.
3. **실제 타입에 맞는 payload를 만든다.** 같은 `status` 필드라도 상대 DB가
   `select`면 select로, `status` 타입이면 status로 보낸다.
4. 없는 속성은 조용히 건너뛴다. 칼럼 하나 없다고 전체가 실패하면 안 된다.
"""

from __future__ import annotations

import logging
from typing import Any

from .client import RICH_TEXT_LIMIT

log = logging.getLogger(__name__)

#: 논리 필드 → 흔히 쓰이는 칼럼명 후보. 위에서부터 먼저 매칭된다.
DEFAULT_ALIASES: dict[str, list[str]] = {
    "topic": ["주제", "제목", "콘텐츠", "이름", "Name", "Title", "Topic"],
    "status": ["상태", "진행", "진행상태", "Status", "State"],
    "platform": ["플랫폼", "채널", "Platform", "Channel"],
    "summary": ["요약", "개요", "설명", "Summary", "Description"],
    "copy": ["카피", "본문", "초안", "Copy", "Draft", "Body"],
    "references": ["레퍼런스", "참고", "참고자료", "References", "Reference"],
    "slug": ["슬러그", "ID", "Slug"],
    "spec_url": ["spec", "스펙", "Spec", "Spec URL"],
    "figma_url": ["피그마", "Figma", "Figma URL", "디자인"],
    "card_count": ["카드수", "장수", "Cards", "Card Count"],
    "updated_at": ["갱신일", "업데이트", "Updated", "Updated At"],
    "tags": ["태그", "키워드", "Tags", "Keywords"],
}

#: 텍스트 계열 — 어느 쪽이든 문자열을 받아 처리할 수 있다.
_TEXT_TYPES = {"title", "rich_text"}
_CHOICE_TYPES = {"select", "status"}


def resolve_property(
    field: str, schema: dict[str, str], overrides: dict[str, str] | None = None
) -> str | None:
    """논리 필드를 실제 Notion 속성명으로 해석. 못 찾으면 None."""
    overrides = overrides or {}

    # 1) 설정으로 명시한 이름이 최우선
    explicit = overrides.get(field)
    if explicit:
        return explicit if explicit in schema else None

    # 2) 기본 별칭 — 정확히 일치하는 것 먼저
    for alias in DEFAULT_ALIASES.get(field, []):
        if alias in schema:
            return alias

    # 3) 대소문자·공백 무시하고 한 번 더
    normalized = {name.strip().lower(): name for name in schema}
    for alias in DEFAULT_ALIASES.get(field, []):
        hit = normalized.get(alias.strip().lower())
        if hit:
            return hit
    return None


def find_title_property(schema: dict[str, str]) -> str | None:
    """title 타입은 DB마다 정확히 하나뿐이다 — 별칭보다 이게 확실하다."""
    for name, type_ in schema.items():
        if type_ == "title":
            return name
    return None


def _chunk_rich_text(text: str) -> list[dict[str, Any]]:
    """Notion은 rich_text 항목 하나당 2000자 제한이 있어 잘라서 넣는다."""
    text = text or ""
    if not text:
        return []
    return [
        {"type": "text", "text": {"content": text[i : i + RICH_TEXT_LIMIT]}}
        for i in range(0, len(text), RICH_TEXT_LIMIT)
    ]


def build_value(prop_type: str, value: Any) -> dict[str, Any] | None:
    """속성 타입에 맞는 쓰기 payload를 만든다. 지원 안 하면 None."""
    if value is None:
        return None

    if prop_type == "title":
        return {"title": _chunk_rich_text(str(value))}
    if prop_type == "rich_text":
        return {"rich_text": _chunk_rich_text(str(value))}
    if prop_type == "select":
        name = str(value).strip()
        # Notion select 옵션명에는 쉼표를 쓸 수 없다.
        return {"select": {"name": name.replace(",", " ")[:100]} if name else None}
    if prop_type == "status":
        name = str(value).strip()
        return {"status": {"name": name[:100]} if name else None}
    if prop_type == "multi_select":
        items = value if isinstance(value, (list, tuple)) else [value]
        return {
            "multi_select": [
                {"name": str(v).replace(",", " ")[:100]} for v in items if str(v).strip()
            ]
        }
    if prop_type == "url":
        return {"url": str(value) or None}
    if prop_type == "email":
        return {"email": str(value) or None}
    if prop_type == "phone_number":
        return {"phone_number": str(value) or None}
    if prop_type == "number":
        try:
            return {"number": float(value)}
        except (TypeError, ValueError):
            return None
    if prop_type == "checkbox":
        return {"checkbox": bool(value)}
    if prop_type == "date":
        start = value.isoformat() if hasattr(value, "isoformat") else str(value)
        return {"date": {"start": start}}

    # people / relation / files / formula / rollup 등은 우리가 채울 수 없다.
    return None


def build_properties(
    fields: dict[str, Any],
    schema: dict[str, str],
    overrides: dict[str, str] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """논리 필드 묶음 → Notion properties. (payload, 건너뛴 필드) 반환."""
    properties: dict[str, Any] = {}
    skipped: list[str] = []

    for field, value in fields.items():
        prop_name = resolve_property(field, schema, overrides)
        if field == "topic" and not prop_name:
            prop_name = find_title_property(schema)
        if not prop_name:
            skipped.append(field)
            continue

        payload = build_value(schema[prop_name], value)
        if payload is None:
            skipped.append(f"{field}({schema[prop_name]} 미지원)")
            continue
        properties[prop_name] = payload

    if skipped:
        log.info("Notion에 기록하지 못한 필드: %s", ", ".join(skipped))
    return properties, skipped


# ------------------------------------------------------------------ 읽기
def read_value(prop: dict[str, Any]) -> Any:
    """Notion 속성 객체 → 파이썬 값."""
    prop_type = prop.get("type", "")

    if prop_type in _TEXT_TYPES:
        return "".join(item.get("plain_text", "") for item in prop.get(prop_type) or [])
    if prop_type in _CHOICE_TYPES:
        chosen = prop.get(prop_type)
        return chosen.get("name") if chosen else None
    if prop_type == "multi_select":
        return [item.get("name") for item in prop.get("multi_select") or []]
    if prop_type in {"url", "email", "phone_number", "number", "checkbox"}:
        return prop.get(prop_type)
    if prop_type == "date":
        date = prop.get("date")
        return date.get("start") if date else None
    if prop_type == "formula":
        formula = prop.get("formula") or {}
        return formula.get(formula.get("type", ""), None)
    if prop_type == "people":
        return [p.get("name") or p.get("id") for p in prop.get("people") or []]
    return None


def read_page(page: dict[str, Any]) -> dict[str, Any]:
    """행 하나를 {속성명: 값} 으로 평탄화."""
    return {
        name: read_value(prop) for name, prop in (page.get("properties") or {}).items()
    }


def get_field(
    row: dict[str, Any],
    field: str,
    schema: dict[str, str],
    overrides: dict[str, str] | None = None,
) -> Any:
    """평탄화된 행에서 논리 필드 값을 꺼낸다."""
    prop_name = resolve_property(field, schema, overrides)
    if field == "topic" and not prop_name:
        prop_name = find_title_property(schema)
    return row.get(prop_name) if prop_name else None
