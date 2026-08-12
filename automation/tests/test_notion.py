"""Notion 연동 단위 테스트 (네트워크 없이 동작)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from toss_content.config import NotionConfig, Settings
from toss_content.models import MediaType, Platform, Reference
from toss_content.notion import blocks as B
from toss_content.notion import schema as S
from toss_content.notion.client import RICH_TEXT_LIMIT, extract_id
from toss_content.notion.sync import _is_pending
from toss_content.cardnews.compose import compose_rule_based


# 실제 사용자가 준 URL 형태를 포함한다.
@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            "https://app.notion.com/p/26-TOSS-Foreigner-Bridge-39ab9019035780069199f931d52b86b4?source=copy_link",
            "39ab9019-0357-8006-9199-f931d52b86b4",
        ),
        (
            "https://www.notion.so/workspace/DB-39ab9019035780069199f931d52b86b4",
            "39ab9019-0357-8006-9199-f931d52b86b4",
        ),
        (
            "39ab9019-0357-8006-9199-f931d52b86b4",
            "39ab9019-0357-8006-9199-f931d52b86b4",
        ),
        ("39ab9019035780069199f931d52b86b4", "39ab9019-0357-8006-9199-f931d52b86b4"),
    ],
)
def test_extract_id(value, expected):
    assert extract_id(value) == expected


def test_extract_id_ignores_view_id_in_query_string():
    """DB URL의 ?v=<뷰id> 를 대상 ID로 잘못 집으면 안 된다."""
    url = (
        "https://www.notion.so/ws/39ab9019035780069199f931d52b86b4"
        "?v=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    assert extract_id(url) == "39ab9019-0357-8006-9199-f931d52b86b4"


def test_extract_id_handles_empty():
    assert extract_id("") == ""


# ------------------------------------------------------------------ 스키마
KOREAN_SCHEMA = {
    "주제": "title",
    "상태": "status",
    "플랫폼": "multi_select",
    "요약": "rich_text",
    "카피": "rich_text",
    "갱신일": "date",
    "카드수": "number",
}

ENGLISH_SCHEMA = {
    "Name": "title",
    "Status": "select",
    "Summary": "rich_text",
}


def test_resolves_korean_column_names():
    assert S.resolve_property("topic", KOREAN_SCHEMA) == "주제"
    assert S.resolve_property("status", KOREAN_SCHEMA) == "상태"
    assert S.resolve_property("copy", KOREAN_SCHEMA) == "카피"


def test_resolves_english_column_names():
    assert S.resolve_property("topic", ENGLISH_SCHEMA) == "Name"
    assert S.resolve_property("status", ENGLISH_SCHEMA) == "Status"


def test_resolve_is_case_insensitive():
    assert S.resolve_property("status", {"status": "select"}) == "status"


def test_explicit_override_wins():
    schema = {"콘텐츠 제목": "title", "주제": "rich_text"}
    assert S.resolve_property("topic", schema, {"topic": "콘텐츠 제목"}) == "콘텐츠 제목"


def test_override_pointing_at_missing_column_returns_none():
    assert S.resolve_property("topic", KOREAN_SCHEMA, {"topic": "없는칼럼"}) is None


def test_topic_falls_back_to_the_title_property():
    """title 타입은 DB에 정확히 하나뿐이라 별칭보다 확실한 단서다."""
    schema = {"완전히 다른 이름": "title", "상태": "status"}
    props, skipped = S.build_properties({"topic": "주제입니다"}, schema)
    assert "완전히 다른 이름" in props
    assert not skipped


def test_status_type_determines_payload_shape():
    """같은 논리 필드라도 상대 DB 타입에 맞춰 모양이 달라져야 한다."""
    as_status, _ = S.build_properties({"status": "완료"}, {"상태": "status"})
    as_select, _ = S.build_properties({"status": "완료"}, {"상태": "select"})
    assert as_status["상태"] == {"status": {"name": "완료"}}
    assert as_select["상태"] == {"select": {"name": "완료"}}


def test_missing_columns_are_skipped_not_fatal():
    props, skipped = S.build_properties(
        {"topic": "주제", "figma_url": "https://figma.com/x"}, {"주제": "title"}
    )
    assert list(props) == ["주제"]
    assert "figma_url" in skipped


def test_unsupported_property_type_is_skipped():
    _, skipped = S.build_properties({"topic": "x"}, {"주제": "relation"})
    assert any("relation" in s for s in skipped)


def test_long_text_is_chunked_under_notion_limit():
    long_text = "가" * 5000
    props, _ = S.build_properties({"copy": long_text}, {"카피": "rich_text"})
    chunks = props["카피"]["rich_text"]
    assert len(chunks) == 3
    assert all(len(c["text"]["content"]) <= RICH_TEXT_LIMIT for c in chunks)


def test_multi_select_strips_commas():
    """Notion multi_select 옵션명에는 쉼표를 쓸 수 없다."""
    props, _ = S.build_properties({"platform": ["a,b"]}, {"플랫폼": "multi_select"})
    assert "," not in props["플랫폼"]["multi_select"][0]["name"]


def test_date_accepts_datetime():
    props, _ = S.build_properties(
        {"updated_at": datetime(2026, 8, 9, tzinfo=timezone.utc)}, {"갱신일": "date"}
    )
    assert props["갱신일"]["date"]["start"].startswith("2026-08-09")


def test_number_coerces_int():
    props, _ = S.build_properties({"card_count": 6}, {"카드수": "number"})
    assert props["카드수"] == {"number": 6.0}


# ------------------------------------------------------------------- 읽기
def test_read_page_flattens_properties():
    page = {
        "properties": {
            "주제": {"type": "title", "title": [{"plain_text": "교통카드"}]},
            "상태": {"type": "status", "status": {"name": "요청"}},
            "플랫폼": {"type": "multi_select", "multi_select": [{"name": "x"}]},
            "빈칸": {"type": "select", "select": None},
        }
    }
    values = S.read_page(page)
    assert values["주제"] == "교통카드"
    assert values["상태"] == "요청"
    assert values["플랫폼"] == ["x"]
    assert values["빈칸"] is None


def test_get_field_uses_logical_name():
    values = {"주제": "교통카드"}
    assert S.get_field(values, "topic", KOREAN_SCHEMA) == "교통카드"


# --------------------------------------------------------------- 처리 판단
@pytest.fixture()
def settings():
    s = Settings()
    s.notion = NotionConfig()
    return s


@pytest.mark.parametrize("value", [None, "", "  ", "요청", "대기", "Todo", "NOT STARTED"])
def test_pending_states(value, settings):
    assert _is_pending(value, settings) is True


@pytest.mark.parametrize("value", ["완료", "done", "DONE", "진행중", "보류"])
def test_non_pending_states(value, settings):
    """완료 상태는 물론, 우리가 모르는 상태도 건드리지 않는다."""
    assert _is_pending(value, settings) is False


# ------------------------------------------------------------------- 블록
def _ref() -> Reference:
    return Reference(
        platform=Platform.X,
        post_id="1",
        url="https://x.com/a/status/1",
        author="@tossteam",
        text="교통카드 잔액 확인",
        created_at=datetime.now(timezone.utc),
        like_count=100,
        media_type=MediaType.IMAGE,
    )


def test_cardnews_blocks_are_valid_notion_shapes():
    news = compose_rule_based("주제", [_ref()], card_count=3)
    built = B.cardnews_blocks(news, spec_path="out/x.json")
    assert all(b.get("object") == "block" and b.get("type") in b for b in built)


def test_cardnews_blocks_carry_the_automation_marker():
    """중복 실행 방지가 이 표식에 의존하므로 반드시 있어야 한다."""
    news = compose_rule_based("주제", [_ref()], card_count=3)
    assert any(B.MARKER in str(b) for b in B.cardnews_blocks(news))


def test_reference_blocks_link_to_source():
    built = B.reference_blocks([_ref()])
    assert any("x.com" in str(b) for b in built)


def test_reference_blocks_empty_for_no_refs():
    assert B.reference_blocks([]) == []


# --------------------------------------------------------------- 행 채우기
FILL_SCHEMA = {
    "주제": "title",
    "상태": "status",
    "플랫폼": "multi_select",
    "요약": "rich_text",
    "카피": "rich_text",
    "레퍼런스": "rich_text",
    "카드수": "number",
}


class FakeNotion:
    """네트워크 없이 fill_row 경로를 통과시키는 최소 스텁."""

    def __init__(self, existing_blocks=None):
        self.updates: list[dict] = []
        self.blocks: list[dict] = []
        self._existing = existing_blocks or []

    def get_schema(self, database_id):
        return FILL_SCHEMA

    def update_page(self, page_id, properties):
        self.updates.append(properties)

    def append_blocks(self, page_id, children):
        self.blocks.extend(children)

    def get_blocks(self, page_id):
        return self._existing


@pytest.fixture()
def filled(tmp_path):
    from toss_content.notion.sync import fill_row
    from toss_content.store import Store

    settings = Settings()
    settings.db_path = tmp_path / "t.db"
    settings.out_dir = tmp_path / "out"
    settings.out_dir.mkdir(parents=True, exist_ok=True)

    store = Store(settings.db_path)
    store.upsert_many([_ref()])

    client = FakeNotion()
    result = fill_row(
        client, settings, store, {"page_id": "p1", "topic": "교통카드"}, schema=FILL_SCHEMA
    )
    return client, result


def test_fill_row_writes_properties_and_body(filled):
    client, result = filled
    assert result.status == "filled"
    assert client.updates and client.blocks


def test_fill_row_does_not_overwrite_the_user_written_title(filled):
    """사람이 적은 주제를 자동화가 덮어쓰면 안 된다 — 입력이 사라지는 최악의 실패다."""
    client, _ = filled
    assert "주제" not in client.updates[0]


def test_fill_row_marks_done_status(filled):
    client, _ = filled
    assert client.updates[0]["상태"] == {"status": {"name": "완료"}}


def test_fill_row_skips_when_already_filled_and_no_status_column():
    """상태 칼럼이 없는 DB는 본문 표식으로 중복 실행을 막는다."""
    from toss_content.notion.sync import fill_row
    from toss_content.store import Store

    settings = Settings()
    schema_without_status = {"주제": "title", "요약": "rich_text"}
    existing = [
        {
            "type": "callout",
            "callout": {"rich_text": [{"plain_text": f"{B.MARKER} · 이전 실행"}]},
        }
    ]
    client = FakeNotion(existing_blocks=existing)
    result = fill_row(
        client,
        settings,
        Store(settings.db_path),
        {"page_id": "p1", "topic": "교통카드"},
        schema=schema_without_status,
    )
    assert result.status == "skipped"
    assert not client.blocks  # 아무것도 추가하지 않았다
