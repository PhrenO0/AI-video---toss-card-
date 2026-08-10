# TOSS Right-Axis Japanese Cast Storyboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the tourist with the user-provided Photo 1 identity, establish a coherent right-side subway concourse for S06/S08, and correct S12 to an unambiguous referee right-hand tag.

**Architecture:** Preserve the existing 13-shot timeline and file contract. Add one immutable tourist identity source and one new spatial anchor A04, then edit only the anchors and shots that consume those sources. Promote approved built-in GPT Image outputs into the existing raw paths, rebuild final frames and the contact sheet with the existing preparation script, then update visual QA documents and the open GitHub Draft PR.

**Tech Stack:** Built-in GPT Image (`image_gen`), local image inspection (`view_image`), Python 3, Pillow, pytest, Git, GitHub CLI.

## Global Constraints

- Final frames remain 9:16, 1080×1920, RGB PNG.
- The final tourist identity is the user-provided `Photo 1.jpg`; no national stereotypes, flags, or costume shorthand.
- Tourist wardrobe/props remain white loose blouse, light-blue jeans, beige crossbody bag, beige flats, and one silver hard-shell suitcase.
- Referee identity and uniform remain locked to `edit/generated/stills/referee_lock_A.png`.
- Referee black watch is always on the left wrist; card actions are always performed with the right hand.
- A04 is the view obtained by turning approximately 90° right from the front-gate viewpoint; S06 and S08 share it.
- No gate row, large `타는 곳` sign, or front-gate vanishing point may appear in S06/S08.
- The exact product source is `260702_토스_선불카드_애셋_모음집/pre-card-hologram-front (1).png`.
- S01–S09 contain no TOSS card; product reveal begins at S10.
- No generated captions, ad copy, speech bubbles, watermarks, or Japanese sound-effect typography.
- Existing frames may be replaced because the user explicitly requested replacement; Git history preserves the prior version.

---

### Task 1: Lock the new tourist identity source

**Files:**
- Create: `edit/generated/stills/tourist_lock_JP_v2.jpg`
- Create: `edit/generated/stills/tourist_lock_JP_v2.md`

**Interfaces:**
- Consumes: user attachment `Photo 1.jpg`.
- Produces: exact identity source `tourist_lock_JP_v2.jpg` referenced by every tourist edit; the companion Markdown records immutable traits.

- [ ] **Step 1: Inspect the user attachment at original detail**

Use `view_image` and verify five consistent views: left profile, two three-quarter/front variants, front, and rear.

- [ ] **Step 2: Copy the attachment without recompression**

Copy the exact JPEG into `edit/generated/stills/tourist_lock_JP_v2.jpg`. Do not synthesize a different face for the identity master.

- [ ] **Step 3: Record the identity invariants**

Create `tourist_lock_JP_v2.md` with: straight dark-brown shoulder-length hair, light full bangs, small natural smile at rest, restrained natural makeup, white loose blouse, beige crossbody bag, light-blue jeans, beige flats, silver suitcase, and a ban on changing hair length or facial proportions.

- [ ] **Step 4: Validate source integrity**

Run a file hash and image-dimension comparison between the attachment and copied identity master. Expected: identical SHA-256 and identical dimensions.

- [ ] **Step 5: Commit the identity source**

Commit only the two new identity-lock files with message `feat: lock Japanese tourist identity source`.

### Task 2: Create the right-side concourse master A04

**Files:**
- Create: `edit/storyboard_gpt2/anchors/A04_right_concourse_master.png`
- Modify: `edit/storyboard_gpt2/continuity-bible.md`

**Interfaces:**
- Consumes: A01 for architecture/material continuity; A02 for camera origin; no characters.
- Produces: empty 9:16 side-concourse anchor consumed by S06 and S08.

- [ ] **Step 1: Inspect A01 and A02 at original detail**

Verify gray tile module, blue wayfinding system, ceiling fixture spacing, floor reflectance, and neutral-cool exposure.

- [ ] **Step 2: Generate the empty A04 master with built-in GPT Image**

Use this prompt:

