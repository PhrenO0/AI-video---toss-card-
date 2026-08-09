"""토스 콘텐츠 자동화 툴킷.

세 갈래로 나뉜다.
- `collectors/` — X · Instagram · Threads 레퍼런스 수집
- `slack/`      — 슬랙 다이제스트와 승인 워크플로
- `figma/` + `cardnews/` — 카드뉴스 초안 생성과 Figma 반영
"""

from .config import Settings, load_settings
from .models import Card, CardNews, MediaType, Platform, Reference
from .store import Store

__version__ = "0.1.0"

__all__ = [
    "Settings",
    "load_settings",
    "Store",
    "Reference",
    "Platform",
    "MediaType",
    "Card",
    "CardNews",
    "__version__",
]
