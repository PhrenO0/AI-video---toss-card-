"""toss-content CLI.

    toss-content doctor            # 어떤 연동이 살아있는지 점검
    toss-content collect           # 레퍼런스 수집
    toss-content digest            # 슬랙으로 상위 레퍼런스 전송
    toss-content cardnews "주제"    # 카드뉴스 초안 + 프리뷰 (+슬랙 게시)
    toss-content figma inspect     # Figma 파일의 프레임 목록
    toss-content figma export      # 노드를 PNG로 내려받기
    toss-content daily             # collect + digest (CI용)
    toss-content slack-app         # Socket Mode 봇 실행
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys

from . import pipeline
from .config import load_settings
from .models import Platform
from .store import Store


def _setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s · %(message)s",
        datefmt="%H:%M:%S",
    )


# ---------------------------------------------------------------- commands
def cmd_doctor(args, settings, store) -> int:
    """무엇이 연결됐고 무엇이 비었는지 한눈에."""
    checks = [
        ("Slack Bot Token", bool(settings.slack_bot_token), "SLACK_BOT_TOKEN"),
        ("Slack App Token (Socket Mode)", bool(settings.slack_app_token), "SLACK_APP_TOKEN"),
        ("Slack Webhook (폴백)", bool(settings.slack_webhook_url), "SLACK_WEBHOOK_URL"),
        ("X (공식 API)", bool(os.environ.get("X_BEARER_TOKEN")), "X_BEARER_TOKEN"),
        ("Instagram Graph API", bool(os.environ.get("IG_ACCESS_TOKEN")), "IG_ACCESS_TOKEN"),
        ("Threads API", bool(os.environ.get("THREADS_ACCESS_TOKEN")), "THREADS_ACCESS_TOKEN"),
        ("Apify (폴백 수집)", bool(os.environ.get("APIFY_TOKEN")), "APIFY_TOKEN"),
        ("Figma", bool(settings.figma_token), "FIGMA_TOKEN"),
        ("Figma 파일 키", bool(settings.figma.file_key), "config/sources.yaml → figma.file_key"),
        ("Notion", bool(settings.notion_token), "NOTION_TOKEN"),
        (
            "Notion 콘텐츠 목록 DB",
            bool(settings.notion.database_id),
            "notion.database_id (`toss-content notion find` 로 확인)",
        ),
        ("Claude (카피 생성)", bool(os.environ.get("ANTHROPIC_API_KEY")), "ANTHROPIC_API_KEY"),
    ]
    print("\n연동 상태\n" + "─" * 56)
    for name, ok, hint in checks:
        print(f"  {'✅' if ok else '⬜'}  {name:<30} {'' if ok else f'← {hint}'}")

    print(f"\n수집 규칙: {len(settings.sources)}개")
    for platform in Platform:
        rules = settings.queries_for(platform.value)
        order = settings.collect.providers.get(platform.value) or "(기본 순서)"
        print(f"  · {platform.value:<10} 규칙 {len(rules):>2}개 · 프로바이더 {order}")

    counts = store.counts_by_platform()
    print(f"\nDB: {settings.db_path}")
    print(f"  누적 레퍼런스: {sum(counts.values())}건 {counts or ''}")

    # 필수는 슬랙 전송 경로 하나뿐 — 나머지는 있으면 좋은 것들이다.
    if not (settings.slack_bot_token or settings.slack_webhook_url):
        print("\n⚠️  슬랙 전송 경로가 없습니다. dry-run 모드로만 동작합니다.")
    return 0


def cmd_collect(args, settings, store) -> int:
    platforms = None
    if args.platform:
        platforms = [Platform(p.strip()) for p in args.platform.split(",") if p.strip()]

    result = pipeline.run_collect(settings, store, platforms)
    print(f"수집 {result.fetched}건 (신규 {result.inserted}건) {result.by_platform}")
    for i, ref in enumerate(result.top, start=1):
        print(f"  {i:>2}. [{ref.platform.value}] {ref.score:>6.2f}  {ref.author}  {ref.summary(70)}")
    return 0


def cmd_digest(args, settings, store) -> int:
    result = pipeline.run_digest(
        settings, store, limit=args.limit, channel=args.channel, mark=not args.no_mark
    )
    print(f"다이제스트 전송: {result['sent']}건 ({result['mode']} 모드)")
    return 0


def cmd_cardnews(args, settings, store) -> int:
    news, spec_path, previews = pipeline.build_cardnews(
        settings,
        store,
        topic=args.topic,
        card_count=args.cards,
        uids=args.uids.split(",") if args.uids else None,
    )
    print(f"카드뉴스 초안: {news.slug} ({len(news.cards)}장)")
    print(f"  spec    : {spec_path}")
    for path in previews:
        print(f"  preview : {path}")
    for card in news.cards:
        print(f"  {card.index:02d} [{card.kind}] {card.title} — {card.body[:40]}")

    if args.post:
        result = pipeline.publish_cardnews_draft(
            settings, news, previews, channel=args.channel
        )
        print(f"슬랙 게시 완료 ({result['mode']} 모드)")
    return 0


def cmd_figma(args, settings, store) -> int:
    from .figma import from_settings as figma_from_settings

    client = figma_from_settings(settings)

    if args.figma_command == "inspect":
        me = client.whoami()
        print(f"인증 OK: {me.get('email') or me.get('handle')}")
        for frame in client.list_frames(page_name=args.page):
            print(f"  {frame['id']:<12} [{frame['type']:<13}] {frame['page']} / {frame['name']}")
    elif args.figma_command == "export":
        node_ids = [n.strip() for n in args.nodes.split(",") if n.strip()]
        paths = pipeline.export_from_figma(settings, node_ids, args.slug)
        for path in paths:
            print(f"  저장: {path}")
    elif args.figma_command == "comment":
        client.post_comment(args.message, node_id=args.node or "")
        print("코멘트를 남겼습니다.")
    return 0


def cmd_notion(args, settings, store) -> int:
    from .notion import from_settings as notion_from_settings
    from .notion import run_fill
    from .notion.client import extract_id
    from .notion.schema import DEFAULT_ALIASES, resolve_property

    client = notion_from_settings(settings)

    if args.notion_command == "find":
        me = client.whoami()
        print(f"인증 OK: {me.get('name') or me.get('bot', {}).get('owner', {}).get('type', '')}\n")
        results = client.search_data_sources(args.query)
        if not results:
            print(
                "통합에 공유된 데이터베이스가 없습니다.\n"
                "Notion에서 대상 DB → ⋯ → 연결(Connections) → 통합을 추가해주세요."
            )
            return 1
        print("공유된 데이터베이스:")
        for item in results:
            print(f"\n  {item['title'] or '(제목 없음)'}")
            print(f"    database_id : {item['database_id']}")
            print(f"    url         : {item['url']}")
            for source in item["data_sources"]:
                print(f"    data source : {source['name']} ({source['id']})")
        return 0

    if not settings.notion.database_id:
        print(
            "notion.database_id 가 설정되지 않았습니다.\n"
            "`toss-content notion find` 로 ID를 찾아 config/sources.yaml 에 넣어주세요.",
            file=sys.stderr,
        )
        return 1

    if args.notion_command == "schema":
        schema = client.get_schema(settings.notion.database_id)
        print(f"데이터베이스: {extract_id(settings.notion.database_id)}\n")
        print("실제 칼럼:")
        for name, type_ in schema.items():
            print(f"  · {name:<24} {type_}")

        print("\n논리 필드 매핑 (자동 감지 결과):")
        for logical in DEFAULT_ALIASES:
            resolved = resolve_property(logical, schema, settings.notion.properties)
            mark = "✅" if resolved else "⬜"
            print(f"  {mark} {logical:<14} → {resolved or '(없음 — 이 필드는 건너뜁니다)'}")
        print(
            "\n자동 감지가 틀렸다면 config/sources.yaml 의 notion.properties 에 "
            "논리필드: 실제칼럼명 으로 지정하세요."
        )
        return 0

    if args.notion_command == "pending":
        from .notion.sync import pending_rows

        rows = pending_rows(client, settings)
        if not rows:
            print("채울 행이 없습니다.")
            return 0
        print(f"대기 중인 행 {len(rows)}개:")
        for row in rows:
            print(f"  · {row['topic']}  (상태: {row['status'] or '비어 있음'})")
        return 0

    if args.notion_command == "fill":
        results = run_fill(client, settings, store, limit=args.limit, dry_run=args.dry_run)
        if not results:
            print("채울 행이 없습니다.")
            return 0
        for result in results:
            icon = {"filled": "✅", "skipped": "⏭", "failed": "❌"}[result.status]
            detail = result.error or f"{result.slug} · 레퍼런스 {result.reference_count}건"
            print(f"  {icon} {result.topic} — {detail}")
            if result.skipped_fields:
                print(f"      기록 못 한 필드: {', '.join(result.skipped_fields)}")
        return 1 if any(r.status == "failed" for r in results) else 0

    return 0


def cmd_daily(args, settings, store) -> int:
    result = pipeline.run_daily(settings, store)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


def cmd_slack_app(args, settings, store) -> int:
    from .slack.app import run_socket_mode

    return run_socket_mode(settings, store)


# ------------------------------------------------------------------ parser
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="toss-content", description="토스 콘텐츠 자동화 (수집 · 슬랙 · 카드뉴스)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="디버그 로그")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="연동 상태 점검").set_defaults(func=cmd_doctor)

    p_collect = sub.add_parser("collect", help="레퍼런스 수집")
    p_collect.add_argument("--platform", help="x,instagram,threads 중 선택 (쉼표 구분)")
    p_collect.set_defaults(func=cmd_collect)

    p_digest = sub.add_parser("digest", help="슬랙 다이제스트 전송")
    p_digest.add_argument("--limit", type=int, default=None)
    p_digest.add_argument("--channel", default="")
    p_digest.add_argument("--no-mark", action="store_true", help="전송 후 '보냄' 표시를 남기지 않음")
    p_digest.set_defaults(func=cmd_digest)

    p_card = sub.add_parser("cardnews", help="카드뉴스 초안 생성")
    p_card.add_argument("topic", help="카드뉴스 주제")
    p_card.add_argument("--cards", type=int, default=6)
    p_card.add_argument("--uids", default="", help="특정 레퍼런스 uid만 사용 (쉼표 구분)")
    p_card.add_argument("--post", action="store_true", help="슬랙에 초안 게시")
    p_card.add_argument("--channel", default="")
    p_card.set_defaults(func=cmd_cardnews)

    p_figma = sub.add_parser("figma", help="Figma 연동")
    figma_sub = p_figma.add_subparsers(dest="figma_command", required=True)

    p_inspect = figma_sub.add_parser("inspect", help="프레임 목록 보기")
    p_inspect.add_argument("--page", default="")

    p_export = figma_sub.add_parser("export", help="노드를 PNG로 내려받기")
    p_export.add_argument("--nodes", required=True, help="노드 ID (쉼표 구분)")
    p_export.add_argument("--slug", default="export")

    p_comment = figma_sub.add_parser("comment", help="파일에 코멘트 남기기")
    p_comment.add_argument("message")
    p_comment.add_argument("--node", default="")

    p_figma.set_defaults(func=cmd_figma)

    p_notion = sub.add_parser("notion", help="Notion 콘텐츠 목록 연동")
    notion_sub = p_notion.add_subparsers(dest="notion_command", required=True)

    p_find = notion_sub.add_parser("find", help="통합에 공유된 DB 찾기")
    p_find.add_argument("--query", default="", help="DB 제목 검색어")

    notion_sub.add_parser("schema", help="DB 칼럼과 자동 매핑 결과 확인")
    notion_sub.add_parser("pending", help="채울 대기 행 목록")

    p_fill = notion_sub.add_parser("fill", help="대기 행을 자동으로 채우기")
    p_fill.add_argument("--limit", type=int, default=5, help="한 번에 처리할 행 수")
    p_fill.add_argument("--dry-run", action="store_true", help="Notion에 쓰지 않고 결과만 확인")

    p_notion.set_defaults(func=cmd_notion)

    sub.add_parser("daily", help="collect + digest + notion fill (CI용)").set_defaults(
        func=cmd_daily
    )
    sub.add_parser("slack-app", help="Socket Mode 봇 실행").set_defaults(func=cmd_slack_app)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    _setup_logging(args.verbose)
    settings = load_settings()
    store = Store(settings.db_path)

    from .figma.client import FigmaError
    from .notion.client import NotionError
    from .slack.client import SlackError

    try:
        return args.func(args, settings, store)
    except (FigmaError, SlackError, NotionError) as exc:
        # 설정 누락은 사용자가 고칠 문제다 — 트레이스백 대신 안내만 보여준다.
        print(f"\n✗ {exc}\n", file=sys.stderr)
        if args.verbose:
            raise
        print("자세한 오류를 보려면 -v 를 붙여 다시 실행하세요.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n중단했습니다.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
