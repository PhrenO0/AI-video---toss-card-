# TOSS Structural-Realism Storyboard Regeneration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (- [ ]) syntax for tracking.

**Goal:** 현실 지하철 사진의 구조적 규칙을 해석해 간판·게이트·복도를 재설계하고, 제공된 일본인 여성의 얼굴을 고정한 13컷 스토리보드로 교체한다.

**Architecture:** 현실 사진은 합성 배경이 아니라 A05 게이트 홀과 A06 오른쪽 복도의 구조 레퍼런스로만 사용한다. 두 공간 앵커를 먼저 승인한 뒤 인물·제품 프레임을 생성하며, S03과 S04는 동일한 일반 회색 카드의 정확히 두 번의 실패로 구성한다. 최종 선택본만 raw 프레임에 승격하고 기존 정규화 도구로 1080×1920 RGB와 콘택트시트를 재생성한다.

**Tech Stack:** built-in GPT Image, Pillow, pytest, PowerShell, Git

## Global Constraints

- 현실 사진을 직접 배경으로 복사하거나 합성하지 않는다.
- 타는 곳 / Tracks 패널은 유지하되 실제 두께, 두 개의 행거, 천장 고정 플레이트와 그림자를 갖게 한다.
- 관광객은 edit/generated/stills/tourist_lock_JP_v2.jpg의 인물로 고정한다.
- S02는 얼굴과 옆얼굴이 전혀 보이지 않는 완전 후면 구도다.
- S03은 첫 실패 하이앵글, S04는 단 한 번의 재시도를 보여주는 리더기 높이 바텀뷰다.
- S04 관광객의 시선은 카메라가 아니라 일반 회색 카드와 리더기 접점에 향한다.
- TOSS 카드는 S10 전에는 등장하지 않는다.
- S12·S13은 화면 오른쪽의 심판이 시계 없는 오른손으로 태그하고 왼손목 시계는 아래에 둔다.
- 최종 산출물은 1080×1920 RGB PNG 13장과 1488×2688 콘택트시트다.

---

### Task 1: Reference Provenance and Prompt Locks

**Files:**
- Create: edit/storyboard_gpt2/references/structural/right-concourse-reference.jpg
- Create: edit/storyboard_gpt2/references/structural/gate-hall-reference.jpg
- Create: edit/storyboard_gpt2/references/structural/current-contact-sheet-reference.jpg
- Modify: edit/storyboard_gpt2/continuity-bible.md
- Modify: edit/storyboard_gpt2/prompts/prompt-pack.md

**Interfaces:**
- Consumes: 사용자가 제공한 Photo 1, Photo 2, Photo 3과 tourist_lock_JP_v2.jpg
- Produces: 모든 후속 생성 호출이 참조할 구조 레퍼런스 경로와 공통 프롬프트 잠금

- [ ] **Step 1: 레퍼런스 세 장을 프로젝트 안에 원본 그대로 복사**

    Copy-Item -LiteralPath 'C:\Users\jun12\Documents\📁 AI_프로젝트\Toss foreigner Bridge Crew\.codex-remote-attachments\019f70b7-14e8-7133-97b7-e6a6d8c7233c\21d895f9-ed57-48af-908f-50b15bc6572d\1-Photo-1.jpg' -Destination edit/storyboard_gpt2/references/structural/right-concourse-reference.jpg
    Copy-Item -LiteralPath 'C:\Users\jun12\Documents\📁 AI_프로젝트\Toss foreigner Bridge Crew\.codex-remote-attachments\019f70b7-14e8-7133-97b7-e6a6d8c7233c\21d895f9-ed57-48af-908f-50b15bc6572d\2-Photo-2.jpg' -Destination edit/storyboard_gpt2/references/structural/gate-hall-reference.jpg
    Copy-Item -LiteralPath 'C:\Users\jun12\Documents\📁 AI_프로젝트\Toss foreigner Bridge Crew\.codex-remote-attachments\019f70b7-14e8-7133-97b7-e6a6d8c7233c\21d895f9-ed57-48af-908f-50b15bc6572d\3-Photo-3.jpg' -Destination edit/storyboard_gpt2/references/structural/current-contact-sheet-reference.jpg

- [ ] **Step 2: 해시와 이미지 모드를 검증**

    각 원본과 복사본의 SHA-256이 같아야 한다. Pillow로 세 파일이 열리고 너비와 높이가 0보다 큰지 검사한다.

