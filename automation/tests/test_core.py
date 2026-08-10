"""핵심 로직 단위 테스트 (네트워크 없이 동작)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from toss_content.cardnews.compose import compose_rule_based, slugify
from toss_content.collectors.base import Collector, ProviderUnavailable
from toss_content.config import CollectConfig, RankingConfig, SourceRule
from toss_content.figma.client import extract_file_key, normalize_node_id
from toss_content.models import CardNews, MediaType, Platform, Reference
from toss_content.ranking import NO_METRIC_PROXY, diversify, rank, score_reference
from toss_content.slack import blocks as B
from toss_content.store import Store


def make_ref(
    post_id: str = "1",
    platform: Platform = Platform.X,
    likes: int = 10,
    age_hours: float = 1.0,
    author: str = "@someone",
    text: str = "토스 선불카드 써봤는데 편하네요",
    media: MediaType = MediaType.TEXT,
) -> Reference:
    return Reference(
        platform=platform,
        post_id=post_id,
        url=f"https://example.com/{post_id}",
        author=author,
        text=text,
        created_at=datetime.now(timezone.utc) - timedelta(hours=age_hours),
        like_count=likes,
        media_type=media,
    )


# ------------------------------------------------------------------ models
def test_uid_is_unique_across_platforms():
    a = make_ref("123", Platform.X)
    b = make_ref("123", Platform.INSTAGRAM)
    assert a.uid != b.uid
    assert a.uid == "x:123"


def test_summary_truncates_and_collapses_whitespace():
    ref = make_ref(text="긴  텍스트\n여러 줄" + "가" * 300)
    assert len(ref.summary(50)) == 50
    assert "\n" not in ref.summary(50)


def test_cardnews_spec_roundtrip():
    news = compose_rule_based("교통카드", [make_ref("1"), make_ref("2")], card_count=4)
    restored = CardNews.from_spec(news.to_spec())
    assert restored.slug == news.slug
    assert [c.title for c in restored.cards] == [c.title for c in news.cards]


# ----------------------------------------------------------------- ranking
def test_fresh_post_outranks_stale_post_with_same_engagement():
    cfg = RankingConfig()
    fresh = score_reference(make_ref("a", likes=100, age_hours=1), cfg)
    stale = score_reference(make_ref("b", likes=100, age_hours=200), cfg)
    assert fresh > stale


def test_threads_gets_neutral_proxy_when_metrics_missing():
    """Threads 공개 검색은 지표를 주지 않는다 — 0점으로 묻히면 안 된다."""
    cfg = RankingConfig()
    threads = make_ref("t", Platform.THREADS, likes=0)
    x_zero = make_ref("x", Platform.X, likes=0)
    assert score_reference(threads, cfg) > score_reference(x_zero, cfg)
    assert NO_METRIC_PROXY > 0


def test_rank_sorts_descending_and_sets_scores():
    refs = [make_ref("a", likes=1), make_ref("b", likes=5000)]
    ranked = rank(refs, RankingConfig())
    assert ranked[0].post_id == "b"
    assert all(r.score > 0 for r in ranked)


def test_diversify_caps_per_platform_and_author():
    refs = [make_ref(str(i), Platform.X, author="@same") for i in range(10)]
    refs += [make_ref(f"i{i}", Platform.INSTAGRAM, author=f"@ig{i}") for i in range(5)]
    picked = diversify(rank(refs, RankingConfig()), limit=6, per_platform_cap=3)
    assert len(picked) == 6
    assert sum(1 for r in picked if r.author == "@same") <= 2


def test_diversify_fills_remaining_slots_when_caps_are_tight():
    refs = [make_ref(str(i), Platform.X, author=f"@a{i}") for i in range(10)]
    picked = diversify(rank(refs, RankingConfig()), limit=5, per_platform_cap=2)
    assert len(picked) == 5  # 상한 때문에 모자란 자리는 점수순으로 채운다
    assert len({r.uid for r in picked}) == 5


# ------------------------------------------------------------------- store
@pytest.fixture()
def store(tmp_path):
    return Store(tmp_path / "test.db")


def test_upsert_is_idempotent_and_updates_metrics(store):
    ref = make_ref("1", likes=10)
    assert store.upsert_many([ref]) == 1
    assert store.upsert_many([ref]) == 0  # 같은 uid는 신규가 아님

    ref.like_count = 999
    ref.score = 42.0
    store.upsert_many([ref])
    assert store.get(ref.uid).like_count == 999


def test_only_unnotified_filters_out_sent_items(store):
    refs = [make_ref(str(i), likes=i * 10) for i in range(1, 4)]
    store.upsert_many(rank(refs, RankingConfig()))

    first = store.top(limit=2, only_unnotified=True)
    assert len(first) == 2
    store.mark_notified([r.uid for r in first])

    remaining = store.top(limit=10, only_unnotified=True)
    assert {r.uid for r in remaining}.isdisjoint({r.uid for r in first})


def test_since_hours_excludes_old_posts(store):
    store.upsert_many([make_ref("old", age_hours=500), make_ref("new", age_hours=1)])
    assert [r.post_id for r in store.top(limit=10, since_hours=48)] == ["new"]


def test_cardnews_status_transitions(store):
    store.save_cardnews("slug-1", "주제", '{"cards": []}')
    store.set_cardnews_status("slug-1", "approved", figma_node_id="1:23")
    record = store.get_cardnews("slug-1")
    assert record["status"] == "approved"
    assert record["figma_node_id"] == "1:23"


# -------------------------------------------------------------- collectors
class _FakeCollector(Collector):
    platform = Platform.X
    default_provider_order = ("first", "second")

    def __init__(self):
        self.calls: list[str] = []

    @property
    def providers(self):
        def first(rule, cfg):
            self.calls.append("first")
            raise ProviderUnavailable("토큰 없음")

        def second(rule, cfg):
            self.calls.append("second")
            return [make_ref("from-second")]

        return {"first": first, "second": second}


def test_collector_falls_through_to_next_provider():
    collector = _FakeCollector()
    refs = collector.collect([SourceRule(kind="keyword", value="토스")], CollectConfig())
    assert collector.calls == ["first", "second"]
    assert refs[0].provider == "second"
    assert refs[0].query == "토스"


def test_collector_stops_at_first_successful_provider():
    class _BothWork(_FakeCollector):
        @property
        def providers(self):
            def first(rule, cfg):
                self.calls.append("first")
                return [make_ref("from-first")]

            def second(rule, cfg):
                self.calls.append("second")
                return [make_ref("from-second")]

            return {"first": first, "second": second}

    collector = _BothWork()
    collector.collect([SourceRule(kind="keyword", value="토스")], CollectConfig())
    assert collector.calls == ["first"]


# ------------------------------------------------------------------- figma
@pytest.mark.parametrize(
    "value",
    [
        "https://www.figma.com/design/ztuGJQdoVtA7u9pxvq8m4m/Untitled?node-id=0-1",
        "https://www.figma.com/file/ztuGJQdoVtA7u9pxvq8m4m/Name",
        "ztuGJQdoVtA7u9pxvq8m4m",
    ],
)
def test_extract_file_key(value):
    assert extract_file_key(value) == "ztuGJQdoVtA7u9pxvq8m4m"


def test_normalize_node_id():
    assert normalize_node_id("0-1") == "0:1"
    assert normalize_node_id("0:1") == "0:1"  # 이미 정규형이면 그대로


# ---------------------------------------------------------------- cardnews
def test_rule_based_compose_has_cover_and_outro():
    news = compose_rule_based("교통카드 캠페인", [make_ref(str(i)) for i in range(5)], card_count=6)
    assert news.cards[0].kind == "cover"
    assert news.cards[-1].kind == "outro"
    assert [c.index for c in news.cards] == list(range(1, len(news.cards) + 1))


def test_compose_works_without_references():
    news = compose_rule_based("주제만 있는 경우", [], card_count=3)
    assert len(news.cards) == 2  # cover + outro


def test_slugify_is_url_safe():
    slug = slugify("토스 선불카드 / 캠페인!")
    assert " " not in slug and "/" not in slug and "!" not in slug


# ------------------------------------------------------------------- slack
def test_digest_blocks_stay_within_slack_limit():
    refs = rank([make_ref(str(i), likes=i) for i in range(40)], RankingConfig())
    assert len(B.digest_blocks(refs)) <= B.MAX_BLOCKS


def test_digest_blocks_handle_empty_list():
    blocks = B.digest_blocks([])
    assert any("없습니다" in str(b) for b in blocks)


def test_cardnews_blocks_include_approve_action():
    news = compose_rule_based("주제", [make_ref("1")], card_count=3)
    actions = [b for b in B.cardnews_blocks(news) if b["type"] == "actions"]
    action_ids = {e.get("action_id") for e in actions[0]["elements"]}
    assert "cardnews_approve" in action_ids
