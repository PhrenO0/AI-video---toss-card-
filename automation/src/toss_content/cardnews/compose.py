"""레퍼런스 → 카드뉴스 초안 생성.

두 가지 경로가 있다.

1. **LLM 경로** (`ANTHROPIC_API_KEY` 설정 시): Claude가 레퍼런스를 읽고
   토스 톤에 맞는 카드뉴스 카피를 써준다. 품질이 훨씬 좋다.
2. **규칙 경로** (키 없을 때): 레퍼런스를 요약해 슬롯에 끼워 넣는 결정론적 폴백.
   CI에서 API 호출 없이 파이프라인을 검증할 때도 이 경로를 쓴다.

어느 쪽이든 결과물은 동일한 `CardNews` 객체 = Figma 플러그인이 먹는 spec.
"""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone

from ..models import Card, CardNews, Reference

log = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-opus-5"

#: 토스 선불카드 콘텐츠의 고정 톤. 프롬프트와 폴백이 공유한다.
BRAND_VOICE = """토스 선불카드 카드뉴스의 톤:
- 짧고 담백한 문장. 과장·느낌표 남발 금지.
- 사용자가 겪는 상황을 먼저 말하고, 카드가 그걸 어떻게 해결하는지 잇는다.
- 전문용어 대신 일상어. 숫자는 구체적으로.
- 마지막 카드는 행동 유도 한 줄."""

SYSTEM_PROMPT = f"""당신은 토스 선불카드 SNS 콘텐츠를 만드는 카피라이터입니다.
주어진 소셜 레퍼런스(X/Instagram/Threads에서 반응이 좋았던 게시물)를 분석해
인스타그램 카드뉴스 초안을 씁니다.

{BRAND_VOICE}

규칙:
- 레퍼런스의 '구조와 후킹 방식'만 참고하고, 문장을 그대로 베끼지 않습니다.
- 첫 카드(cover)는 스크롤을 멈추게 하는 한 줄. 20자 이내.
- 본문 카드(body)는 제목 18자 이내, 본문 60자 이내.
- 마지막 카드(outro)는 행동 유도.
- 사실이 확인되지 않은 수치·혜택은 쓰지 않습니다."""

CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "topic": {"type": "string"},
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "enum": ["cover", "body", "outro"]},
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "badge": {"type": "string"},
                },
                "required": ["kind", "title", "body", "badge"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["topic", "cards"],
    "additionalProperties": False,
}


def slugify(text: str) -> str:
    slug = re.sub(r"[^\w가-힣]+", "-", text.strip().lower()).strip("-")
    stamp = datetime.now(timezone.utc).strftime("%y%m%d-%H%M")
    return f"{slug[:40] or 'cardnews'}-{stamp}"


def _reference_digest(refs: list[Reference], limit: int = 8) -> str:
    lines = []
    for i, ref in enumerate(refs[:limit], start=1):
        lines.append(
            f"{i}. [{ref.platform.value}] {ref.author} (♥{ref.like_count} 💬{ref.comment_count})\n"
            f"   {ref.summary(200)}\n"
            f"   {ref.url}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------- LLM 경로
def compose_with_llm(
    topic: str,
    refs: list[Reference],
    card_count: int = 6,
    model: str = DEFAULT_MODEL,
) -> CardNews | None:
    """Claude로 카드뉴스 카피를 생성. 키가 없거나 실패하면 None."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.info("ANTHROPIC_API_KEY 없음 — 규칙 기반 생성으로 넘어갑니다.")
        return None
    try:
        import anthropic
    except ImportError:
        log.warning("anthropic 패키지가 설치되지 않았습니다 — 규칙 기반으로 대체합니다.")
        return None

    client = anthropic.Anthropic()
    prompt = (
        f"주제: {topic}\n\n"
        f"참고 레퍼런스:\n{_reference_digest(refs)}\n\n"
        f"위 레퍼런스를 참고해 총 {card_count}장짜리 카드뉴스 초안을 만들어주세요. "
        f"첫 장은 cover, 마지막 장은 outro, 나머지는 body입니다. "
        f"badge에는 각 카드를 한 단어로 요약한 라벨을 넣어주세요."
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=16000,
            system=SYSTEM_PROMPT,
            output_config={"format": {"type": "json_schema", "schema": CARD_SCHEMA}},
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:  # 네트워크/쿼터 문제로 파이프라인을 멈추지 않는다
        log.warning("Claude 호출 실패 — 규칙 기반으로 대체합니다: %s", exc)
        return None

    if response.stop_reason == "refusal":
        log.warning("Claude가 요청을 거절했습니다 — 규칙 기반으로 대체합니다.")
        return None

    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        log.warning("Claude 응답 파싱 실패 — 규칙 기반으로 대체합니다.")
        return None

    source_uids = [r.uid for r in refs[:8]]
    cards = [
        Card(
            index=i,
            kind=item.get("kind", "body"),
            title=item.get("title", ""),
            body=item.get("body", ""),
            badge=item.get("badge", ""),
            source_uids=source_uids,
        )
        for i, item in enumerate(data.get("cards", []), start=1)
    ]
    if not cards:
        return None
    return CardNews(slug=slugify(topic), topic=data.get("topic", topic), cards=cards)


# --------------------------------------------------------------- 규칙 경로
def compose_rule_based(topic: str, refs: list[Reference], card_count: int = 6) -> CardNews:
    """API 없이 만드는 결정론적 초안. 사람이 손보는 걸 전제로 한 뼈대."""
    cards = [
        Card(
            index=1,
            kind="cover",
            title=topic[:20],
            body="이번 주 반응 좋았던 레퍼런스를 토스 톤으로 정리했어요.",
            badge="COVER",
            source_uids=[r.uid for r in refs[:3]],
        )
    ]

    body_slots = max(card_count - 2, 1)
    for i, ref in enumerate(refs[:body_slots], start=2):
        cards.append(
            Card(
                index=i,
                kind="body",
                title=f"{ref.platform.value.upper()} · {ref.author}"[:18],
                body=ref.summary(60),
                badge=f"참여 {ref.engagement}",
                image_url=ref.media_urls[0] if ref.media_urls else "",
                source_uids=[ref.uid],
            )
        )

    cards.append(
        Card(
            index=len(cards) + 1,
            kind="outro",
            title="토스 선불카드",
            body="지금 토스 앱에서 바로 발급받아 보세요.",
            badge="CTA",
        )
    )
    return CardNews(slug=slugify(topic), topic=topic, cards=cards)


def compose(topic: str, refs: list[Reference], card_count: int = 6) -> CardNews:
    """LLM 먼저 시도하고, 안 되면 규칙 기반으로 폴백."""
    return compose_with_llm(topic, refs, card_count) or compose_rule_based(
        topic, refs, card_count
    )