- [ ] **Step 3: 연속성 바이블과 프롬프트 팩 갱신**

    공통 금지 문장은 다음과 같이 고정한다.

    no direct photo composite, no oversized hero sign, no floating sign, no paper-thin sign, no repeated blue placards, no readable gibberish, no showroom symmetry, no idle mannequin pose

    공통 인물 문장은 다음과 같이 고정한다.

    preserve the exact face, full bangs, eye shape, jawline and shoulder-length hair from tourist_lock_JP_v2.jpg; show action-in-progress with grounded feet, contact shadow, cloth inertia and suitcase wheel direction

- [ ] **Step 4: 문서 검증**

    Get-Content -Raw -Encoding UTF8 edit/storyboard_gpt2/continuity-bible.md
    Get-Content -Raw -Encoding UTF8 edit/storyboard_gpt2/prompts/prompt-pack.md

    구조 레퍼런스 세 경로, 타는 곳 패널 유지, 제공 인물 고정, S04 바텀뷰 문장이 모두 존재해야 한다.

- [ ] **Step 5: 커밋**

    git add edit/storyboard_gpt2/references/structural edit/storyboard_gpt2/continuity-bible.md edit/storyboard_gpt2/prompts/prompt-pack.md
    git commit -m "docs: lock structural subway references"

### Task 2: A05 Gate Hall and A06 Right-Concourse Anchors

**Files:**
- Create: edit/storyboard_gpt2/anchors/A05_gate_hall_structural_master.png
- Create: edit/storyboard_gpt2/anchors/A06_right_concourse_structural_master.png

**Interfaces:**
- Consumes: gate-hall-reference.jpg, right-concourse-reference.jpg, A01_gate_master.png, A04_right_concourse_master.png
- Produces: 게이트 장면용 A05와 복도 장면용 A06

- [ ] **Step 1: A05 게이트 홀 생성**

    Built-in GPT Image prompt:

    Use case: ads-marketing. Create a portrait 9:16 photorealistic Korean subway fare-gate hall. Interpret only the architecture and installation logic of gate-hall-reference.jpg; do not copy or composite the photo. Keep modern stainless flap gates from A01. Retain one slim matte-black 타는 곳 / Tracks panel, physically suspended from the ceiling by two narrow metal rods with visible ceiling plates, realistic panel thickness, subtle underside shadow and correct clearance. Gates, readers, ceiling fixtures, columns and floor grout share one vanishing point. Add restrained depth from columns and distant displays. No people, no TOSS card, no oversized sign, no repeated placards, no gibberish, no showroom symmetry.

- [ ] **Step 2: A05 시각 검수**

    패널이 시설물로 읽히고, 다섯 개 이상 통로가 실제 폭으로 보이며, 타는 곳 / Tracks 외의 선명한 가짜 문자가 없어야 한다.

- [ ] **Step 3: A06 오른쪽 복도 생성**

    Built-in GPT Image prompt:

    Use case: ads-marketing. Create a portrait 9:16 photorealistic Korean subway side concourse. Interpret only the spatial rules of right-concourse-reference.jpg; do not copy or composite the photo. Use a low metal-panel ceiling with linear fluorescent fixtures, tiled round columns on the left, flat tiled service wall on the right, one column-mounted vertical wayfinding panel with a real metal bracket, one framed route map recessed on the right wall, tactile paving and grounded maintenance details. All fixtures follow one vanishing point. No fare gates, no 타는 곳 hero sign, no people, no readable gibberish, no repeated blue signs.

- [ ] **Step 4: A06 시각 검수**

    개찰구가 없어야 하고, 안내판은 최대 두 개이며 브래킷·프레임 두께·접촉 그림자가 보여야 한다.

- [ ] **Step 5: 앵커 커밋**

    git add edit/storyboard_gpt2/anchors/A05_gate_hall_structural_master.png edit/storyboard_gpt2/anchors/A06_right_concourse_structural_master.png
    git commit -m "feat: add structure-aware subway anchors"

### Task 3: Opening and Two-Failure Sequence

**Files:**
- Modify: edit/storyboard_gpt2/frames/raw/S01.png
- Modify: edit/storyboard_gpt2/frames/raw/S02.png
- Modify: edit/storyboard_gpt2/frames/raw/S03.png
- Modify: edit/storyboard_gpt2/frames/raw/S04.png

**Interfaces:**
- Consumes: A05, tourist_lock_JP_v2.jpg, existing S01–S04
- Produces: 현실적인 게이트 소개, 후면 진입, 첫 실패, 한 번의 재시도

- [ ] **Step 1: S01 생성**

    A05와 동일한 공간을 유지하고, 카메라를 사람 눈높이보다 조금 낮춘 28–35mm 정면 와이드로 둔다. 빈 게이트 홀의 사용 흔적과 미세한 비대칭은 허용하되 사람과 카드는 생성하지 않는다.

