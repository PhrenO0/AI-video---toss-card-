# 1. 슬랙 연동 (토스 Enterprise Grid)

목표: 수집한 레퍼런스를 매일 슬랙 채널로 받고, 슬랙에서 바로 카드뉴스 초안을 만들고 승인하기.

## 먼저 알아야 할 것: Enterprise Grid 제약

토스처럼 **Enterprise Grid**를 쓰는 조직은 일반 워크스페이스와 다릅니다.

- 앱 설치에 **조직(Org) 관리자 승인**이 필요합니다. 개인이 임의로 설치할 수 없습니다.
- 워크스페이스별 설치와 조직 전체 설치가 구분됩니다.
- 승인 심사에서 **요청 스코프가 넓을수록 오래 걸립니다.**

그래서 이 툴킷은 전송 경로를 **두 개** 지원합니다. 승인이 오래 걸려도 파이프라인이 멈추지 않게 하기 위해서입니다.

| 경로 | 필요한 것 | 되는 것 | 승인 난이도 |
|---|---|---|---|
| **A. Bot 앱** (권장) | `xoxb-` + `xapp-` 토큰 | 다이제스트, 슬래시 커맨드, 파일 업로드, 버튼 승인 | 보통 (조직 승인 필요) |
| **B. Incoming Webhook** | 웹훅 URL 1개 | 지정 채널에 메시지 게시만 | 낮음 |
| **C. dry-run** | 없음 | 표준출력에 출력 (개발/CI 검증용) | — |

토큰을 아무것도 넣지 않으면 자동으로 C(dry-run)로 동작하므로, 승인 전에도 나머지 기능을 전부 테스트할 수 있습니다.

---

## 경로 A: Bot 앱 (Socket Mode)

**Socket Mode를 쓰는 이유**: 공개 HTTPS 엔드포인트가 필요 없습니다. 사내망 안에서 돌아가고, 보안 검토에서 "외부에 열린 포트가 없다"는 점이 크게 유리합니다.

### A-1. 앱 만들기

1. https://api.slack.com/apps → **Create New App** → *From scratch*
2. 이름 `TOSS 콘텐츠 자동화`, 설치할 워크스페이스 선택
3. **Socket Mode** 메뉴 → `Enable Socket Mode` 켜기
   → App-Level Token이 생성됩니다. 스코프는 `connections:write`.
   → 이 값이 **`SLACK_APP_TOKEN` (`xapp-`로 시작)**

### A-2. 권한(Bot Token Scopes)

**OAuth & Permissions** → *Scopes* → *Bot Token Scopes* 에서 아래만 추가하세요.
필요 이상으로 넓히면 조직 승인이 늦어집니다.

| 스코프 | 왜 필요한가 |
|---|---|
| `chat:write` | 다이제스트/초안 메시지 게시 |
| `commands` | `/toss-ref`, `/toss-cardnews` 슬래시 커맨드 |
| `files:write` | 카드뉴스 프리뷰 이미지 업로드 |
| `channels:read` | `#채널명`을 채널 ID로 변환 |
| `groups:read` | 비공개 채널에 게시할 경우에만 |

> `channels:history` 나 `users:read` 는 이 툴킷에서 쓰지 않습니다. 요청하지 마세요.

### A-3. 슬래시 커맨드 등록

**Slash Commands** → *Create New Command* 를 두 번:

| Command | Short Description | Usage Hint |
|---|---|---|
| `/toss-ref` | 최근 수집된 레퍼런스 보기 | `[키워드]` |
| `/toss-cardnews` | 카드뉴스 초안 생성 | `주제` |

Socket Mode에서는 Request URL 칸이 없습니다(있다면 Socket Mode가 꺼져 있는 것).

### A-4. 설치와 토큰

1. **Install App** → *Install to Workspace*
2. Enterprise Grid라면 여기서 **조직 관리자 승인 요청**이 걸립니다. 승인까지 기다립니다.
3. 승인 후 표시되는 **Bot User OAuth Token** → **`SLACK_BOT_TOKEN` (`xoxb-`로 시작)**
4. 봇을 게시할 채널에 초대: 채널에서 `/invite @TOSS 콘텐츠 자동화`

### A-5. 실행

```bash
cd automation
cp .env.example .env       # SLACK_BOT_TOKEN, SLACK_APP_TOKEN 채우기
pip install -e ".[all]"

toss-content doctor        # 연동 상태 확인
toss-content digest        # 다이제스트 1회 전송
toss-content slack-app     # 슬래시 커맨드 봇 상시 실행
```

---

## 경로 B: Incoming Webhook (승인 대기 중 임시)

가장 좁은 권한이라 승인이 빠릅니다. **채널 하나에 메시지 게시만** 가능하고, 파일 업로드·슬래시 커맨드·스레드 답글은 되지 않습니다.

1. 앱의 **Incoming Webhooks** → 켜기 → *Add New Webhook to Workspace*
2. 게시할 채널 선택 → 생성된 URL을 `.env`의 `SLACK_WEBHOOK_URL`에 넣기

`SLACK_BOT_TOKEN`이 없으면 자동으로 이 경로를 씁니다.

---

## 승인이 끝내 안 될 때

관리자 승인이 막히면 다음 순서로 대응하세요.

1. **경로 B로 우선 가동** — 다이제스트만이라도 채널에 흘려보냅니다.
2. **직접 토큰 제공** — 이미 조직에 설치된 앱이 있다면 그 앱의 봇 토큰을 받아 `SLACK_BOT_TOKEN`에 넣으면 그대로 동작합니다. 필요한 스코프는 A-2 표와 같습니다.
3. **파일로 전달** — `toss-content digest` 없이 `toss-content collect` 결과를 `automation/out/` 에서 꺼내 수동 공유합니다.

---

## 사용법

### 매일 자동 다이제스트

GitHub Actions 워크플로(`.github/workflows/content-automation.yml`)가 평일 오전 9시(KST)에 수집 + 다이제스트를 돌립니다. 저장소 **Settings → Secrets and variables → Actions** 에 `SLACK_BOT_TOKEN` 등을 등록하세요.

### 슬랙에서 바로

```
/toss-ref                       최근 48시간 레퍼런스 상위 8건
/toss-ref 교통카드                키워드로 필터
/toss-cardnews 일본 관광객 교통카드   카드뉴스 초안 생성 → 미리보기 + 승인 버튼
```

다이제스트 메시지 하단의 **🎨 카드뉴스 초안 만들기** 버튼을 누르면 상위 5건을 근거로 초안이 만들어집니다.

## 문제 해결

| 증상 | 원인과 해결 |
|---|---|
| `not_in_channel` | 봇을 채널에 초대하지 않음 → `/invite @앱이름` |
| `missing_scope` | A-2 표의 스코프 누락 → 추가 후 **앱 재설치** 필요 |
| `channel_not_found` | 비공개 채널인데 `groups:read` 없음, 또는 채널명 오타 |
| 슬래시 커맨드 무반응 | `toss-content slack-app` 프로세스가 떠 있는지 확인 (Socket Mode는 상시 실행 필요) |
| 다이제스트가 비어 있음 | 아직 수집이 안 됨 → `toss-content collect` 먼저 실행 |