```text
Use case: ads-marketing.
Asset type: 9:16 photorealistic Korean subway location master.
Input images: A01 is the exact architecture, materials, lighting and color reference; A02 establishes the camera origin at G3.
Primary request: rotate the lens approximately 90 degrees to the right from the front-facing gate viewpoint and show the side concourse that logically connects to the same station.
Scene: long clean Seoul subway side corridor, gray tiled columns and walls, glossy gray floor, repeated neutral-white ceiling lights, blue route and exit boards, one wall map, distant corridor depth for a person to approach from 6–8 meters.
Composition: empty corridor, centered walkable axis, eye height 1.55 meters, 35 mm lens, generous vertical headroom.
Constraints: same station and color grade as A01; no people; no referee; no tourist; no card.
Avoid: any fare gates, repeated gate cabinets, large Tracks sign, front-gate vanishing point, stairs blocking the path, text overlays, logos, watermarks.
```

- [ ] **Step 3: Inspect and iterate once if necessary**

Pass only if the frame is recognizably the same station but unmistakably a different right-facing direction and contains no gate hardware.

- [ ] **Step 4: Save and document A04**

Copy the selected generated PNG to the anchor path. Add A04 geography, lens, lighting, and exclusions to the continuity bible.

- [ ] **Step 5: Commit A04**

Commit A04 and the continuity-bible update with message `feat: add right-side subway concourse anchor`.

### Task 3: Rebuild S06 and S08 on the A04 axis

**Files:**
- Modify: `edit/storyboard_gpt2/frames/raw/S06.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S08.png`
- Modify: `edit/storyboard_gpt2/prompts/prompt-pack.md`

**Interfaces:**
- Consumes: `A04_right_concourse_master.png`, `tourist_lock_JP_v2.jpg`, `referee_lock_A.png`, old S06/S08 for timing intent.
- Produces: two raw frames with a continuous approach vector and no gate background.

- [ ] **Step 1: Generate S06 over-the-shoulder reveal**

```text
Use case: ads-marketing identity-preserve edit.
Edit target: current S06 supplies only story timing; replace its camera angle and background.
Identity references: Photo 1 is the exact tourist; referee_lock_A is the exact referee.
Environment reference: A04 is mandatory and must remain recognizable.
Composition: camera behind and slightly left of the tourist; her new hair, rear head and left shoulder occupy the left foreground 20–25%, softly out of focus. Six to eight meters away, the referee stands slightly screen-right and takes his first deliberate step toward her while looking at her. Focus on referee. 35–50 mm natural perspective.
Constraints: same uniform, whistle, left-wrist black watch; tourist white blouse and beige bag edge visible.
Avoid: fare gates, Tracks sign, front-facing gate hall, TOSS card, captions, extra people, mirrored bodies.
```

- [ ] **Step 2: Validate S06**

Pass only if the tourist foreground establishes her gaze and the referee clearly walks toward her rather than toward an abstract camera.

- [ ] **Step 3: Generate S08 approach continuation**

```text
Use case: ads-marketing identity-preserve edit.
Edit target: current S08 supplies referee stride and stern tone only; replace its gate background.
Identity references: Photo 1 is the exact tourist; referee_lock_A is the exact referee.
Environment reference: A04 is mandatory; S06 establishes the approach axis.
Composition: same corridor and direction as S06, camera 10–15% closer and slightly lower. Referee takes a large mid-stride step toward the tourist, full body and both shoes visible, stern deadpan face. The tourist's blurred rear-hair edge and left shoulder occupy no more than 8% of the left frame.
Constraints: left-wrist black watch, centered whistle, natural arm swing, 50 mm lens.
Avoid: fare gates, Tracks sign, front-gate background, fashion-runway symmetry, TOSS card, captions, duplicated limbs.
```

- [ ] **Step 4: Validate S06/S08 as a pair**

Inspect side by side. Floor lines, column order, light rhythm, approach direction, referee identity, and tourist foreground side must match.

- [ ] **Step 5: Promote and document**

Copy selected outputs to raw S06/S08 and replace their prompt sections with the final prompts.