- [ ] **Step 2: S02 완전 후면 생성**

    Tourist is seen strictly from behind, with no face or cheek visible, finishing her last half-step toward the center fare gate. She faces the gates squarely. Her right arm begins to rise toward the reader; her left hand pulls the silver suitcase trailing diagonally 30–40 degrees behind. Weight settles on the left foot, right heel still moving, blouse hem and hair retain slight stopping inertia. Preserve exact clothing, hair length and luggage from tourist_lock_JP_v2.jpg. She is integrated by matching ceiling light, contact shadow and floor reflection. No card visible yet.

- [ ] **Step 3: S03 첫 실패 하이앵글 생성**

    같은 A05 게이트와 관광객을 유지한다. 위에서 내려다보며 오른손의 일반 회색 카드, 붉은 X 리더기, 닫힌 플랩과 뒤쪽 캐리어를 보여준다. 얼굴은 보이지 않고 TOSS 카드는 금지한다.

- [ ] **Step 4: S04 단 한 번 재시도 바텀뷰 생성**

    Reader-level bottom view from beside the card sensor. The ordinary gray card and her right hand dominate the near lower foreground as she taps a second and final time. Beyond the card, preserve the exact face from tourist_lock_JP_v2.jpg. Her eyes look downward at the card-reader contact point, never at the camera. Her eyebrows draw together slightly and lips part minimally in a restrained puzzled expression. The gate shows a red failure state and stays closed. No exaggerated face, no selfie angle, no TOSS card.

- [ ] **Step 5: 두 번의 실패 검수**

    S03과 S04가 동일한 일반 회색 카드의 첫 시도와 단 한 번의 재시도로 읽혀야 한다. S04는 낮은 리더기 시점, 카드 쪽 시선, 의아한 표정이 동시에 보여야 한다.

- [ ] **Step 6: 오프닝 시퀀스 커밋**

    git add edit/storyboard_gpt2/frames/raw/S01.png edit/storyboard_gpt2/frames/raw/S02.png edit/storyboard_gpt2/frames/raw/S03.png edit/storyboard_gpt2/frames/raw/S04.png
    git commit -m "feat: rebuild opening and two-failure sequence"

### Task 4: Right-Concourse Approach

**Files:**
- Modify: edit/storyboard_gpt2/frames/raw/S06.png
- Modify: edit/storyboard_gpt2/frames/raw/S08.png

**Interfaces:**
- Consumes: A06, tourist_lock_JP_v2.jpg, referee_lock_A.png
- Produces: 같은 복도 축에서 이어지는 두 단계 접근

- [ ] **Step 1: S06 생성**

    A06 복도를 유지한다. 관광객의 뒤통수와 왼쪽 어깨는 전경 왼쪽에서 오른쪽으로 몸을 돌리는 중이며, 심판은 먼 중경에서 호루라기를 마치고 첫걸음을 옮긴다. 인물의 광원과 바닥 그림자는 A06과 일치시킨다.

- [ ] **Step 2: S08 생성**

    S06과 동일한 렌즈 축·복도·관광객 OTS 위치를 유지하고, 심판만 두 걸음 가까워진 중간 보행 자세로 만든다. 팔과 반대 다리의 교차, 신발 접지와 그림자가 자연스러워야 한다.

- [ ] **Step 3: 연속성 검수**

    두 컷의 기둥·노선도·조명 위치가 같은 공간으로 이어지고, S08 심판의 크기만 합리적으로 커져야 한다. 개찰구와 타는 곳 패널은 보이면 안 된다.

- [ ] **Step 4: 접근 시퀀스 커밋**

    git add edit/storyboard_gpt2/frames/raw/S06.png edit/storyboard_gpt2/frames/raw/S08.png
    git commit -m "feat: ground referee approach in realistic concourse"

### Task 5: Identity and Gate-Hall Continuity

**Files:**
- Modify: edit/storyboard_gpt2/frames/raw/S07.png
- Modify: edit/storyboard_gpt2/frames/raw/S09.png
- Modify: edit/storyboard_gpt2/frames/raw/S10.png
- Modify: edit/storyboard_gpt2/frames/raw/S11.png
- Modify: edit/storyboard_gpt2/frames/raw/S12.png
- Modify: edit/storyboard_gpt2/frames/raw/S13.png

**Interfaces:**
- Consumes: A05, tourist_lock_JP_v2.jpg, referee_lock_A.png, exact TOSS card reference
- Produces: 제공 인물과 구조적 게이트 홀로 통일된 후반부

