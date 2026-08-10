"""Slack Socket Mode 봇.

Socket Mode를 쓰는 이유: 공개 HTTPS 엔드포인트가 필요 없다.
사내 방화벽 뒤에서도 돌고, Enterprise Grid 보안 검토도 훨씬 수월하다.

필요 토큰
- ``SLACK_BOT_TOKEN`` (``xoxb-``) — Bot User OAuth Token
- ``SLACK_APP_TOKEN`` (``xapp-``) — App-Level Token, ``connections:write`` 스코프

슬래시 커맨드
- ``/toss-ref [키워드]``    최근 레퍼런스 상위 N건
- ``/toss-cardnews <주제>``  카드뉴스 초안 생성 → 미리보기 + 승인 버튼
"""

from __future__ import annotations

import logging
import threading

from ..config import Settings
from ..models import CardNews
from ..store import Store
from . import blocks as B

log = logging.getLogger(__name__)


def _format_error(exc: Exception) -> list[dict]:
    return B.error_blocks("처리 중 오류가 발생했습니다", f"{type(exc).__name__}: {exc}")


def build_app(settings: Settings, store: Store):
    """Bolt 앱을 조립해서 반환 (테스트에서 핸들러만 떼어 쓰기 쉽게 분리)."""
    from slack_bolt import App

    from .. import pipeline

    app = App(token=settings.slack_bot_token)

    # ------------------------------------------------------------ /toss-ref
    @app.command("/toss-ref")
    def handle_ref(ack, respond, command):
        ack()
        keyword = (command.get("text") or "").strip()
        refs = store.top(limit=30, since_hours=settings.collect.lookback_hours)
        if keyword:
            lowered = keyword.lower()
            refs = [
                r for r in refs
                if lowered in r.text.lower()
                or lowered in r.author.lower()
                or lowered in r.query.lower()
            ]
        refs = refs[: settings.slack.digest_limit]
        title = f"레퍼런스 검색: {keyword}" if keyword else "최근 레퍼런스"
        respond(
            blocks=B.digest_blocks(refs, title=title),
            text=f"{title} {len(refs)}건",
            response_type="in_channel",
        )

    # ------------------------------------------------------- /toss-cardnews
    @app.command("/toss-cardnews")
    def handle_cardnews(ack, respond, command):
        topic = (command.get("text") or "").strip()
        if not topic:
            ack(text="사용법: `/toss-cardnews 대중교통 요금 인상 대응`")
            return
        # 생성은 수십 초가 걸릴 수 있어 3초 ack 제한 안에서 먼저 응답하고 백그라운드로 넘긴다.
        ack(text=f"‘{topic}’ 카드뉴스 초안을 만들고 있어요… (30초 정도 걸립니다)")

        def worker():
            try:
                news, _, previews = pipeline.build_cardnews(settings, store, topic=topic)
                respond(
                    blocks=B.cardnews_blocks(news),
                    text=f"카드뉴스 초안 · {news.topic}",
                    response_type="in_channel",
                )
                log.info("카드뉴스 초안 %s (프리뷰 %d장)", news.slug, len(previews))
            except Exception as exc:
                log.exception("카드뉴스 생성 실패")
                respond(blocks=_format_error(exc), text="카드뉴스 생성 실패")

        threading.Thread(target=worker, daemon=True).start()

    # ---------------------------------------------------------- 버튼 액션
    @app.action("cardnews_draft")
    def handle_draft(ack, body, respond, action):
        ack()
        uids = [u for u in (action.get("value") or "").split(",") if u]
        user = body.get("user", {}).get("id", "")

        def worker():
            try:
                topic = "이번 주 레퍼런스 기반 카드뉴스"
                news, _, _ = pipeline.build_cardnews(
                    settings, store, topic=topic, uids=uids or None
                )
                respond(
                    blocks=B.cardnews_blocks(news),
                    text=f"카드뉴스 초안 · {news.topic}",
                    response_type="in_channel",
                )
            except Exception as exc:
                log.exception("초안 생성 실패 (요청자 %s)", user)
                respond(blocks=_format_error(exc), text="초안 생성 실패")

        threading.Thread(target=worker, daemon=True).start()

    @app.action("cardnews_approve")
    def handle_approve(ack, respond, action, body):
        ack()
        slug = action.get("value", "")
        user = body.get("user", {}).get("id", "")
        store.set_cardnews_status(slug, "approved")

        figma_url = ""
        if settings.figma.file_key:
            figma_url = f"https://www.figma.com/design/{settings.figma.file_key}/"
        respond(
            text=f"`{slug}` 승인됨",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (
                            f"✅ <@{user}> 님이 `{slug}` 를 승인했습니다.\n"
                            f"이제 Figma에서 *TOSS 카드뉴스 생성기* 플러그인을 열고 "
                            f"`out/cardnews/{slug}.json` 의 내용을 붙여넣으면 카드가 생성됩니다."
                            + (f"\n<{figma_url}|Figma 파일 열기>" if figma_url else "")
                        ),
                    },
                }
            ],
            response_type="in_channel",
        )

    @app.action("cardnews_regenerate")
    def handle_regenerate(ack, respond, action):
        ack()
        slug = action.get("value", "")
        record = store.get_cardnews(slug)
        if not record:
            respond(text=f"`{slug}` 를 찾을 수 없습니다.")
            return

        import json

        topic = CardNews.from_spec(json.loads(record["spec"])).topic

        def worker():
            try:
                news, _, _ = pipeline.build_cardnews(settings, store, topic=topic)
                respond(
                    blocks=B.cardnews_blocks(news),
                    text=f"카드뉴스 재생성 · {news.topic}",
                    response_type="in_channel",
                )
            except Exception as exc:
                log.exception("재생성 실패")
                respond(blocks=_format_error(exc), text="재생성 실패")

        threading.Thread(target=worker, daemon=True).start()

    @app.action("cardnews_open_figma")
    def handle_open_figma(ack):
        ack()  # url 버튼이라 별도 처리는 없고 Slack 경고만 막는다

    return app


def run_socket_mode(settings: Settings, store: Store) -> int:
    if not settings.slack_bot_token or not settings.slack_app_token:
        print(
            "SLACK_BOT_TOKEN(xoxb-)과 SLACK_APP_TOKEN(xapp-)이 모두 필요합니다.\n"
            "docs/automation/01-slack-setup.md 를 참고하세요."
        )
        return 1

    from slack_bolt.adapter.socket_mode import SocketModeHandler

    app = build_app(settings, store)
    log.info("Socket Mode 시작 — /toss-ref, /toss-cardnews 사용 가능")
    SocketModeHandler(app, settings.slack_app_token).start()
    return 0
