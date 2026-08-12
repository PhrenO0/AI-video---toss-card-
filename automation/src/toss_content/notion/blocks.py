"""Notion 페이지 본문 블록 빌더.

속성(칼럼)에는 짧은 값만 들어간다. 카드뉴스 카피 전문과 레퍼런스 목록처럼
분량이 있는 내용은 페이지 **본문**에 쓴다.
"""

from __future__ import annotations

from typing import Any

from ..models import CardNews, Reference
from .client import RICH_TEXT_LIMIT

#: 자동 생성 구간의 시작 표식 — 사람이 쓴 내용과 구분하기 위해 남긴다.
MARKER = "🤖 자동 생성"


def _text(content: str, bold: bool = False, code: bool = False) -> dict[str, Any]:
    return {
        "type": "text",
        "text": {"content": (content or "")[:RICH_TEXT_LIMIT]},
        "annotations": {"bold": bold, "code": code},
    }


def _link(content: str, url: str) -> dict[str, Any]:
    return {
        "type": "text",
        "text": {"content": (content or "")[:RICH_TEXT_LIMIT], "link": {"url": url}},
    }


def paragraph(content: str) -> dict[str, Any]:
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [_text(content)]}}


def heading(content: str, level: int = 2) -> dict[str, Any]:
    key = f"heading_{min(max(level, 1), 3)}"
    return {"object": "block", "type": key, key: {"rich_text": [_text(content)]}}


def divider() -> dict[str, Any]:
    return {"object": "block", "type": "divider", "divider": {}}


def callout(content: str, emoji: str = "🤖") -> dict[str, Any]:
    return {
        "object": "block",
        "type": "callout",
        "callout": {"rich_text": [_text(content)], "icon": {"type": "emoji", "emoji": emoji}},
    }


def bulleted(rich_text: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": rich_text},
    }


def code_block(content: str, language: str = "json") -> dict[str, Any]:
    return {
        "object": "block",
        "type": "code",
        "code": {"rich_text": [_text(content)], "language": language},
    }


def cardnews_blocks(news: CardNews, spec_path: str = "") -> list[dict[str, Any]]:
    """카드뉴스 초안을 페이지 본문으로."""
    blocks: list[dict[str, Any]] = [
        divider(),
        callout(f"{MARKER} · 카드뉴스 초안 `{news.slug}` ({len(news.cards)}장)"),
        heading("카드뉴스 카피", 2),
    ]

    for card in news.cards:
        badge = f"[{card.badge}] " if card.badge else ""
        blocks.append(
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [_text(f"{card.index:02d}. {badge}{card.title}")]
                },
            }
        )
        if card.body:
            blocks.append(paragraph(card.body))

    if spec_path:
        blocks += [
            heading("Figma 반영 방법", 2),
            paragraph(
                "Figma에서 Plugins → TOSS 카드뉴스 생성기 를 열고 아래 spec을 붙여넣으면 "
                "카드가 생성됩니다."
            ),
            paragraph(spec_path),
        ]
    return blocks


def reference_blocks(refs: list[Reference], title: str = "참고한 레퍼런스") -> list[dict[str, Any]]:
    """근거가 된 레퍼런스 목록 — 나중에 '이 카피 어디서 나왔지?' 추적용."""
    if not refs:
        return []

    blocks: list[dict[str, Any]] = [heading(title, 2)]
    for ref in refs:
        metrics = f" · ♥{ref.like_count} 💬{ref.comment_count}" if ref.engagement else ""
        blocks.append(
            bulleted(
                [
                    _text(f"[{ref.platform.value}] ", bold=True),
                    _link(ref.author, ref.url) if ref.url else _text(ref.author),
                    _text(f" — {ref.summary(150)}{metrics}"),
                ]
            )
        )
    return blocks