- [ ] **Step 1: S07과 S09 인물 재생성**

    S07은 제공 인물의 얼굴로 심판 방향 반응을 재생성하고, S09는 A05 게이트 홀에서 심판이 오른쪽에서 프레임으로 들어와 멈추는 행동 중간을 잡는다. 관광객의 눈은 심판을 따라가고 몸은 게이트 앞에 자연스럽게 남는다.

- [ ] **Step 2: S10과 S11 제품 공개 재생성**

    S10은 가슴주머니에서 카드 상단 1/3이 나오는 순간, S11은 오른팔 최고점의 한 장 카드를 보여준다. A05 패널은 물리적 두께와 행거가 유지되며 TOSS 카드의 비율과 로고가 레퍼런스와 일치해야 한다.

- [ ] **Step 3: S12와 S13 태그 재생성**

    심판은 화면 오른쪽에 둔다. 시계 없는 오른손이 카드를 들고 리더기로 이어지며, 검은 시계가 찬 왼팔은 아래에 고정한다. S13 관광객은 제공 인물과 같은 얼굴·머리이며 캐리어와 함께 게이트 통과 동작을 마친다.

- [ ] **Step 4: 후반부 검수**

    S10 이전에는 TOSS 카드가 없고, S10–S13에는 한 장만 존재해야 한다. 타는 곳 패널의 크기와 설치 위치가 컷마다 변하지 않아야 한다. S12·S13 오른팔과 왼손목 시계를 어깨부터 손까지 추적 가능해야 한다.

- [ ] **Step 5: 후반부 커밋**

    git add edit/storyboard_gpt2/frames/raw/S07.png edit/storyboard_gpt2/frames/raw/S09.png edit/storyboard_gpt2/frames/raw/S10.png edit/storyboard_gpt2/frames/raw/S11.png edit/storyboard_gpt2/frames/raw/S12.png edit/storyboard_gpt2/frames/raw/S13.png
    git commit -m "feat: unify cast and gate-hall continuity"

### Task 6: Normalize, Document, Sync and Publish

**Files:**
- Modify: edit/storyboard_gpt2/frames/final/S01.png–S13.png
- Modify: edit/storyboard_gpt2/review/contact-sheet.png
- Modify: edit/storyboard_gpt2/review/qa-report.md
- Modify: edit/storyboard_gpt2/review/video-prompt-spec.md
- Modify: edit/storyboard_gpt2/storyboard-manifest.json
- Modify: README.md

**Interfaces:**
- Consumes: 승인된 raw S01–S13
- Produces: 최종 13컷, 콘택트시트, QA, 원본 프로젝트 동기화와 GitHub Draft PR

- [ ] **Step 1: 최종 프레임과 콘택트시트 재생성**

    python edit/storyboard_gpt2/tools/prepare_storyboard.py --raw edit/storyboard_gpt2/frames/raw --final edit/storyboard_gpt2/frames/final --sheet edit/storyboard_gpt2/review/contact-sheet.png

- [ ] **Step 2: 문서와 매니페스트 갱신**

    A05·A06 경로, S03/S04 두 번 실패, S02 완전 후면, 제공 인물 고정, S12/S13 오른손 태그를 QA와 영상 프롬프트에 기록한다.

- [ ] **Step 3: 자동 검증**

    python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q

    Expected: 1 passed

    Pillow 검증은 final/S01.png부터 S13.png까지 정확히 13장, 각 1080×1920 RGB, contact-sheet.png 1488×2688, 매니페스트 13개 qa=pass를 확인한다.

- [ ] **Step 4: 시각 검수**

    콘택트시트와 S02, S04, S06, S08, S12, S13을 원본 크기로 열어 설계 문서의 공간·인물·제품 QA를 대조한다.

- [ ] **Step 5: 원본 프로젝트 폴더 동기화**

    게시용 체크아웃에서 승인된 앵커, raw, final, review, prompts, manifest, README와 설계·계획 문서를 원본 프로젝트 폴더에 복사한다. 대표 파일 SHA-256이 양쪽에서 일치해야 한다.

- [ ] **Step 6: 최종 커밋과 푸시**

    git add README.md docs/superpowers edit/storyboard_gpt2
    git commit -m "feat: publish structure-aware storyboard revision"
    git push origin codex/publish-gpt-image-storyboard

- [ ] **Step 7: 원격 검증**

    로컬 HEAD와 git ls-remote의 브랜치 SHA가 같아야 한다. GitHub Draft PR에서 A05, A06, S02, S04, S12, S13, contact-sheet.png와 qa-report.md가 조회되어야 한다.
