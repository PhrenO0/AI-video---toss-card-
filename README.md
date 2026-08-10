# TOSS 포리너 브릿지 크루 2기 — 콘텐츠 저장소

Toss for Travelers **Visitor** 서비스를 **일본인 관광객**에게 알리는 콘텐츠 제작 저장소.
세 갈래의 작업이 함께 있습니다 — ① AI 광고 릴스 ② X·Instagram 콘텐츠 기획 ③ 콘텐츠 자동화 툴킷.

---

## 1. AI 광고 릴스

한국 지하철 개찰구에서 교통카드 결제에 세 번 실패한 일본인 여성 관광객 앞에
축구 심판이 나타나 레드카드처럼 TOSS 선불카드를 선언하는 무대사 상황 코미디.
세로형(9:16), 19.0초.

### 최신 납품 상태

- 메인 스토리보드 **S01–S13** (총 13장) + 보조 제어 프레임 **S03A/S03B/S05A/S05B** 4장
- 메인·보조 프레임 **1080×1920 RGB PNG**, 통합 콘택트시트 **1488×3354 RGB PNG**
- 실패는 세 번만 발생: 후면 와이드 → 하이 앵글 → 리더 높이 바텀뷰. 세 번째 실패 뒤에만 얼굴 반응
- S02·S12·S13은 승인된 생성 베이스를 보존하고 카드 면만
  [고정 좌표 합성 스크립트](edit/storyboard_gpt2/tools/composite_locked_cards.ps1)로 교정 —
  제품 글자·칩·로고는 AI 의사 텍스트가 아닌 **공식 PNG 소스 픽셀**

### 바로 보기

- [17프레임 통합 콘택트시트](edit/storyboard_gpt2/review/contact-sheet.png)
- [메인 최종 프레임 S01–S13](edit/storyboard_gpt2/frames/final/)
- [S13 — 완전히 열린 개찰구 엔딩](edit/storyboard_gpt2/frames/final/S13.png)

### 제작 문서

| 문서 | 내용 |
|---|---|
| [docs/storyboard.md](docs/storyboard.md) | 초기 기획·스토리보드·프롬프트 |
| [docs/production-log.md](docs/production-log.md) | 제작 로그 |
| [edit/storyboard_gpt2/review/video-prompt-spec.md](edit/storyboard_gpt2/review/video-prompt-spec.md) | S01–S13 길이·카메라·모션·SFX·전환·금지 요소 |
| [edit/storyboard_gpt2/review/qa-report.md](edit/storyboard_gpt2/review/qa-report.md) | 공간·캐릭터·제품·손 방향·엔딩 통로 검수 |
| [edit/storyboard_gpt2/continuity-bible.md](edit/storyboard_gpt2/continuity-bible.md) | 연속성 바이블 |
| [docs/superpowers/](docs/superpowers/) | 설계 스펙·구현 계획 |
| [docs/toss-travelers-basutei.md](docs/toss-travelers-basutei.md) | 「バス停」편 통합 문서 |
| [docs/video-prompts-basutei.md](docs/video-prompts-basutei.md) · [video-prompts-buswindow.md](docs/video-prompts-buswindow.md) | 영상 생성용 프롬프트 |

### 폴더

```text
edit/storyboard_gpt2/
├─ anchors/          # 구조 앵커 (개찰구 홀, 복도)
├─ source_sketches/  # 사용자 제공 S01–S13 스케치
├─ frames/final/      # 정규화된 메인 납품 프레임
├─ frames/auxiliary/  # 정규화된 보조 제어 프레임
├─ prompts/           # 이미지 생성 프롬프트·연속성 잠금
├─ review/            # 콘택트시트, QA, 영상 프롬프트 명세
└─ tools/ · tests/    # 합성·정규화 스크립트

ai 스토리보드/                        # 손그림 스토리보드 원본
assets/toss-card/                    # 카드 공식 애셋 — AI 생성 시 reference 필수
260702_토스_선불카드_애셋_모음집/        # 카드 공식 애셋 (원본 모음집)
clips/ · output/                     # 생성 클립 · 최종본
```

검증: `python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q`

---

## 2. X·Instagram 콘텐츠 기획

Toss for Travelers Visitor 서비스를 일본인 관광객에게 알리는 X·Instagram 초안과
그 근거가 된 작업 방식. 채널: Instagram(릴스·캐러셀) · X · TikTok · Threads.

| 문서 | 내용 |
|---|---|
| [docs/content-workflow.md](docs/content-workflow.md) | **우리 작업 방식** — 기획 원칙, 포맷 압축 매핑, 검수 체크리스트, 이미지 일관성 |
| [docs/x-post-drafts.md](docs/x-post-drafts.md) | X 포스트 초안 10건 (일본어 + 한국어 해석 + 이미지 계획) |
| [docs/instagram-drafts.md](docs/instagram-drafts.md) | 인스타 캐러셀 10장 + 릴스 30초 초안, 3채널 동시 발행 계획 |
| [docs/ops-questions.md](docs/ops-questions.md) | 운영진 문의 사항 (복사해 보낼 수 있는 메시지) |
| [docs/design-system.md](docs/design-system.md) | 카드 디자인 시스템 (컬러·타입·그리드·Figma 반입) |
| [docs/references/](docs/references/) | 외부 레퍼런스 요약 3건 |

`assets/design/` — 정보 카드 SVG 5종 (Figma 편집 가능)

### 작업 전 반드시 확인

1. **표현 규칙 4가지** — `プリペイドカード` 명시 / `最初の1枚` 한정 / `カード払いができるお店` 조건 /
   `T-money対応の` 한정. 다듬다가 빠지면 그 순간 금지 표현이 된다
2. **`両替不要` 류 소구 금지** — 일본 결제수단이 충전수단 목록에 없어 원화 현금이 필요하다
3. **AI 생성 금지 영역** — 카드 실물 · 앱 화면 · 결제 순간은 실촬영/실캡처/공식 애셋만
4. **디스클레이머** — 제품 언급 포스트에 `#PR`, 이미지 안에도 표기

자세한 내용은 [docs/content-workflow.md](docs/content-workflow.md) §3, §4 참조.

---

## 3. 콘텐츠 자동화 툴킷 (`automation/`)

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

| 문서 | 내용 |
|---|---|
| [automation/README.md](automation/README.md) | 명령어·구조·설계 메모 |
| [docs/automation/01-slack-setup.md](docs/automation/01-slack-setup.md) | 토스 Enterprise Grid 앱 설치, 스코프, 승인 대기 시 대안 |
| [docs/automation/02-reference-collection.md](docs/automation/02-reference-collection.md) | X/IG/Threads API 현실과 폴백 전략, 랭킹 설계 |
| [docs/automation/03-figma-cardnews.md](docs/automation/03-figma-cardnews.md) | 템플릿 규칙, 플러그인 설치, spec 형식 |

`.github/workflows/content-automation.yml` 이 평일 오전 9시(KST)에 수집 + 슬랙 다이제스트를 돌립니다.
저장소 **Settings → Secrets and variables → Actions** 에 토큰을 등록하세요.
