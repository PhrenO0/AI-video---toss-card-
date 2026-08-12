# toss-content — 콘텐츠 자동화 툴킷

레퍼런스 수집 → 슬랙 공유 → 카드뉴스 제작까지 이어지는 파이프라인.

```
X / Instagram / Threads       Slack              Notion              Figma
        │                       │                  │                   │
   수집 · 랭킹 ──────►  일일 다이제스트      콘텐츠 목록 DB      플러그인이 카드 생성
        │                  승인 버튼         주제만 적으면 ──►         │
   SQLite 저장                              레퍼런스·카피 자동      PNG export
```

## 빠른 시작

```bash
cd automation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[all]"

cp .env.example .env      # 있는 토큰만 채우면 됩니다
toss-content doctor       # 무엇이 연결됐는지 확인
```

토큰이 하나도 없어도 동작합니다 — 수집은 0건, 슬랙은 dry-run(표준출력)으로 떨어집니다.

## 명령어

| 명령 | 하는 일 |
|---|---|
| `toss-content doctor` | 연동 상태·수집 규칙·DB 현황 점검 |
| `toss-content collect` | 레퍼런스 수집 → 점수화 → 저장 |
| `toss-content digest` | 상위 레퍼런스를 슬랙으로 |
| `toss-content cardnews "주제"` | 카드뉴스 초안 + 프리뷰 (`--post` 로 슬랙 게시) |
| `toss-content figma inspect` | Figma 파일의 프레임 목록 |
| `toss-content figma export --nodes "1:2,1:3"` | 노드를 PNG로 내려받기 |
| `toss-content notion find` | 통합에 공유된 Notion DB 찾기 |
| `toss-content notion schema` | DB 칼럼과 자동 매핑 결과 확인 |
| `toss-content notion pending` | 채울 대기 행 목록 |
| `toss-content notion fill` | 대기 행을 자동으로 채우기 (`--dry-run` 지원) |
| `toss-content daily` | collect + digest + notion fill (CI용) |
| `toss-content slack-app` | 슬래시 커맨드 봇 (Socket Mode) |

## 구조

```
automation/
├── config/sources.yaml        수집 규칙·랭킹 가중치·채널·Figma 설정
├── .env.example               토큰 (실제 값은 .env, 커밋 안 됨)
├── src/toss_content/
│   ├── models.py              Reference / Card / CardNews
│   ├── config.py              YAML + .env 로딩
│   ├── store.py               SQLite (중복 방지, 전송 이력)
│   ├── http.py                재시도·레이트리밋 백오프
│   ├── ranking.py             점수화와 다변화
│   ├── collectors/            x.py · instagram.py · threads.py (+ 폴백 체인)
│   ├── slack/                 client · blocks · digest · app(Socket Mode)
│   ├── cardnews/              compose(Claude/규칙) · render(프리뷰)
│   ├── figma/                 REST 클라이언트 (읽기 · export · 코멘트)
│   ├── notion/                client(2025-09-03 data source) · schema · blocks · sync
│   ├── pipeline.py            end-to-end 조합
│   └── cli.py                 CLI 진입점
├── figma-plugin/              노드 생성 담당 (REST로는 불가능한 부분)
└── tests/
```

## 설계 메모

**왜 프로바이더 폴백 체인인가** — X/Meta의 API 정책이 자주 바뀝니다. 공식 API가 막히면 Apify, 그것도 안 되면 RSS로 내려가도록 해서 정책 변화에 파이프라인 전체가 죽지 않게 했습니다.

**왜 Figma가 반자동인가** — Figma REST API는 노드를 만들 수 없습니다. 생성은 플러그인 API만 가능하고, 플러그인은 사람이 Figma를 열어야 실행됩니다. 그래서 카피 생성·spec 작성·export는 자동, 카드 생성만 버튼 한 번으로 남겼습니다.

**왜 dry-run이 기본인가** — 토스 Enterprise Grid는 앱 설치에 조직 승인이 필요합니다. 승인 대기 중에도 나머지를 개발·검증할 수 있어야 해서, 토큰이 없으면 자동으로 dry-run으로 떨어집니다.

**왜 Notion 스키마를 실행 시점에 읽는가** — 상대 DB의 칼럼 이름과 타입을 미리 알 수 없고 나중에 바뀌기도 합니다. 타입이 안 맞으면 Notion은 400을 냅니다. 그래서 매 실행마다 스키마를 읽어 논리 필드를 실제 칼럼에 매핑하고, 없는 칼럼은 건너뜁니다 — 칼럼 하나 때문에 전체가 실패하지 않게.

## 문서

- [슬랙 연동](../docs/automation/01-slack-setup.md)
- [레퍼런스 수집](../docs/automation/02-reference-collection.md)
- [카드뉴스 · Figma](../docs/automation/03-figma-cardnews.md)
- [노션 콘텐츠 목록](../docs/automation/04-notion-setup.md)

## 테스트

```bash
python -m pytest -q
```
