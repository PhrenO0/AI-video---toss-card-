# AI Video — TOSS Card

한국을 여행하는 일본인 여성 관광객이 개찰구에서 세 번 실패한 `삐빅`의 정체를 축구 심판의 호루라기로 발견하고, TOSS 카드로 통과하는 19.0초 세로형 광고 스토리보드입니다. 무대사 코미디를 실제 한국 지하철의 구조감과 프리미엄 광고 톤으로 구성했습니다.

## 최신 납품 상태

- 메인 스토리보드는 **S01–S13**이며, 총 13장입니다.
- 편집 리듬과 카메라 이동을 정밀하게 전달하는 보조 제어 프레임 **S03A/S03B/S05A/S05B** 4장을 추가했습니다.
- 메인·보조 프레임은 모두 **1080×1920 RGB PNG**, 통합 콘택트시트는 **1488×3354 RGB PNG**입니다.
- 실패는 세 번만 발생합니다: 후면 와이드 → 하이 앵글 → 리더 높이 바텀뷰. 세 번째 실패 뒤에만 얼굴 반응을 둡니다.
- S05는 심판의 풋살화에서 호루라기 얼굴까지 실제로 올라가는 붐업, S06은 관광객 없는 심판 단독 전신입니다.
- S13은 G3 양쪽 플랩이 하우징 안으로 완전히 수납되고, 오른손 TOSS 태그·내린 왼손목 시계·상단 좌측 카피 안전영역을 갖습니다.
- S02·S12·S13의 장면·인물·손·게이트는 승인된 생성 베이스를 보존하고, 카드 면만 [고정 좌표 합성 스크립트](edit/storyboard_gpt2/tools/composite_locked_cards.ps1)로 재현 가능하게 교정했습니다. S12·S13의 제품 글자·칩·로고는 AI 의사 텍스트가 아닌 공식 PNG 소스 픽셀입니다.

## 바로 보기

- [17프레임 통합 콘택트시트](edit/storyboard_gpt2/review/contact-sheet.png)
- [메인 최종 프레임 S01–S13](edit/storyboard_gpt2/frames/final/)
- [S02 — 첫 실패, 엄격한 뒷모습](edit/storyboard_gpt2/frames/final/S02.png)
- [S03B — 세 번째 실패, 리더 높이 바텀뷰](edit/storyboard_gpt2/frames/auxiliary/S03B.png)
- [S04 — 세 번째 실패 뒤 반응](edit/storyboard_gpt2/frames/final/S04.png)
- [S05A — 붐업 시작, 풋살화](edit/storyboard_gpt2/frames/auxiliary/S05A.png)
- [S05B — 붐업 종료, 호루라기 얼굴](edit/storyboard_gpt2/frames/auxiliary/S05B.png)
- [S06 — 심판 단독 전신](edit/storyboard_gpt2/frames/final/S06.png)
- [S08 — A06 복도에서의 접근](edit/storyboard_gpt2/frames/final/S08.png)
- [S12 — 오른손 성공 태그](edit/storyboard_gpt2/frames/final/S12.png)
- [S13 — 완전히 열린 개찰구 엔딩](edit/storyboard_gpt2/frames/final/S13.png)

## 제작자가 바로 사용할 문서·에셋

- [영상 프롬프트 명세](edit/storyboard_gpt2/review/video-prompt-spec.md) — S01–S13의 길이, 카메라, 모션, SFX, 전환, 금지 요소.
- [QA 리포트](edit/storyboard_gpt2/review/qa-report.md) — 공간·캐릭터·제품·손 방향·엔딩 통로 검수.
- [스토리보드 매니페스트](edit/storyboard_gpt2/storyboard-manifest.json) — 19.0초 연속 타임라인과 샷 메타데이터.
- [연속성 바이블](edit/storyboard_gpt2/continuity-bible.md)
- [이미지 생성 프롬프트 팩](edit/storyboard_gpt2/prompts/prompt-pack.md)
- [A05 개찰구 홀 구조 앵커](edit/storyboard_gpt2/anchors/A05_gate_hall_structural_master.png)
- [A06 오른쪽 복도 구조 앵커](edit/storyboard_gpt2/anchors/A06_right_concourse_structural_master.png)
- [일본인 관광객 기준 인물](edit/generated/stills/tourist_lock_JP_v2.jpg)
- [심판 기준 인물](edit/generated/stills/referee_lock_A.png)
- [승인된 크리에이티브 디자인](docs/superpowers/specs/2026-07-18-toss-three-tap-referee-reveal-ending-design.md)
- [승인된 구현 계획](docs/superpowers/plans/2026-07-18-toss-three-tap-referee-reveal-ending.md)
- [기존 프리뷰 v01](edit/preview/TOSS_JP_reel_v01.mp4)
- [기존 프리뷰 QA](edit/preview/QA_REPORT.md)

## 폴더 구조

```text
edit/storyboard_gpt2/
├─ anchors/                 # A05 개찰구 홀, A06 오른쪽 복도 구조 앵커
├─ source_sketches/         # 사용자가 제공한 S01–S13 스토리보드 스케치
├─ frames/raw/              # GPT Image 장면 + S02/S12/S13 고정 카드 면 합성
├─ frames/final/            # 정규화된 메인 납품 프레임 S01–S13
├─ frames/auxiliary/raw/    # 보조 제어 프레임 원본
├─ frames/auxiliary/        # 정규화된 S03A/S03B/S05A/S05B
├─ prompts/                 # 이미지 생성 프롬프트와 연속성 잠금
├─ review/                  # 콘택트시트, QA, 영상 프롬프트 명세
├─ tools/                   # 정규화·콘택트시트 생성 스크립트
└─ tests/                   # 정규화 스크립트 테스트

edit/
├─ generated/               # 캐릭터 시트와 생성 스틸
├─ assembly/                # 편집 세그먼트
├─ audio/                   # 효과음·환경음·내레이션 정보
├─ preview/                 # 기존 렌더와 QA
├─ prompts/                 # 기존 영상 생성 프롬프트
└─ production/              # 자산 매니페스트와 연속성 규칙
```

## 검증

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

검증 스크립트는 보조 프레임 정규화, 1080×1920 RGB 출력, 기존/확장 콘택트시트 크기를 확인합니다.
