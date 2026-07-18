# TOSS Three-Tap Referee Reveal and Open-Gate Ending Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 세 번의 실패 태그, 풋살화에서 얼굴로 올라가는 심판 붐업, 관광객 없는 심판 전신컷과 완전히 열린 카피 안전형 엔딩을 기존 S01–S13 번호 체계에 추가한다.

**Architecture:** 메인 프레임 S01–S13은 유지하고, 반복과 카메라 이동을 제어하는 S03A·S03B·S05A·S05B는 별도 보조 프레임으로 관리한다. GPT Image로 각 기준 프레임을 생성한 뒤 Pillow 준비 도구가 메인 13장과 보조 4장을 1080×1920 RGB로 정규화하고, 기존 콘택트시트 하단에 보조 프레임 한 줄을 추가한다.

**Tech Stack:** built-in GPT Image, Python 3, Pillow, pytest, PowerShell, Git, GitHub CLI

## Global Constraints

- 실패 태그는 첫 시도와 두 번의 재시도, 총 세 번만 발생한다.
- 모든 실패 태그는 관광객의 오른손과 동일한 무광 회색 일반 카드다.
- S03B와 S04에서 관광객은 카메라를 보지 않고 카드·리더 접점을 내려다본다.
- S05A에서 S05B로의 카메라 이동은 줌이 아니라 신발 높이에서 얼굴 높이로 실제 상승하는 붐업이다.
- S05와 S06에는 관광객, 캐리어, 관광객의 실루엣이 전혀 없어야 한다.
- S06은 심판의 머리부터 검은 풋살화까지 전신이 잘리지 않아야 한다.
- S13 관광객 차로의 좌우 검은 플랩은 게이트 본체 안으로 완전히 수납한다.
- S13 인물은 하단 60–65%에, 카피 안전영역은 상단 30–35%에 둔다.
- S13 심판은 화면 오른쪽에서 시계 없는 오른손으로 TOSS 카드를 태그하고, 검은 시계가 찬 왼팔은 아래에 둔다.
- 이미지 안에 자막·말풍선·효과음 글자를 생성하지 않는다.

---

### Task 1: Auxiliary Frame Normalization and Contact-Sheet Support

**Files:**
- Modify: `edit/storyboard_gpt2/tools/prepare_storyboard.py`
- Modify: `edit/storyboard_gpt2/tests/test_prepare_storyboard.py`
- Create: `edit/storyboard_gpt2/frames/auxiliary/.gitkeep`

**Interfaces:**
- Consumes: main raw directory with `S01.png`–`S13.png`; optional auxiliary raw directory with `S03A.png`, `S03B.png`, `S05A.png`, `S05B.png`
- Produces: `prepare_all(raw_dir, final_dir, sheet_path, auxiliary_raw_dir=None, auxiliary_final_dir=None) -> None`; normalized auxiliary PNGs; 1488×3354 combined contact sheet when auxiliary inputs exist

- [ ] **Step 1: Write failing auxiliary-frame tests**

Add a second test and strengthen the original test:

```python
import pytest


def make_main_frames(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    raw.mkdir()
    for index in range(1, 14):
        Image.new("RGB", (1200, 1600), (index * 10, 20, 30)).save(
            raw / f"S{index:02}.png"
        )
    return raw


def test_prepare_all_keeps_legacy_sheet_without_auxiliary(tmp_path: Path) -> None:
    raw = make_main_frames(tmp_path)
    final = tmp_path / "final"
    sheet = tmp_path / "contact-sheet.png"
    prepare_all(raw, final, sheet)
    assert Image.open(sheet).size == (1488, 2688)


def test_prepare_all_normalizes_four_auxiliary_frames_and_extends_sheet(
    tmp_path: Path,
) -> None:
    raw = make_main_frames(tmp_path)
    auxiliary_raw = tmp_path / "auxiliary-raw"
    auxiliary_raw.mkdir()
    for name in ("S03A.png", "S03B.png", "S05A.png", "S05B.png"):
        Image.new("RGB", (1600, 1200), (60, 80, 100)).save(auxiliary_raw / name)
    final = tmp_path / "final"
    auxiliary_final = tmp_path / "auxiliary-final"
    sheet = tmp_path / "contact-sheet.png"

    prepare_all(raw, final, sheet, auxiliary_raw, auxiliary_final)

    assert sorted(path.name for path in auxiliary_final.glob("*.png")) == [
        "S03A.png", "S03B.png", "S05A.png", "S05B.png"
    ]
    assert all(
        Image.open(path).size == (1080, 1920)
        for path in auxiliary_final.glob("*.png")
    )
    assert Image.open(sheet).size == (1488, 3354)


def test_prepare_all_rejects_one_sided_auxiliary_configuration(
    tmp_path: Path,
) -> None:
    raw = make_main_frames(tmp_path)
    with pytest.raises(ValueError, match="auxiliary raw and final directories"):
        prepare_all(
            raw,
            tmp_path / "final",
            tmp_path / "contact-sheet.png",
            tmp_path / "auxiliary-raw",
            None,
        )
```

