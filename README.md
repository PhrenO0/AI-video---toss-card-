# TOSS 선불카드 콘텐츠 저장소

두 갈래의 작업이 함께 있습니다.

## 1. AI 광고 릴스 (진행 중)

힉스필드(Higgsfield) MCP로 제작하는 세로형(9:16) 12~15초 AI 광고 숏폼.
한국 지하철에서 교통카드 결제에 실패한 일본인 관광객 앞에 축구 심판이 나타나
레드카드처럼 TOSS 선불카드를 선언하는 무대사 상황 코미디.

- 기획·스토리보드·프롬프트: [docs/storyboard.md](docs/storyboard.md)
- 제작 로그: [docs/production-log.md](docs/production-log.md)
- 설계 문서: [docs/superpowers/](docs/superpowers/)
- 손그림 스토리보드: `ai 스토리보드/`
- 카드 에셋: `260702_토스_선불카드_애셋_모음집/`, `assets/toss-card/`
- 클립: `clips/` · 최종본: `output/`

## 2. 콘텐츠 자동화 툴킷 (`automation/`)

레퍼런스 수집 → 슬랙 공유 → 카드뉴스 제작을 잇는 파이프라인.

```
X / Instagram / Threads          Slack                     Figma
        │                          │                         │
   수집 · 랭킹  ────────►  일일 다이제스트 ──►  카드뉴스 초안 ──►  플러그인이 카드 생성
        │                     승인 버튼              │              │
   SQLite 저장                                  프리뷰 PNG      PNG export
```

```bash
cd automation
pip install -e ".[all]"
cp .env.example .env      # 있는 토큰만 채우면 됩니다
toss-content doctor       # 무엇이 연결됐는지 확인
```

토큰이 하나도 없어도 동작합니다 — 수집은 0건, 슬랙은 dry-run으로 떨어집니다.

### 문서

| 문서 | 내용 |
|---|---|
| [automation/README.md](automation/README.md) | 명령어·구조·설계 메모 |
| [01-slack-setup.md](docs/automation/01-slack-setup.md) | 토스 Enterprise Grid 앱 설치, 스코프, 승인 대기 시 대안 |
| [02-reference-collection.md](docs/automation/02-reference-collection.md) | X/IG/Threads API 현실과 폴백 전략, 랭킹 설계 |
| [03-figma-cardnews.md](docs/automation/03-figma-cardnews.md) | 템플릿 규칙, 플러그인 설치, spec 형식 |

### 자동 실행

`.github/workflows/content-automation.yml` 이 평일 오전 9시(KST)에 수집 + 슬랙 다이제스트를 돌립니다.
저장소 **Settings → Secrets and variables → Actions** 에 토큰을 등록하세요.