- [ ] **Step 6: Commit the spatial sequence**

Commit S06, S08 and prompt-pack changes with message `feat: rebuild referee approach on right concourse`.

### Task 4: Correct S12 right-hand ownership

**Files:**
- Modify: `edit/storyboard_gpt2/frames/raw/S12.png`
- Modify: `edit/storyboard_gpt2/prompts/prompt-pack.md`

**Interfaces:**
- Consumes: current S12 reader geometry; referee lock; exact TOSS card source; corrected S13 for screen-side relationship.
- Produces: unambiguous raw S12 success tag.

- [ ] **Step 1: Generate the corrected S12**

```text
Use case: ads-marketing precise-object edit.
Edit target: current S12 supplies the reader design and success state, but its hand ownership is wrong.
Identity reference: referee_lock_A.
Product reference: exact TOSS hologram-front PNG.
Composition: three-quarter medium close-up. Contactless reader occupies screen-left; referee torso is partially visible on screen-right. His watch-free RIGHT arm reaches from his screen-right body toward screen-left and his RIGHT hand taps one exact TOSS card flat on the green reader. His LEFT arm hangs beside his torso; the black watch is clearly visible on the lowered LEFT wrist at the right edge.
Constraints: one card, one reader, natural five-finger anatomy, green success ring, card artwork undistorted.
Avoid: watch on card hand, left-hand tag, mirrored anatomy, cropped arm ownership, duplicate card or hand, text overlays.
```

- [ ] **Step 2: Validate anatomy before promotion**

Trace both arms from shoulder to wrist. Pass only if the card arm originates at the referee's right shoulder and contains no watch, while the lowered left wrist contains the black watch.

- [ ] **Step 3: Promote and document**

Copy the selected result to raw S12 and update its prompt section.

- [ ] **Step 4: Commit S12**

Commit the raw frame and prompt update with message `fix: correct referee right-hand tag in S12`.

### Task 5: Replace the tourist across all consuming anchors and shots

**Files:**
- Modify: `edit/storyboard_gpt2/anchors/A02_tourist_gate_master.png`
- Modify: `edit/storyboard_gpt2/anchors/A03_referee_gate_master.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S02.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S03.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S04.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S07.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S09.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S10.png`
- Modify: `edit/storyboard_gpt2/frames/raw/S13.png`
- Modify: `edit/storyboard_gpt2/prompts/prompt-pack.md`

**Interfaces:**
- Consumes: exact `tourist_lock_JP_v2.jpg`, A01/A02/A03 geometry, existing raw frames for blocking, referee lock where visible.
- Produces: one coherent tourist identity while preserving every shot's action and product timing.

- [ ] **Step 1: Replace tourist identity in A02 and A03**

For each edit, state: change only tourist face, bangs, straight shoulder-length hair, and identity; preserve white blouse, light-blue jeans, beige crossbody, beige flats, silver suitcase, pose, hands, gate geometry, referee, lighting, and signage.

- [ ] **Step 2: Replace S02/S03/S04**

Use one edit call per frame. Preserve S02 entry/right-hand reach, S03 high-angle generic gray-card failure, and S04 downward gaze; ban TOSS branding in all three.

- [ ] **Step 3: Replace S07/S09**

Preserve S07 rightward surprised gaze and S09 respectful two-shot blocking; change only tourist identity and hair.

- [ ] **Step 4: Replace visible tourist portions in S10 and S13**

Preserve S10 card emergence, referee hand and effects. Preserve corrected S13 right-hand tag, open passage, referee screen-right, overhead Korean sign and upper copy space. Change only tourist identity/hair and matching wardrobe details.

- [ ] **Step 5: Cross-frame identity review**

Compare A02, S04, S07, S09 and S13 at face scale. Pass only if bangs, hair length, eyes, nose, jawline and age remain stable. Compare S02/S03/S06/S08/S10 rear and side hair silhouettes.

- [ ] **Step 6: Promote and document**

Copy only approved results to their raw/anchor paths and update prompt inputs to `tourist_lock_JP_v2.jpg`.

