# TOSS GPT Image Storyboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 13 continuity-locked, photorealistic 9:16 storyboard frames for the TOSS Japanese-tourist subway advertisement using Codex's built-in GPT Image tool.

**Architecture:** Use an anchor-first image pipeline: preserve the 13 hand sketches, generate one gate master and two blocking masters, then derive each shot as a separate image. Normalize accepted outputs to 1080×1920, validate continuity and product accuracy frame by frame, and assemble a labeled contact sheet plus a reusable video-prompt pack.

**Tech Stack:** Codex built-in GPT Image, local `view_image`, PowerShell, Python 3 with Pillow 10.1.0, Markdown, JSON.

## Global Constraints

- All new generated frames use the built-in GPT Image tool; Higgsfield must not generate or edit any storyboard frame.
- Final output contains exactly 13 separate portrait frames named `S01.png` through `S13.png`.
- Final frame size is exactly 1080×1920 RGB PNG.
- Locked identities: `edit/generated/stills/tourist_lock_A.png` and `edit/generated/stills/referee_lock_A.png`.
- Exact product source: `260702_토스_선불카드_애셋_모음집/pre-card-hologram-front (1).png`.
- Do not show the TOSS card before S10; use the exact card source from its first partial appearance in S10 through S13.
- Failure scenes keep the tourist and suitcase before the closed flap; success opens the flap only in S13.
- Do not burn dialogue, captions, station names, random signage, or the final copy into generated frames.
- Preserve G3 as the tourist gate, G4 as the referee's adjacent right-hand lane, and the G3 reader on the tourist's right.
- The final contact sheet must read without audio as `location → failure → whistle source → referee approach → card declaration → success → brand`.

---

## File Map

- `edit/storyboard_gpt2/source_sketches/S01.png` … `S13.png`: immutable copies of the 13 supplied hand sketches.
- `edit/storyboard_gpt2/continuity-bible.md`: reusable spatial, character, lighting, lens, and negative constraints.
- `edit/storyboard_gpt2/prompts/prompt-pack.md`: final anchor and shot prompts used with GPT Image.
- `edit/storyboard_gpt2/storyboard-manifest.json`: frame timing, source sketch, references, generated path, and QA status.
- `edit/storyboard_gpt2/anchors/A01_gate_master.png`: empty gate geography master.
- `edit/storyboard_gpt2/anchors/A02_tourist_gate_master.png`: tourist-at-G3 blocking master.
- `edit/storyboard_gpt2/anchors/A03_referee_gate_master.png`: referee-at-G4 blocking master.
- `edit/storyboard_gpt2/frames/raw/S01.png` … `S13.png`: accepted built-in GPT Image outputs before deterministic sizing.
- `edit/storyboard_gpt2/frames/final/S01.png` … `S13.png`: normalized 1080×1920 deliverables.
- `edit/storyboard_gpt2/tools/prepare_storyboard.py`: deterministic resize, validation, and contact-sheet builder.
- `edit/storyboard_gpt2/tests/test_prepare_storyboard.py`: Pillow utility tests.
- `edit/storyboard_gpt2/review/contact-sheet.png`: labeled 13-frame review sheet.
- `edit/storyboard_gpt2/review/qa-report.md`: pass/fail record and regeneration notes.
- `edit/storyboard_gpt2/review/video-prompt-spec.md`: motion, transition, gaze, and sound intent for each shot.

---

### Task 1: Preserve Sources and Lock the Production Manifest

**Files:**
- Create: `edit/storyboard_gpt2/source_sketches/S01.png` … `S13.png`
- Create: `edit/storyboard_gpt2/continuity-bible.md`
- Create: `edit/storyboard_gpt2/storyboard-manifest.json`

**Interfaces:**
- Consumes: the 13 supplied temp PNG files, the approved design spec, locked character images, and exact product PNG.
- Produces: stable source paths and a machine-readable list of all frames used by later tasks.