- [ ] **Step 2: Run tests and confirm the new interface fails**

Run:

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

Expected: the legacy test passes and both new tests fail because `prepare_all` does not accept the two auxiliary arguments.

- [ ] **Step 3: Implement the auxiliary interface**

Add constants and optional parameters:

```python
AUXILIARY_NAMES = ("S03A.png", "S03B.png", "S05A.png", "S05B.png")
LEGACY_SHEET_SIZE = (1488, 2688)
EXTENDED_SHEET_SIZE = (1488, 3354)


def prepare_all(
    raw_dir: Path,
    final_dir: Path,
    sheet_path: Path,
    auxiliary_raw_dir: Path | None = None,
    auxiliary_final_dir: Path | None = None,
) -> None:
```

When both auxiliary arguments are supplied, require all four names, normalize them to 1080×1920 RGB, append them at `y=2688`, and create a 1488×3354 sheet. When neither is supplied, preserve the existing 1488×2688 behavior. Raise `ValueError` if only one auxiliary argument is supplied.

Add CLI arguments:

```python
parser.add_argument("--aux-raw", type=Path)
parser.add_argument("--aux-final", type=Path)
```

- [ ] **Step 4: Run tests and verify both modes pass**

Run:

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

Expected: `3 passed`.

- [ ] **Step 5: Commit normalization support**

```powershell
git add edit/storyboard_gpt2/tools/prepare_storyboard.py edit/storyboard_gpt2/tests/test_prepare_storyboard.py edit/storyboard_gpt2/frames/auxiliary/.gitkeep
git commit -m "feat: support auxiliary storyboard control frames"
```

### Task 2: Prompt and Continuity Locks

**Files:**
- Modify: `edit/storyboard_gpt2/prompts/prompt-pack.md`
- Modify: `edit/storyboard_gpt2/continuity-bible.md`

**Interfaces:**
- Consumes: approved design, A05, A06, `tourist_lock_JP_v2.jpg`, `referee_lock_A.png`, exact TOSS card PNG
- Produces: exact prompts and negative locks used by Tasks 3–5

- [ ] **Step 1: Replace the failure-sequence prompt blocks**

Record these exact story roles:

```text
S02 = first failed tap, strict rear wide, ordinary gray card, right hand
S03A = second failed tap, 45-degree high angle, small wrist correction
S03B = third failed tap, reader-level 28–35mm bottom view, card and hand foreground
S04 = face reaction only, 70–85mm, gaze remains down at card-reader contact
```

Every prompt must include: `same matte-gray unbranded card`, `no TOSS card`, `no camera eye contact`, and `no extra attempt`.

- [ ] **Step 2: Add S05A, S05B and S06 locks**

Record:

```text
S05A = black futsal boots and black football socks, floor-level start, referee only
S05B = same referee and vertical body axis, whistle at mouth, stern face, referee only
S06 = 35–50mm full-body referee in A06, head and boots visible, no tourist silhouette
```

- [ ] **Step 3: Strengthen the S13 ending lock**

