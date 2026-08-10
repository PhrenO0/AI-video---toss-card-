"""로컬 카드뉴스 프리뷰 렌더러 (Pillow).

Figma 플러그인은 사람이 Figma를 열어야 돌아간다. 그 전에 슬랙에서
"이 카피로 갈까요?"를 물으려면 눈으로 볼 이미지가 필요하므로,
같은 spec으로 저해상도 프리뷰를 로컬에서 찍는다.

**최종 결과물이 아니라 승인용 프리뷰다.** 실제 납품물은 Figma에서 나온다.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

from ..models import Card, CardNews

log = logging.getLogger(__name__)

# 인스타그램 세로형 4:5
CANVAS = (1080, 1350)
MARGIN = 90

PALETTE = {
    "cover": {"bg": (0, 100, 255), "fg": (255, 255, 255), "sub": (214, 231, 255)},
    "body": {"bg": (255, 255, 255), "fg": (23, 27, 35), "sub": (94, 104, 120)},
    "outro": {"bg": (23, 27, 35), "fg": (255, 255, 255), "sub": (150, 190, 255)},
}

#: 한글이 깨지지 않으려면 CJK 폰트가 필요하다. 없으면 기본 폰트로 떨어진다.
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgunbd.ttf",
]


@lru_cache(maxsize=1)
def _font_path() -> str | None:
    """설치된 CJK 폰트를 한 번만 찾는다 (경고도 한 번만 나가도록)."""
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return path
    log.warning(
        "CJK 폰트를 찾지 못해 프리뷰의 한글이 깨집니다. "
        "`apt-get install fonts-noto-cjk` 또는 Noto Sans KR 설치를 권장합니다."
    )
    return None


@lru_cache(maxsize=8)
def _load_font(size: int):
    from PIL import ImageFont

    path = _font_path()
    if path:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            log.warning("폰트 로드 실패: %s", path)
    return ImageFont.load_default()


def _wrap(draw, text: str, font, max_width: int) -> list[str]:
    """한국어는 공백이 적어 단어 단위 줄바꿈이 잘 안 먹는다. 글자 단위로 자른다."""
    lines: list[str] = []
    current = ""
    for char in text:
        if char == "\n":
            lines.append(current)
            current = ""
            continue
        trial = current + char
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = char
    if current:
        lines.append(current)
    return lines


def render_card(card: Card, out_path: Path) -> Path:
    from PIL import Image, ImageDraw

    colors = PALETTE.get(card.kind, PALETTE["body"])
    image = Image.new("RGB", CANVAS, colors["bg"])
    draw = ImageDraw.Draw(image)

    title_font = _load_font(84 if card.kind == "cover" else 64)
    body_font = _load_font(40)
    badge_font = _load_font(28)

    content_width = CANVAS[0] - MARGIN * 2
    title_lines = _wrap(draw, card.title, title_font, content_width)
    body_lines = _wrap(draw, card.body, body_font, content_width)

    # 본문을 세로 가운데로 — 위쪽에만 몰리면 실제 카드뉴스와 인상이 너무 다르다.
    block_height = (
        (60 if card.badge else 0)
        + len(title_lines) * (title_font.size + 16)
        + (30 if body_lines else 0)
        + len(body_lines) * (body_font.size + 14)
    )
    y = max(MARGIN, (CANVAS[1] - block_height) // 2)

    if card.badge:
        draw.text((MARGIN, y), card.badge.upper(), font=badge_font, fill=colors["sub"])
        y += 60

    for line in title_lines:
        draw.text((MARGIN, y), line, font=title_font, fill=colors["fg"])
        y += title_font.size + 16

    y += 30
    for line in body_lines:
        draw.text((MARGIN, y), line, font=body_font, fill=colors["sub"])
        y += body_font.size + 14

    # 하단 진행 표시 — 몇 번째 장인지 한눈에
    draw.text(
        (MARGIN, CANVAS[1] - MARGIN),
        f"{card.index:02d}",
        font=badge_font,
        fill=colors["sub"],
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path, "PNG")
    return out_path


def render_cardnews(news: CardNews, out_dir: Path) -> list[Path]:
    out_dir = Path(out_dir) / news.slug
    return [
        render_card(card, out_dir / f"{card.index:02d}-{card.kind}.png")
        for card in news.cards
    ]