- [ ] **Step 1: Copy the 13 supplied sketches without modifying the originals**

Use `Copy-Item -LiteralPath` to map the images in message order to `S01.png` through `S13.png`. Verify with:

```powershell
(Get-ChildItem -LiteralPath 'edit/storyboard_gpt2/source_sketches' -Filter 'S*.png').Count
```

Expected: `13`.

- [ ] **Step 2: Write the continuity bible**

Include the exact G3/G4 coordinates, tourist and referee wardrobe, reader placement, failure/success flap state, lens progression, cool cyan-white station lighting, Japanese game-effect limitation to S10–S11, and the ban on generated text.

- [ ] **Step 3: Write the manifest**

Create a JSON object with `version`, `canvas`, `runtime_seconds`, `locked_assets`, and a `shots` array. Every shot entry must contain `id`, `start`, `end`, `sketch`, `raw`, `final`, `qa`, and `card_visibility`. Use `card_visibility: "none"` for S01–S09, `"partial_exact"` for S10, and `"full_exact"` for S11–S13.

- [ ] **Step 4: Validate the manifest and paths**

```powershell
python -c "import json, pathlib; p=pathlib.Path('edit/storyboard_gpt2/storyboard-manifest.json'); d=json.loads(p.read_text(encoding='utf-8')); assert len(d['shots'])==13; assert d['shots'][0]['id']=='S01'; assert d['shots'][-1]['id']=='S13'; print('manifest-ok')"
```

Expected: `manifest-ok`.

- [ ] **Step 5: Commit Task 1**

```powershell
git add -- 'edit/storyboard_gpt2/source_sketches' 'edit/storyboard_gpt2/continuity-bible.md' 'edit/storyboard_gpt2/storyboard-manifest.json'
git commit --only -m "chore: lock GPT storyboard sources and continuity" -- 'edit/storyboard_gpt2/source_sketches' 'edit/storyboard_gpt2/continuity-bible.md' 'edit/storyboard_gpt2/storyboard-manifest.json'
```

### Task 2: Write the Exact GPT Image Prompt Pack

**Files:**
- Create: `edit/storyboard_gpt2/prompts/prompt-pack.md`

**Interfaces:**
- Consumes: `continuity-bible.md`, `storyboard-manifest.json`, 13 source sketches, and three locked product/character assets.
- Produces: three anchor prompts and 13 individual shot prompts, each ready for one built-in GPT Image call.

- [ ] **Step 1: Write the shared prompt header**

Every prompt begins with:

```text
Use case: ads-marketing, sketch-to-render, identity-preserve
Asset type: 9:16 photorealistic keyframe for a premium Japanese TV commercial
Scene: a modern Seoul subway fare-gate hall, cool cyan-white fluorescent light, realistic stainless steel, glass and rubber surfaces
Continuity: G3 is the center tourist gate; G4 is the adjacent lane on screen-right; G3's contactless reader is on the tourist's right; preserve the supplied tourist and referee identities exactly
Style: live-action commercial photography, natural skin and fabric texture, subtle film grain, no glossy CGI look
Text constraint: no subtitles, dialogue, speech balloons, station names, logos, random letters, watermark, or UI text
```

- [ ] **Step 2: Write A01–A03 anchor prompts**

A01 specifies an empty frontal wide view with five physically plausible flap gates and an unobstructed G3/G4 map. A02 adds only the locked tourist before the closed G3 flap with her suitcase trailing behind-left. A03 preserves the same station and adds only the locked referee standing deadpan in G4 on the tourist's right.

- [ ] **Step 3: Write S01–S13 shot prompts**

Each prompt must label all inputs by role: hand sketch as composition reference; character sheet as identity reference; A01/A02/A03 as environment/blocking reference; exact TOSS PNG as supporting product insert only for S10–S13. Repeat the shot-specific gaze, hand, card, reader, flap, suitcase, lens, and negative constraints from the approved spec rather than referring to another prompt.