Require `both black gate flaps fully retracted inside the housings`, `clear walking and suitcase path`, `upper 30–35 percent quiet copy-safe area`, `actors below 65 percent`, `right-hand card tag`, and `left-wrist watch down`.

- [ ] **Step 4: Validate prompt coverage**

Run:

```powershell
rg -n "S03A|S03B|S05A|S05B|three failed taps|fully retracted|30–35" edit/storyboard_gpt2/prompts/prompt-pack.md edit/storyboard_gpt2/continuity-bible.md
```

Expected: every search term appears in at least one of the two files and no line states that S04 is the second and final attempt.

- [ ] **Step 5: Commit prompt locks**

```powershell
git add edit/storyboard_gpt2/prompts/prompt-pack.md edit/storyboard_gpt2/continuity-bible.md
git commit -m "docs: lock three-tap and open-gate continuity"
```

### Task 3: Three-Tap Failure Sequence Generation

**Files:**
- Modify: `edit/storyboard_gpt2/frames/raw/S02.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S03.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S04.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/raw/S03A.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/raw/S03B.png`

**Interfaces:**
- Consumes: A05, current S02–S04, exact tourist lock, prompt blocks from Task 2
- Produces: first attempt main S02, second attempt main S03/S03A, third attempt S03B, reaction main S04

- [ ] **Step 1: Generate S02 first-attempt rear wide**

Use built-in GPT Image in edit mode with A05, current S02 and the tourist lock. Preserve the strict rear identity, grounded suitcase and physical `타는 곳 / Tracks` panel. Show her right hand placing one ordinary matte-gray card on the reader at the first failure moment with a red X. Do not show face, cheek, TOSS colors, product logo or a second card.

- [ ] **Step 2: Generate S03A second-attempt high angle**

Use the approved S02 result, A05 and the tourist lock. Frame a 45-degree high angle over the right shoulder. The same right hand and gray card return after a 3–5cm reset with a slightly more careful wrist alignment. Show the second red X. Copy the selected result to both `frames/raw/S03.png` and `frames/auxiliary/raw/S03A.png`.

- [ ] **Step 3: Generate S03B third-attempt bottom view**

Use S03A, A05 and the exact tourist lock. Place the reader and gray card in the large lower foreground and her exact face above. Her eyes must point to the physical card-reader contact, not the lens. Capture the short final tap and red X. Save only as `frames/auxiliary/raw/S03B.png`.

- [ ] **Step 4: Generate S04 reaction close-up**

Use S03B and the exact tourist lock. Create a 70–85mm close-up with the face filling the middle of the portrait frame. Eyes remain down at the off-screen card-reader contact, eyebrows gather minimally and lips part slightly. No card, referee, TOSS product, speech bubble, text or camera eye contact.

- [ ] **Step 5: Inspect the four failure assets together**

Open S02, S03A, S03B and S04 at original detail. Verify the same tourist, white blouse, beige bag, right hand, same gray card and increasing shot proximity. Reject any candidate with lens eye contact, left-hand tap, extra card or TOSS branding.

- [ ] **Step 6: Commit the failure sequence**

```powershell
git add edit/storyboard_gpt2/frames/raw/S02.png edit/storyboard_gpt2/frames/raw/S03.png edit/storyboard_gpt2/frames/raw/S04.png edit/storyboard_gpt2/frames/auxiliary/raw/S03A.png edit/storyboard_gpt2/frames/auxiliary/raw/S03B.png
git commit -m "feat: stage three distinct failed tap beats"
```

### Task 4: Referee Boom-Up Controls and Solo Full-Body Frame

**Files:**
- Modify: `edit/storyboard_gpt2/frames/raw/S05.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S06.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/raw/S05A.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/raw/S05B.png`

**Interfaces:**
- Consumes: A06, exact referee lock, S05A/S05B/S06 prompts from Task 2
- Produces: matched vertical start/end controls for the boom-up and a separate tourist-free full-body shot

- [ ] **Step 1: Generate S05A shoe-level start frame**

