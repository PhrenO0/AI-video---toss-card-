# AI Video — TOSS Card

한국을 여행하는 일본인 여성 관광객이 개찰구에서 세 번 실패한 `삐빅`의 정체를 축구 심판의 호루라기로 발견하고, TOSS 카드로 통과하는 19.0초 세로형 광고 스토리보드입니다.

## 현재 납품본

메인 번호는 **S01–S13**을 유지했습니다. 편집 리듬과 카메라 이동을 정확히 전달하기 위해 **S03A, S03B, S05A, S05B** 네 장의 보조 제어 프레임을 더했습니다.

- [17프레임 통합 콘택트시트](edit/storyboard_gpt2/review/contact-sheet.png)
- [S03B — 세 번째 실패, 리더 높이 바텀뷰](edit/storyboard_gpt2/frames/auxiliary/S03B.png)
- [S05A — 붐업 시작, 풋살화](edit/storyboard_gpt2/frames/auxiliary/S05A.png)
- [S05B — 붐업 종료, 호루라기 얼굴](edit/storyboard_gpt2/frames/auxiliary/S05B.png)
- [S06 — 심판 단독 전신](edit/storyboard_gpt2/frames/final/S06.png)
- [S13 — 완전히 열린 개찰구 엔딩](edit/storyboard_gpt2/frames/final/S13.png)

## 바로 사용할 문서

- [영상 프롬프트 명세](edit/storyboard_gpt2/review/video-prompt-spec.md)
- [QA 리포트](edit/storyboard_gpt2/review/qa-report.md)
- [스토리보드 매니페스트](edit/storyboard_gpt2/storyboard-manifest.json)
- [연속성 바이블](edit/storyboard_gpt2/continuity-bible.md)
- [이미지 생성 프롬프트 팩](edit/storyboard_gpt2/prompts/prompt-pack.md)
- [승인된 크리에이티브 디자인](docs/superpowers/specs/2026-07-18-toss-three-tap-referee-reveal-ending-design.md)
- [승인된 구현 계획](docs/superpowers/plans/2026-07-18-toss-three-tap-referee-reveal-ending.md)

## 검증

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

모든 메인·보조 프레임은 1080×1920 RGB PNG이며, 콘택트시트는 1488×3354 RGB PNG입니다.