- [ ] **Step 4: Run a completeness scan**

```powershell
$p='edit/storyboard_gpt2/prompts/prompt-pack.md'
1..13 | ForEach-Object { $id='S{0:D2}' -f $_; if(-not (Select-String -Quiet -LiteralPath $p -Pattern "## $id")){ throw "missing $id" } }
'prompt-pack-ok'
```

Expected: `prompt-pack-ok`.

- [ ] **Step 5: Commit Task 2**

```powershell
git add -- 'edit/storyboard_gpt2/prompts/prompt-pack.md'
git commit --only -m "docs: add GPT storyboard prompt pack" -- 'edit/storyboard_gpt2/prompts/prompt-pack.md'
```

### Task 3: Generate and Approve the Three Spatial Anchors

**Files:**
- Create: `edit/storyboard_gpt2/anchors/A01_gate_master.png`
- Create: `edit/storyboard_gpt2/anchors/A02_tourist_gate_master.png`
- Create: `edit/storyboard_gpt2/anchors/A03_referee_gate_master.png`
- Modify: `edit/storyboard_gpt2/review/qa-report.md`

**Interfaces:**
- Consumes: A01–A03 prompts and locked character references.
- Produces: the only environment/blocking references allowed for S01–S13.

- [ ] **Step 1: Generate A01 with one built-in GPT Image call**

Use the A01 prompt with no Higgsfield media reference. Save the selected result from the built-in generated-images location to `anchors/A01_gate_master.png`.

- [ ] **Step 2: Inspect A01 at original detail**

Reject if five lanes are not readable, G3/G4 merge, a reader is floating, flaps are asymmetrical, or text/signage attracts attention. Regenerate A01 alone until it passes.

- [ ] **Step 3: Generate and inspect A02**

Use A01 as environment reference, the tourist sheet as identity reference, and sketch S02 as composition reference. Reject if the tourist is beyond the closed flap, suitcase is inside the gate, right-hand reader position changes, or wardrobe/face drifts.

- [ ] **Step 4: Generate and inspect A03**

Use A01 and A02 as spatial references, the referee sheet as identity reference, and sketch S06 as composition reference. Reject if the referee stands inside G3, appears on screen-left, changes uniform, smiles, or loses the whistle/watch.

- [ ] **Step 5: Record anchor QA**

Create `qa-report.md` with one row per anchor and the columns `Asset`, `Geometry`, `Identity`, `Hands`, `Text`, `Decision`, `Notes`. All three rows must read `PASS` before Task 4.

- [ ] **Step 6: Commit Task 3**

```powershell
git add -- 'edit/storyboard_gpt2/anchors' 'edit/storyboard_gpt2/review/qa-report.md'
git commit --only -m "feat: lock GPT storyboard spatial anchors" -- 'edit/storyboard_gpt2/anchors' 'edit/storyboard_gpt2/review/qa-report.md'
```

### Task 4: Generate Story Frames S01–S09

**Files:**
- Create: `edit/storyboard_gpt2/frames/raw/S01.png` … `S09.png`
- Modify: `edit/storyboard_gpt2/review/qa-report.md`
- Modify: `edit/storyboard_gpt2/storyboard-manifest.json`

**Interfaces:**
- Consumes: approved A01–A03, source sketches S01–S09, tourist/referee identity sheets, and exact prompts S01–S09.
- Produces: nine accepted pre-product story frames with no TOSS card visible.

- [ ] **Step 1: Generate S01 and S02 separately**

S01 uses A01 plus sketch S01. S02 uses A01, A02, tourist identity, and sketch S02. S01 and S02 must preserve the same camera height, gate spacing, and G3 position.

- [ ] **Step 2: Generate S03 and S04 separately**