Use A06 and the referee lock. Create a floor-level 35–50mm frame centered on both black futsal boots planted on the subway floor. Include black football socks and the lower edge of black shorts so the vertical body axis is unambiguous. Match floor grout, light direction and contact shadow. No tourist, suitcase, gate, card or stadium.

- [ ] **Step 2: Generate S05B face-level end frame**

Use S05A, A06 and the referee lock. Preserve the same stance, body axis, clothing and light at the end of a vertical boom-up. Frame his stern face with the whistle naturally at his mouth and striped shoulders visible. No tourist, suitcase, gate, card, radial graphic or stadium.

- [ ] **Step 3: Promote S05 controls**

Save S05A and S05B to the auxiliary raw paths. Copy S05B to `frames/raw/S05.png` as the main cut endpoint.

- [ ] **Step 4: Generate S06 tourist-free full body**

Use A06 and the referee lock. Create a 35–50mm full-body portrait frame with the referee alone, slightly screen-right, head and both futsal boots fully visible. He lowers the whistle and begins one deliberate step with natural opposite arm/leg motion and grounded shadow. No tourist head, shoulder, blur, silhouette, suitcase, gate, TOSS card or effect.

- [ ] **Step 5: Inspect S05A, S05B and S06 together**

Confirm identical referee face, shorts, socks, boots, left-wrist watch and A06 light. Confirm S05 endpoints share one vertical axis and S06 includes no tourist pixels or foreground obstruction.

- [ ] **Step 6: Commit referee reveal assets**

```powershell
git add edit/storyboard_gpt2/frames/raw/S05.png edit/storyboard_gpt2/frames/raw/S06.png edit/storyboard_gpt2/frames/auxiliary/raw/S05A.png edit/storyboard_gpt2/frames/auxiliary/raw/S05B.png
git commit -m "feat: add referee boom-up and solo reveal controls"
```

### Task 5: Open-Gate Copy-Safe Ending

**Files:**
- Modify: `edit/storyboard_gpt2/frames/raw/S13.png`

**Interfaces:**
- Consumes: A05, approved S12, exact tourist and referee locks, exact TOSS card PNG
- Produces: upper-safe ending with a physically unobstructed tourist lane

- [ ] **Step 1: Generate the pulled-back ending**

Use A05, S12, current S13, both character locks and the exact product PNG. Create a 28–35mm portrait wide shot. Keep tourist and referee below 65% of frame height. Leave the upper-left 30–35% quiet for later Japanese copy; move the physical `타는 곳 / Tracks` panel smaller and farther into the upper-right or top-center edge.

- [ ] **Step 2: Lock gate and hand geometry**

The tourist lane must be fully open: both black rectangular flaps are physically retracted inside the two metal housings and no black panel crosses the walking lane or suitcase path. The tourist walks through with the suitcase rolling behind. The referee remains screen-right, taps one exact TOSS card with his right hand and keeps the black watch on his lowered left wrist.

- [ ] **Step 3: Inspect the ending at original detail**

Verify a continuous empty floor path from the tourist's leading foot through the lane and for every suitcase wheel. Verify the upper safe area contains no face, hand, card, sign overlap, pseudo-text or bright display. Trace the referee's right shoulder to the card and the left arm to the watch.

- [ ] **Step 4: Commit the ending**

```powershell
git add edit/storyboard_gpt2/frames/raw/S13.png
git commit -m "feat: open final gate and reserve ending copy space"
```

### Task 6: Normalize, Document, Sync and Publish

**Files:**
- Modify: `edit/storyboard_gpt2/frames/final/S02.png`–`S06.png`
- Modify: `edit/storyboard_gpt2/frames/final/S13.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/S03A.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/S03B.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/S05A.png`
- Create: `edit/storyboard_gpt2/frames/auxiliary/S05B.png`
- Modify: `edit/storyboard_gpt2/review/contact-sheet.png`
- Modify: `edit/storyboard_gpt2/review/qa-report.md`
- Modify: `edit/storyboard_gpt2/review/video-prompt-spec.md`
- Modify: `edit/storyboard_gpt2/storyboard-manifest.json`
- Modify: `README.md`

