"""Block Kit 메시지 빌더."""

from __future__ import annotations

from datetime import datetime

from ..models import CardNews, Platform, Reference

PLATFORM_LABEL = {
    Platform.X: "𝕏",
    Platform.INSTAGRAM: "IG",
    Platform.THREADS: "@",
}

#: Slack 블록은 메시지당 50개가 상한이라 섹션 수를 세어가며 만든다.
MAX_BLOCKS = 50


def _fmt_count(n: int) -> str:
    if n >= 10_000:
        return f"{n / 10_000:.1f}만"
    if n >= 1_000:
        return f"{n / 1_000:.1f}천"
    return str(n)


def _metrics_line(ref: Reference) -> str:
    parts = []
    if ref.like_count:
        parts.append(f"♥ {_fmt_count(ref.like_count)}")
    if ref.comment_count:
        parts.append(f"💬 {_fmt_count(ref.comment_count)}")
    if ref.share_count:
        parts.append(f"🔁 {_fmt_count(ref.share_count)}")
    if ref.view_count:
        parts.append(f"👁 {_fmt_count(ref.view_count)}")
    if not parts:
        parts.append("지표 미제공")
    parts.append(f"점수 {ref.score:g}")
    return " · ".join(parts)


def reference_block(ref: Reference, rank: int) -> dict:
    label = PLATFORM_LABEL.get(ref.platform, ref.platform.value)
    header = f"*{rank}. [{label}] <{ref.url}|{ref.author}>*"
    block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"{header}\n{ref.summary(220)}\n_{_metrics_line(ref)}_",
        },
    }
    if ref.media_urls and ref.media_urls[0].startswith("http"):
        block["accessory"] = {
            "type": "image",
            "image_url": ref.media_urls[0],
            "alt_text": ref.summary(60) or "reference media",
        }
    return block


def digest_blocks(
    refs: list[Reference], title: str = "오늘의 콘텐츠 레퍼런스", note: str = ""
) -> list[dict]:
    """일일 레퍼런스 다이제스트."""
    today = datetime.now().strftime("%Y-%m-%d")
    blocks: list[dict] = [
        {"type": "header", "text": {"type": "plain_text", "text": f"📌 {title} ({today})"}},
    ]
    if note:
        blocks.append(
            {"type": "context", "elements": [{"type": "mrkdwn", "text": note}]}
        )
    if not refs:
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "_조건에 맞는 새 레퍼런스가 없습니다._"},
            }
        )
        return blocks

    blocks.append({"type": "divider"})
    for i, ref in enumerate(refs, start=1):
        # 항목당 블록 2개(섹션+구분선) + 헤더/푸터 여유분
        if len(blocks) >= MAX_BLOCKS - 4:
            break
        blocks.append(reference_block(ref, i))
        blocks.append({"type": "divider"})

    blocks.append(
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "🎨 카드뉴스 초안 만들기"},
                    "style": "primary",
                    "action_id": "cardnews_draft",
                    "value": ",".join(r.uid for r in refs[:5]),
                }
            ],
        }
    )
    return blocks


def cardnews_blocks(news: CardNews, figma_url: str = "", image_urls: list[str] | None = None) -> list[dict]:
    """카드뉴스 초안 미리보기 + 승인 버튼."""
    blocks: list[dict] = [
        {"type": "header", "text": {"type": "plain_text", "text": f"🎨 카드뉴스 초안 · {news.topic}"[:150]}},
        {
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"`{news.slug}` · 총 {len(news.cards)}장 · 템플릿 `{news.template}`"}
            ],
        },
        {"type": "divider"},
    ]
    for card in news.cards:
        if len(blocks) >= MAX_BLOCKS - 5:
            break
        body = card.body.strip() or "_(본문 없음)_"
        badge = f"`{card.badge}` " if card.badge else ""
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{card.index:02d} · {badge}{card.title}*\n{body}",
                },
            }
        )

    for url in (image_urls or [])[:5]:
        blocks.append({"type": "image", "image_url": url, "alt_text": news.topic})

    actions = [
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "✅ 승인 → Figma 반영"},
            "style": "primary",
            "action_id": "cardnews_approve",
            "value": news.slug,
        },
        {
            "type": "button",
            "text": {"type": "plain_text", "text": "🔄 다시 생성"},
            "action_id": "cardnews_regenerate",
            "value": news.slug,
        },
    ]
    if figma_url:
        actions.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Figma에서 열기"},
                "action_id": "cardnews_open_figma",
                "url": figma_url,
            }
        )
    blocks.append({"type": "actions", "elements": actions})
    return blocks


def error_blocks(title: str, detail: str) -> list[dict]:
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"⚠️ *{title}*"}},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"```{detail[:2800]}```"}]},
    ]