S03 uses A02 and sketch S03 for the 45-degree high angle. It shows a generic matte gray transit card, the tourist's right hand on the G3 reader, the closed flap, and suitcase behind-left. S04 uses the tourist identity and A02; her gaze remains down at the hand/reader and not toward camera.

- [ ] **Step 3: Generate S05 and S06 separately**

S05 uses the referee identity and sketch S05 for a real black whistle held in the mouth. S06 uses A01–A03 and sketch S06; the referee stands in G4 on screen-right while the tourist remains at G3.

- [ ] **Step 4: Generate S07–S09 separately**

S07 locks the tourist gaze to screen-right. S08 shows the referee walking toward a low camera with a stern face and consistent uniform. S09 preserves the tourist framing and places the referee entering from screen-right toward screen-left without duplicated bodies or limbs.

- [ ] **Step 5: Inspect every frame and regenerate only failed frames**

Add S01–S09 rows to `qa-report.md`. Each row must pass `Geometry`, `Identity`, `Hands`, `Gaze`, `Card`, `Text`, and `Decision`. Set the corresponding manifest `qa` value to `pass` only after visual inspection with `view_image`.

- [ ] **Step 6: Verify product secrecy**

Manually confirm that S01–S09 contain no TOSS wordmark, blue holographic product card, or recognizable product back. The generic failure card in S03 must be matte gray and unbranded.

- [ ] **Step 7: Commit Task 4**

```powershell
git add -- 'edit/storyboard_gpt2/frames/raw' 'edit/storyboard_gpt2/review/qa-report.md' 'edit/storyboard_gpt2/storyboard-manifest.json'
git commit --only -m "feat: generate GPT storyboard setup and referee beats" -- 'edit/storyboard_gpt2/frames/raw' 'edit/storyboard_gpt2/review/qa-report.md' 'edit/storyboard_gpt2/storyboard-manifest.json'
```

### Task 5: Generate Product Frames S10–S13

**Files:**
- Create: `edit/storyboard_gpt2/frames/raw/S10.png` … `S13.png`
- Modify: `edit/storyboard_gpt2/review/qa-report.md`
- Modify: `edit/storyboard_gpt2/storyboard-manifest.json`

**Interfaces:**
- Consumes: approved anchors, S09 for blocking continuity, referee/tourist identities, exact TOSS card PNG, and prompts S10–S13.
- Produces: four accepted product-resolution frames with exact card identity.

- [ ] **Step 1: Generate S10**

Use S09, referee identity, sketch S10, and exact card PNG. Only the exact card's top corner emerges from the chest pocket. Add restrained blue-gold radial light around the pocket while preserving the live-action station background.

- [ ] **Step 2: Generate S11**

Use S10, referee identity, sketch S11, and exact card PNG. The referee holds one vertical card overhead with the front facing camera; his other arm remains down. Reject extra cards, mirrored logos, bent card shape, malformed fingers, or missing watch.

- [ ] **Step 3: Generate S12**

Use A02, S11, sketch S12, and exact card PNG. Frame the same right-side G3 reader and show the exact card face parallel to the reader surface in the referee's hand. Reject any tourist hand performing the successful tap.

- [ ] **Step 4: Generate S13**

Use A01–A03, S12, both identity sheets, sketch S13, and exact card PNG. Side profile: the G3 flap is open, the tourist and silver suitcase cross together, the referee remains deadpan beside the reader, and the upper-left region stays visually quiet for copy.

- [ ] **Step 5: Apply the exact product source when GPT redraws it**

If any card logo, chip, proportion, or gradient differs from the source, use the original PNG as a perspective-matched insert while retaining generated fingers, occlusion, lighting, and depth. Record `exact PNG insert` in that frame's QA notes.

- [ ] **Step 6: Inspect and approve S10–S13**

Add QA rows and set manifest status to `pass`. S10 is partial exact, S11–S13 are full exact. Confirm the card remains vertical and front-facing in S11, touches the correct G3 reader in S12, and does not duplicate in S13.

