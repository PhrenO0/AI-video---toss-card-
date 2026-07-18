# AI Video — TOSS Card

한국을 여행하는 일본인 여성 관광객에게 TOSS 카드를 소개하는 세로형 숏폼 광고 프로젝트입니다. 축구 심판의 `삐빅` 호루라기와 개찰구 결제 실패음을 연결한 무대사 코미디를, 실제 한국 지하철 공간과 프리미엄 광고 톤으로 구성했습니다.

## 최신 작업 상태

- GPT Image 기반 9:16 스토리보드: **13컷 완성**
- 최종 스토리보드 규격: **1080×1920 RGB PNG**
- 콘택트시트: **1488×2688 PNG**
- S13 엔딩컷 수정 완료: 심판은 개찰구 화면 오른쪽에 서고 **오른손으로 TOSS 카드를 태그**, 시계가 찬 왼팔은 아래로 유지
- 이전 영상 제작본·오디오·소스 스틸·검수 자료도 `edit/` 아래에 함께 보관

## 바로 보기

- [13컷 콘택트시트](edit/storyboard_gpt2/review/contact-sheet.png)
- [최종 프레임 S01–S13](edit/storyboard_gpt2/frames/final/)
- [수정된 S13 엔딩컷](edit/storyboard_gpt2/frames/final/S13.png)
- [스토리보드 연속성 바이블](edit/storyboard_gpt2/continuity-bible.md)
- [이미지 생성 프롬프트 팩](edit/storyboard_gpt2/prompts/prompt-pack.md)
- [영상 생성 프롬프트 명세](edit/storyboard_gpt2/review/video-prompt-spec.md)
- [QA 리포트](edit/storyboard_gpt2/review/qa-report.md)
- [스토리보드 매니페스트](edit/storyboard_gpt2/storyboard-manifest.json)
- [기존 릴 v01](edit/preview/TOSS_JP_reel_v01.mp4)
- [기존 릴 QA](edit/preview/QA_REPORT.md)

## 폴더 구조

```text
edit/storyboard_gpt2/
├─ anchors/          # 공간·인물 고정 앵커 3장
├─ source_sketches/  # 손그림 스토리보드 S01–S13
├─ frames/raw/       # GPT Image 원본 프레임
├─ frames/final/     # 1080×1920 납품 프레임
├─ prompts/          # 이미지 생성 프롬프트
├─ review/           # 콘택트시트, QA, 영상 프롬프트
├─ tools/            # 규격화·콘택트시트 생성 스크립트
└─ tests/            # 준비 스크립트 테스트

edit/
├─ generated/        # 캐릭터 락, 장면 스틸, 생성 영상
├─ assembly/         # 편집 세그먼트
├─ audio/            # 효과음·환경음 및 라이선스 정보
├─ preview/          # 릴 렌더와 QA 프레임
├─ prompts/          # 기존 영상 제작 프롬프트
└─ production/       # 자산 매니페스트와 연속성 규칙
```

## 검증

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

현재 체크포인트는 13개 최종 PNG, 콘택트시트, 매니페스트 및 S13 오른손 방향 수정까지 PASS입니다.
