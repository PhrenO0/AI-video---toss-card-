"""설정 로딩 — `config/*.yaml` + 환경변수(.env).

비밀값(토큰)은 전부 환경변수로만 받는다. YAML에는 절대 토큰을 적지 않는다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
AUTOMATION_ROOT = REPO_ROOT / "automation"
DEFAULT_CONFIG_DIR = AUTOMATION_ROOT / "config"


def _load_dotenv(path: Path) -> None:
    """의존성 없이 .env를 읽어 os.environ에 채운다 (기존 값은 덮어쓰지 않음)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def env_bool(name: str, default: bool = False) -> bool:
    raw = env(name, "").lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "y", "on"}


@dataclass
class SourceRule:
    """수집 규칙 1건 (검색어 또는 계정)."""

    kind: str  # keyword | hashtag | account
    value: str
    platforms: list[str] = field(default_factory=list)
    label: str = ""

    def applies_to(self, platform: str) -> bool:
        return not self.platforms or platform in self.platforms


@dataclass
class CollectConfig:
    lookback_hours: int = 48
    per_query_limit: int = 25
    min_engagement: int = 0
    languages: list[str] = field(default_factory=lambda: ["ko", "ja", "en"])
    exclude_keywords: list[str] = field(default_factory=list)
    #: 플랫폼별 프로바이더 우선순위. 앞에서부터 시도하고 실패하면 다음으로 넘어간다.
    providers: dict[str, list[str]] = field(default_factory=dict)


@dataclass
class RankingConfig:
    half_life_hours: float = 36.0
    weight_engagement: float = 1.0
    weight_velocity: float = 1.4
    weight_keyword: float = 0.6
    weight_media: float = 0.3
    boost_keywords: list[str] = field(default_factory=list)


@dataclass
class SlackConfig:
    default_channel: str = ""
    digest_channel: str = ""
    digest_limit: int = 8
    mention_on_digest: str = ""


@dataclass
class FigmaConfig:
    file_key: str = ""
    template_node_id: str = ""
    page_name: str = "카드뉴스 자동생성"
    export_scale: float = 2.0
    export_format: str = "png"


@dataclass
class NotionConfig:
    #: 콘텐츠 목록 DB. URL 전체를 넣어도 ID를 알아서 뽑는다.
    database_id: str = ""
    #: 레퍼런스를 따로 쌓을 DB (선택)
    reference_database_id: str = ""
    #: 이 상태이거나 비어 있는 행을 처리 대상으로 본다
    trigger_status: list[str] = field(
        default_factory=lambda: ["요청", "대기", "todo", "not started", "새 요청"]
    )
    #: 처리 완료 후 기록할 상태 (첫 값을 사용)
    done_status: list[str] = field(default_factory=lambda: ["완료", "done"])
    failed_status: str = "실패"
    card_count: int = 6
    #: 자동 감지가 틀릴 때 논리 필드 → 실제 칼럼명을 직접 지정
    #: 예) {"topic": "콘텐츠 제목", "status": "진행 상태"}
    properties: dict[str, str] = field(default_factory=dict)


@dataclass
class Settings:
    sources: list[SourceRule] = field(default_factory=list)
    collect: CollectConfig = field(default_factory=CollectConfig)
    ranking: RankingConfig = field(default_factory=RankingConfig)
    slack: SlackConfig = field(default_factory=SlackConfig)
    figma: FigmaConfig = field(default_factory=FigmaConfig)
    notion: NotionConfig = field(default_factory=NotionConfig)
    db_path: Path = AUTOMATION_ROOT / "data" / "references.db"
    out_dir: Path = AUTOMATION_ROOT / "out"

    # --- 비밀값 (환경변수 전용) ---
    @property
    def slack_bot_token(self) -> str:
        return env("SLACK_BOT_TOKEN")

    @property
    def slack_app_token(self) -> str:
        return env("SLACK_APP_TOKEN")

    @property
    def slack_webhook_url(self) -> str:
        return env("SLACK_WEBHOOK_URL")

    @property
    def figma_token(self) -> str:
        return env("FIGMA_TOKEN")

    @property
    def notion_token(self) -> str:
        return env("NOTION_TOKEN")

    def queries_for(self, platform: str) -> list[SourceRule]:
        return [r for r in self.sources if r.applies_to(platform)]


def load_settings(config_dir: Path | None = None) -> Settings:
    config_dir = config_dir or DEFAULT_CONFIG_DIR
    _load_dotenv(AUTOMATION_ROOT / ".env")
    _load_dotenv(REPO_ROOT / ".env")

    raw: dict[str, Any] = {}
    sources_file = config_dir / "sources.yaml"
    if sources_file.exists():
        raw = yaml.safe_load(sources_file.read_text(encoding="utf-8")) or {}

    settings = Settings()

    for item in raw.get("sources", []) or []:
        settings.sources.append(
            SourceRule(
                kind=item.get("kind", "keyword"),
                value=item["value"],
                platforms=item.get("platforms", []) or [],
                label=item.get("label", ""),
            )
        )

    for section, target in (
        ("collect", settings.collect),
        ("ranking", settings.ranking),
        ("slack", settings.slack),
        ("figma", settings.figma),
        ("notion", settings.notion),
    ):
        for key, value in (raw.get(section) or {}).items():
            if hasattr(target, key):
                setattr(target, key, value)

    if raw.get("db_path"):
        settings.db_path = (AUTOMATION_ROOT / str(raw["db_path"])).resolve()
    if raw.get("out_dir"):
        settings.out_dir = (AUTOMATION_ROOT / str(raw["out_dir"])).resolve()

    # 환경변수로 덮어쓸 수 있게 (CI에서 편함)
    if env("FIGMA_FILE_KEY"):
        settings.figma.file_key = env("FIGMA_FILE_KEY")
    if env("SLACK_DIGEST_CHANNEL"):
        settings.slack.digest_channel = env("SLACK_DIGEST_CHANNEL")
    if env("NOTION_DATABASE_ID"):
        settings.notion.database_id = env("NOTION_DATABASE_ID")
    if env("NOTION_REFERENCE_DATABASE_ID"):
        settings.notion.reference_database_id = env("NOTION_REFERENCE_DATABASE_ID")

    settings.db_path.parent.mkdir(parents=True, exist_ok=True)
    settings.out_dir.mkdir(parents=True, exist_ok=True)
    return settings