- [ ] **Step 7: Commit Task 5**

```powershell
git add -- 'edit/storyboard_gpt2/frames/raw' 'edit/storyboard_gpt2/review/qa-report.md' 'edit/storyboard_gpt2/storyboard-manifest.json'
git commit --only -m "feat: generate exact-product GPT storyboard beats" -- 'edit/storyboard_gpt2/frames/raw' 'edit/storyboard_gpt2/review/qa-report.md' 'edit/storyboard_gpt2/storyboard-manifest.json'
```

### Task 6: Normalize Frames and Build the Contact Sheet

**Files:**
- Create: `edit/storyboard_gpt2/tools/prepare_storyboard.py`
- Create: `edit/storyboard_gpt2/tests/test_prepare_storyboard.py`
- Create: `edit/storyboard_gpt2/frames/final/S01.png` … `S13.png`
- Create: `edit/storyboard_gpt2/review/contact-sheet.png`

**Interfaces:**
- Consumes: 13 accepted raw RGB images.
- Produces: 13 exact 1080×1920 files and one 4-column labeled contact sheet.

- [ ] **Step 1: Write the failing Pillow test**

```python
import importlib.util
from pathlib import Path
from PIL import Image

MODULE_PATH = Path(__file__).parents[1] / "tools" / "prepare_storyboard.py"
SPEC = importlib.util.spec_from_file_location("prepare_storyboard", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)
prepare_all = MODULE.prepare_all


def test_prepare_all_outputs_13_portrait_frames_and_contact_sheet(tmp_path: Path):
    raw = tmp_path / "raw"
    final = tmp_path / "final"
    raw.mkdir()
    for index in range(1, 14):
        Image.new("RGB", (1200, 1600), (index * 10, 20, 30)).save(raw / f"S{index:02}.png")
    sheet = tmp_path / "contact-sheet.png"
    prepare_all(raw, final, sheet)
    outputs = sorted(final.glob("S*.png"))
    assert len(outputs) == 13
    assert all(Image.open(path).size == (1080, 1920) for path in outputs)
    assert Image.open(sheet).size == (1488, 2688)
```

- [ ] **Step 2: Run the test and verify failure**

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -v
```

Expected: import failure because `prepare_storyboard.py` does not exist.

- [ ] **Step 3: Implement the utility**

```python
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

FRAME_SIZE = (1080, 1920)
THUMB_SIZE = (360, 640)
SHEET_SIZE = (1488, 2688)