- [ ] **Step 7: Commit the recast**

Commit the identity master consumers with message `feat: recast tourist across storyboard`.

### Task 6: Rebuild finals, QA and delivery documents

**Files:**
- Modify: `edit/storyboard_gpt2/frames/final/S02.png`
- Modify: `edit/storyboard_gpt2/frames/final/S03.png`
- Modify: `edit/storyboard_gpt2/frames/final/S04.png`
- Modify: `edit/storyboard_gpt2/frames/final/S06.png`
- Modify: `edit/storyboard_gpt2/frames/final/S07.png`
- Modify: `edit/storyboard_gpt2/frames/final/S08.png`
- Modify: `edit/storyboard_gpt2/frames/final/S09.png`
- Modify: `edit/storyboard_gpt2/frames/final/S10.png`
- Modify: `edit/storyboard_gpt2/frames/final/S12.png`
- Modify: `edit/storyboard_gpt2/frames/final/S13.png`
- Modify: `edit/storyboard_gpt2/review/contact-sheet.png`
- Modify: `edit/storyboard_gpt2/review/qa-report.md`
- Modify: `edit/storyboard_gpt2/review/video-prompt-spec.md`
- Modify: `edit/storyboard_gpt2/storyboard-manifest.json`
- Modify: `README.md` in the publishing checkout.

**Interfaces:**
- Consumes: approved raw frames and anchors.
- Produces: normalized deliverables, documentation, and auditable PASS status.

- [ ] **Step 1: Run the existing preparation pipeline**

```powershell
python edit/storyboard_gpt2/tools/prepare_storyboard.py `
  --raw edit/storyboard_gpt2/frames/raw `
  --final edit/storyboard_gpt2/frames/final `
  --sheet edit/storyboard_gpt2/review/contact-sheet.png
```

Expected: command exits 0 and produces exactly S01–S13 finals.

- [ ] **Step 2: Inspect final S06/S08/S12 and the contact sheet**

Use original-detail inspection. Confirm right-axis geography, over-the-shoulder direction, right-hand tag, consistent tourist identity and no generated text.

- [ ] **Step 3: Update QA and video motion language**

Record A04, Photo 1 identity lock, S06/S08 continuity, and S12 shoulder-to-hand proof. Video prompts must preserve A04 across the two approach clips and forbid gate-background drift.

- [ ] **Step 4: Run automated verification**

```powershell
python -m pytest edit/storyboard_gpt2/tests/test_prepare_storyboard.py -q
```

Expected: `1 passed`.

Run a Pillow validation that asserts exactly 13 final files, each `(1080, 1920)` and `RGB`, contact sheet `(1488, 2688)`, manifest 13 shots, and all `qa` values `pass`.

- [ ] **Step 5: Commit final delivery**

Commit normalized finals and documentation with message `docs: finalize recast storyboard QA`.

### Task 7: Update the GitHub Draft PR

**Files:**
- Synchronize the changed project files into `C:/Users/jun12/Documents/📁 AI_프로젝트/AI-video---toss-card--publish`.

**Interfaces:**
- Consumes: verified local delivery.
- Produces: follow-up commit on `codex/publish-gpt-image-storyboard`, visible in Draft PR #1.

- [ ] **Step 1: Copy only changed production paths**

Synchronize identity lock, A04, anchors, raw/final frames, contact sheet, prompts, QA, manifest, spec and this implementation plan. Exclude `.pytest_cache`, `__pycache__`, `*.pyc`, and candidate images.

- [ ] **Step 2: Re-run tests in the publishing checkout**

Expected: pytest passes and the same dimension/manifest assertions succeed.

- [ ] **Step 3: Review and commit**

Review `git diff --stat` and stage only project-scoped files. Commit with message `feat: apply Japanese recast and right-axis storyboard fixes`.

- [ ] **Step 4: Push and verify remote objects**

Push `codex/publish-gpt-image-storyboard`, confirm Draft PR #1 remains open, and query remote A04, S06, S08 and S12 paths to verify their blob sizes and SHAs.