**Interfaces:**
- Consumes: approved raw main and auxiliary frames, Task 1 normalizer
- Produces: normalized delivery, combined review sheet, manifest, video prompts, original-workspace sync and updated GitHub Draft PR

- [ ] **Step 1: Normalize all assets and build the extended contact sheet**

Run:

```powershell
python edit/storyboard_gpt2/tools/prepare_storyboard.py `
  --raw edit/storyboard_gpt2/frames/raw `
  --final edit/storyboard_gpt2/frames/final `
  --aux-raw edit/storyboard_gpt2/frames/auxiliary/raw `
  --aux-final edit/storyboard_gpt2/frames/auxiliary `
  --sheet edit/storyboard_gpt2/review/contact-sheet.png
```

Expected: 13 main PNGs and 4 auxiliary PNGs at 1080×1920 RGB; combined contact sheet at 1488×3354 RGB.

- [ ] **Step 2: Update manifest metadata**

Set `runtime_seconds` to `19.0`. Record S02 as `failure_attempt: 1`, S03 as `failure_attempt: 2`, and S04 as `action: reaction_after_attempt_3`. Add:

```json
"auxiliary_shots": [
  {"id":"S03A","role":"failure_attempt_2","attempt_index":2,"framing":"high_angle","gaze":"card_reader_contact"},
  {"id":"S03B","role":"failure_attempt_3","attempt_index":3,"framing":"reader_level_bottom_view","gaze":"card_reader_contact"},
  {"id":"S05A","role":"boom_up_start","camera_move":"boom_up","subject":"referee_only"},
  {"id":"S05B","role":"boom_up_end","camera_move":"boom_up","subject":"referee_only"}
]
```

Set S05 `camera_move: boom_up`, S06 `subject: referee_only`, and S13 `gate_state: fully_open_flaps_retracted`, `copy_safe_top_percent: 35`.

- [ ] **Step 3: Update review documentation**

The video prompt must describe three separate `삐빅` beats with decreasing durations, S05's 1.2–1.5 second vertical boom-up, S06's tourist-free full body and S13's fully retracted flaps. The QA report must include PASS rows for S03A, S03B, S05A and S05B and report the new 1488×3354 sheet size.

- [ ] **Step 4: Update README links**

Add clickable links to the combined contact sheet, S03B, S05A, S05B, S06, S13, the approved design and this plan. State that main numbering remains S01–S13 and four auxiliary control frames were added.

- [ ] **Step 5: Run automated verification**

Run:

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

Expected: `3 passed`.

Run a Pillow/JSON assertion that checks exactly 13 main frames and 4 auxiliary frames, all 1080×1920 RGB, one 1488×3354 RGB sheet, `runtime_seconds == 19.0`, auxiliary attempt indices 2 and 3, S06 `referee_only`, and S13 `fully_open_flaps_retracted`.

- [ ] **Step 6: Perform visual verification**

Open the combined sheet and S02, S03A, S03B, S04, S05A, S05B, S06 and S13 at original detail. Check every requirement in the approved design. Regenerate only the failing frame and repeat normalization if any hand, gaze, shoe, tourist exclusion, flap or safe-area check fails.

- [ ] **Step 7: Sync to the original workspace**

Copy the approved prompts, continuity bible, main raw/final frames, auxiliary raw sources and normalized auxiliary frames, review files, manifest, README, design and plan from `AI-video---toss-card--publish` into `Toss foreigner Bridge Crew` without deleting unrelated user files. Compare SHA-256 for the contact sheet, S03B, S05A, S06, S13 and video prompt.

- [ ] **Step 8: Commit and push**

```powershell
git add README.md docs/superpowers edit/storyboard_gpt2
git commit -m "feat: publish three-tap referee reveal revision"
git push origin codex/publish-gpt-image-storyboard
```

- [ ] **Step 9: Verify GitHub publication**

Require local HEAD to equal `git ls-remote origin refs/heads/codex/publish-gpt-image-storyboard`. Verify Draft PR 1 is open and remotely serves S03B, S05A, S05B, S06, S13, the extended contact sheet, QA report, approved design and this plan.