def prepare_all(raw_dir: Path, final_dir: Path, sheet_path: Path) -> None:
    names = [f"S{index:02}.png" for index in range(1, 14)]
    missing = [name for name in names if not (raw_dir / name).is_file()]
    if missing:
        raise ValueError(f"missing frames: {', '.join(missing)}")
    final_dir.mkdir(parents=True, exist_ok=True)
    prepared = []
    for name in names:
        with Image.open(raw_dir / name) as source:
            frame = ImageOps.fit(source.convert("RGB"), FRAME_SIZE, Image.Resampling.LANCZOS)
            frame.save(final_dir / name, format="PNG", optimize=True)
            prepared.append((name, frame.copy()))
    sheet = Image.new("RGB", SHEET_SIZE, (18, 22, 28))
    draw = ImageDraw.Draw(sheet)
    for index, (name, frame) in enumerate(prepared):
        column = index % 4
        row = index // 4
        x = 24 + column * 366
        y = 24 + row * 666
        thumb = ImageOps.fit(frame, THUMB_SIZE, Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y + 22))
        draw.text((x, y), name.removesuffix(".png"), fill=(240, 244, 250))
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True, type=Path)
    parser.add_argument("--final", required=True, type=Path)
    parser.add_argument("--sheet", required=True, type=Path)
    args = parser.parse_args()
    prepare_all(args.raw, args.final, args.sheet)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the test and verify pass**

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -v
```

Expected: `1 passed`.

- [ ] **Step 5: Build project outputs**

```powershell
python edit/storyboard_gpt2/tools/prepare_storyboard.py --raw edit/storyboard_gpt2/frames/raw --final edit/storyboard_gpt2/frames/final --sheet edit/storyboard_gpt2/review/contact-sheet.png
```

Expected: 13 final PNG files and one contact sheet.

- [ ] **Step 6: Commit Task 6**

```powershell
git add -- 'edit/storyboard_gpt2/tools' 'edit/storyboard_gpt2/tests' 'edit/storyboard_gpt2/frames/final' 'edit/storyboard_gpt2/review/contact-sheet.png'
git commit --only -m "feat: normalize GPT storyboard and build contact sheet" -- 'edit/storyboard_gpt2/tools' 'edit/storyboard_gpt2/tests' 'edit/storyboard_gpt2/frames/final' 'edit/storyboard_gpt2/review/contact-sheet.png'
```

### Task 7: Final Visual QA and Video-Prompt Handoff

**Files:**
- Modify: `edit/storyboard_gpt2/review/qa-report.md`
- Create: `edit/storyboard_gpt2/review/video-prompt-spec.md`
- Modify: `edit/storyboard_gpt2/storyboard-manifest.json`

**Interfaces:**
- Consumes: 13 final frames, contact sheet, approved design spec, and exact timing table.
- Produces: an approved storyboard set and per-shot motion prompts ready for video generation.

- [ ] **Step 1: Inspect the contact sheet at original detail**

Confirm the sequence reads without audio and that station geometry, identities, wardrobe, suitcase, reader placement, gaze, referee direction, card reveal timing, and end-copy safe area remain coherent.

- [ ] **Step 2: Inspect S03, S05, S09, S11, S12, and S13 individually**

These are the highest-risk frames: hand-to-reader contact, whistle-in-mouth anatomy, two-character occlusion, overhead card grip, exact product-reader contact, and successful gate passage.

- [ ] **Step 3: Write the video prompt spec**

For every shot, include `duration`, `start frame`, `end action`, `camera`, `subject motion`, `gaze`, `transition`, `sound cue`, `overlay cue`, and `negative motion`. Preserve the 18.0-second master timing and specify Japanese game-style rays only for S10–S11.

- [ ] **Step 4: Close the QA report and manifest**

Set `overall_status` to `pass` only if all 13 frame rows pass. Record the exact final paths and prompt-pack path. Leave `overall_status` as `fail` if even one required frame is not accepted.

- [ ] **Step 5: Run final filesystem verification**

```powershell
python -c "from pathlib import Path; from PIL import Image; p=Path('edit/storyboard_gpt2/frames/final'); f=sorted(p.glob('S*.png')); assert len(f)==13; assert all(Image.open(x).size==(1080,1920) for x in f); assert Path('edit/storyboard_gpt2/review/contact-sheet.png').is_file(); print('storyboard-delivery-ok')"
```

Expected: `storyboard-delivery-ok`.

- [ ] **Step 6: Commit Task 7**

```powershell
git add -- 'edit/storyboard_gpt2/review' 'edit/storyboard_gpt2/storyboard-manifest.json'
git commit --only -m "docs: approve GPT storyboard and video prompt handoff" -- 'edit/storyboard_gpt2/review' 'edit/storyboard_gpt2/storyboard-manifest.json'
```

---

## Completion Evidence

- The workspace contains 13 accepted final PNG frames at 1080×1920.
- The contact sheet shows all 13 frames in order with no failed QA row.
- S01–S09 show no TOSS product card.
- S10–S13 use the exact TOSS product art with no mirrored or redrawn branding.
- The tourist remains before the flap on failure and crosses only after the successful S12 tap.
- The motion-prompt handoff preserves the approved 18-second rhythm and transition design.
