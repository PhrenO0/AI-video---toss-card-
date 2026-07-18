# TOSS Japan Tourist Reel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a polished 14.7-second, 1080×1920 Japanese-targeted TOSS prepaid transit-card advertisement from the approved storyboard using Higgsfield generation and exact local card assets.

**Architecture:** Lock character and location identity in still images first, animate seven simple action units with Seedance 2.0, then assemble them locally with exact card overlays, controlled Japanese typography, licensed sound effects, and frame-level QA. Higgsfield generation stays silent; all audio, text, product fidelity, timing, and final render are controlled in local post-production.

**Tech Stack:** Higgsfield MCP (`gpt_image_2`, `seedance_2_0_mini`, `seedance_2_0`), ffmpeg/ffprobe, PowerShell, PNG/APNG assets, Yu Gothic and Noto Sans CJK fonts.

## Global Constraints

- Final output: 1080×1920, 30fps, H.264 video, AAC 48kHz stereo audio, 14.2–14.9 seconds.
- Visual style: premium Japanese commercial from first frame to last; no smartphone reel, UGC, vlog, or handheld-phone aesthetic.
- No dialogue, voice-over, lip-sync, or spoken words.
- The first failed card is unbranded and must not resemble TOSS.
- The TOSS card first appears during the referee reveal and uses `pre-card-hologram-front (1).png` for every readable product view.
- Generated frames contain no text. Japanese SFX and final copy are composited locally after all visual overlays.
- Same whistle sample and exact rhythm are used for the gate misdirection and referee reveal; only spatial perspective changes.
- Tourist continuity: ivory blouse, light-blue straight jeans, beige crossbody bag, silver hard-shell carry-on, dark-brown wavy hair with airy bangs.
- Referee continuity: black/white vertical striped jersey, black shorts/socks/shoes, black whistle and watch, deadpan expression.
- Main model owns creative judgment and Higgsfield prompts. `gpt-5.6-terra` low may handle metadata, checksums, JSON validation, polling summaries, and ffprobe QA only.
- All generated and edited outputs stay under `edit/`; source assets remain untouched.
- Planned Higgsfield budget: approximately 399 credits before retries, leaving approximately 763 of the current 1,162-credit balance.
- No Git commit steps because this workspace is not a Git repository. Each task checkpoints state in `edit/higgsfield/jobs.json` and `edit/project.md`.

---

### Task 1: Freeze the production asset manifest

**Files:**
- Create: `edit/production/asset-manifest.json`
- Create: `edit/production/continuity-rules.md`
- Modify: `edit/project.md`

**Interfaces:**
- Consumes: source images under `ai 스토리보드/` and `260702_토스_선불카드_애셋_모음집/`.
- Produces: immutable source paths, SHA-256 hashes, dimensions, roles, and prohibited-use notes for every later task.

- [ ] **Step 1: Create directories**

Run:

```powershell
New-Item -ItemType Directory -Force edit/production,edit/prompts,edit/higgsfield,edit/generated/stills,edit/generated/video_mini,edit/generated/video_final,edit/audio,edit/animations,edit/verify | Out-Null
```

Expected: every directory exists and no source folder changes.

- [ ] **Step 2: Hash the locked sources**

Run `Get-FileHash -Algorithm SHA256` for these exact files and store the values in `asset-manifest.json`:

```text
ai 스토리보드/장소와 인물.png
ai 스토리보드/스토리보드 1.png
ai 스토리보드/스토리 1.png
ai 스토리보드/스토리 2.png
ai 스토리보드/스토리 3.png
ai 스토리보드/b55b92ad-5b3c-40e4-adb1-c9b8ba492165.png
260702_토스_선불카드_애셋_모음집/pre-card-hologram-front (1).png
```

Expected JSON root keys: `version`, `created_at`, `assets`, `render_spec`.

- [ ] **Step 3: Encode explicit roles and exclusions**

Set the card asset role to `exact_product_front`. Set `bc087e2e-1b35-44bf-a25a-0d598ef7482f.png` to `excluded_character_reference`. Set the APNG and 3D hand assets to `excluded_from_main_film`. Record `KakaoTalk_20260715_200455753.mp4` as `excluded_reference_video`.

- [ ] **Step 4: Validate the manifest**

Run:

```powershell
Get-Content edit/production/asset-manifest.json -Raw | ConvertFrom-Json | Out-Null
```

Expected: exit code 0.

- [ ] **Step 5: Write the session checkpoint**

Append a session to `edit/project.md` stating that the premium-commercial direction is locked, the reference MP4 is excluded, and generation has not started.

### Task 2: Upload the minimum Higgsfield reference set

**Files:**
- Create: `edit/higgsfield/jobs.json`
- Create: `edit/higgsfield/upload-map.md`

**Interfaces:**
- Consumes: manifest entries from Task 1.
- Produces: confirmed Higgsfield media IDs keyed as `storyboard_master`, `tourist_story`, `referee_sheet`, and `toss_card_exact`.

- [ ] **Step 1: Open one Higgsfield image-upload widget**

Call `media_upload_widget` with `type=image`, `multiple=true`, `min_files=4`, `max_files=4` and select exactly:

```text
ai 스토리보드/장소와 인물.png
ai 스토리보드/스토리 1.png
ai 스토리보드/b55b92ad-5b3c-40e4-adb1-c9b8ba492165.png
260702_토스_선불카드_애셋_모음집/pre-card-hologram-front (1).png
```

- [ ] **Step 2: Save returned media IDs**

Write `edit/higgsfield/jobs.json` as valid JSON with top-level keys `media`, `image_jobs`, `mini_video_jobs`, `final_video_jobs`, and `downloads`. Do not infer IDs from filenames; copy confirmed IDs exactly.

- [ ] **Step 3: Verify type and count**

Expected: four confirmed image media IDs and no video/audio IDs.

### Task 3: Generate and approve character lock sheets

**Files:**
- Create: `edit/prompts/01_tourist_lock.md`
- Create: `edit/prompts/02_referee_lock.md`
- Create: `edit/generated/stills/tourist_lock.png`
- Create: `edit/generated/stills/referee_lock.png`
- Modify: `edit/higgsfield/jobs.json`

**Interfaces:**
- Consumes: confirmed storyboard/referee media IDs.
- Produces: approved image job IDs `tourist_lock` and `referee_lock` for every video generation.

- [ ] **Step 1: Write the tourist prompt verbatim**

```text
Professional photorealistic production character reference sheet for one exact Japanese female tourist, late 20s, naturally attractive and believable rather than idol-like, soft oval face, realistic fair skin texture, medium-length dark-brown hair with airy bangs and gentle waves. Locked wardrobe: loose ivory cotton blouse with subtle fabric texture, light-blue straight-fit jeans, small beige crossbody bag, silver hard-shell carry-on suitcase. Include front full body, left three-quarter pulling suitcase, right profile, waist-up looking down at an unbranded generic transit card, hand-and-arm tapping pose, rear three-quarter, and expressions neutral / mildly puzzled / quietly startled / relieved silent bow. Same face, hair, proportions, clothes, bag and suitcase in every panel. Bright premium Japanese commercial photography, cool cyan-white studio daylight, soft bloom, subtle fine grain, clean separated panels on cool-white background. No TOSS card, no logos, no referee, no fare gate, no text, no captions, no duplicated limbs, no malformed hands, no camera-facing gaze in the tapping pose.
```

- [ ] **Step 2: Preflight and generate the tourist sheet**

Use `gpt_image_2`, `aspect_ratio=16:9`, `resolution=2k`, `quality=high`, `count=2`. Attach `storyboard_master` and `tourist_story` with role `image`. First call with `get_cost=true`, then submit after confirming cost is no more than 14 credits.

- [ ] **Step 3: Approve one tourist variant**

Reject any variant with skirt, short sleeves, missing jeans, changed bag, missing suitcase, camera-facing tapping gaze, or non-Japanese facial styling. Save the selected raw URL to `tourist_lock.png` and its job ID to `jobs.json`.

- [ ] **Step 4: Write the referee prompt verbatim**

```text
Professional photorealistic production character reference sheet for one exact Korean male soccer referee, late 30s to early 40s, athletic realistic build, short neatly styled black hair, strong cheekbones and defined jaw, calm severe completely deadpan expression. Locked uniform: black-and-white vertical striped referee jersey with small chest pocket, black referee shorts, black knee socks with thin white bands, black football referee shoes, black sports watch, black whistle on a short black lanyard. Include front full body, both three-quarter views, side-profile deliberate walking pose, separate close-up actively blowing the whistle, reaching into chest pocket, low-angle pose with arm fully extended vertically like showing a red card, hand detail sized to hold a vertical card, and an arm entering from outside an otherwise empty frame. Same face, body, uniform and accessories in every panel. Premium Japanese commercial photography, cool cyan-white studio light, soft bloom, subtle grain, clean separated panels on cool-white background. No smile, anger, shouting, tourist, subway gate, stadium, crowd, text, card logo, duplicate whistle, duplicate limbs, or malformed hands.
```

- [ ] **Step 5: Preflight, generate, and approve the referee sheet**

Use `gpt_image_2`, 16:9, 2K High, count 2 with `storyboard_master` and `referee_sheet` references. Approve only a variant with a distinct whistle-blowing pose and separate walking pose, fully vertical raised arm, intact watch, and consistent deadpan face.

### Task 4: Generate seven locked shot anchors

**Files:**
- Create: `edit/prompts/03_shot_anchors.md`
- Create: `edit/generated/stills/shot_01_fail.png`
- Create: `edit/generated/stills/shot_02_reaction.png`
- Create: `edit/generated/stills/shot_03_whistle.png`
- Create: `edit/generated/stills/shot_04_walk.png`
- Create: `edit/generated/stills/shot_05_card_reveal.png`
- Create: `edit/generated/stills/shot_06_success.png`
- Create: `edit/generated/stills/shot_07_relief.png`
- Modify: `edit/higgsfield/jobs.json`

**Interfaces:**
- Consumes: approved tourist/referee job IDs and exact TOSS media ID.
- Produces: one approved 9:16 start image per motion unit.

- [ ] **Step 1: Generate each anchor as a separate image job**

Use `gpt_image_2`, 9:16, 2K High, count 1. All prompts share: ultra-realistic clean Seoul subway, premium Japanese commercial, cool cyan-white morning light, subtle bloom and grain, no generated text, no random signage, no crowd, no dialogue.

Exact actions:

```text
01 fail: tourist with silver suitcase taps a muted gray-lilac unbranded transit card; reader shows a red X; TOSS colors and logos absent.
02 reaction: tight portrait of the same tourist looking down at card and reader, then glancing toward an offscreen sound; suitcase handle and beige bag remain visible.
03 whistle: symmetrical distant corridor; referee alone, actively blowing whistle, full body, deadpan, tourist absent.
04 walk: low centered 50mm tracking composition; referee takes long deliberate strides toward camera, whistle out of mouth, arms natural.
05 reveal: low-angle referee with arm fully vertical, exact blue hologram TOSS card presented like a red card; face visible and deadpan.
06 success: macro hand, exact blue TOSS card and subway reader; green recognition glow; card face readable; no red X.
07 relief: same tourist beside the open gate, giving a small relieved smile and subtle silent bow, with bag and suitcase continuity.
```

- [ ] **Step 2: Product-fidelity gate**

For anchors 05 and 06, reject generated logos as final imagery. The generated card establishes hand pose and lighting only; mark both as requiring exact PNG replacement in post.

- [ ] **Step 3: Visual continuity contact sheet**

Use ffmpeg tile to create `edit/verify/anchors_contact.png`. Expected: same tourist/referee identity and lighting across all seven images.

### Task 5: Generate seven Mini motion tests

**Files:**
- Create: `edit/prompts/04_video_motion.md`
- Create: `edit/generated/video_mini/01_fail.mp4` through `07_relief.mp4`
- Modify: `edit/higgsfield/jobs.json`

**Interfaces:**
- Consumes: seven anchor job IDs plus character lock job IDs.
- Produces: motion-approved prompt parameters for final generation.

- [ ] **Step 1: Preflight cost**

For every shot use `seedance_2_0_mini`, `aspect_ratio=9:16`, `duration=4`, `resolution=720p`, `bitrate_mode=high`, `genre=comedy`, `generate_audio=false`. Expected total cost: approximately 70 credits.

- [ ] **Step 2: Submit all seven simple motions**

Use each matching anchor as `start_image` and matching character locks as `image_references`. Use these exact motion prompts, each followed by `Stable identity and wardrobe, natural anatomy and hands, one continuous shot, no cuts, no text, no dialogue, no camera shake, premium Japanese commercial.`

```text
01 fail: Slow precise macro push-in. The tourist moves the unbranded gray-lilac card to the reader, holds it flat for half a second, the gate indicator changes to a clean red X, and she withdraws the card slightly. TOSS branding must never appear.
02 reaction: Locked 85mm portrait. The tourist looks down at her card and the reader, pauses, then moves only her eyes first and turns her head slightly toward the offscreen whistle direction. Mild puzzlement, never broad comedy.
03 whistle: Symmetrical locked corridor shot. The distant referee raises the whistle already on its lanyard to his lips and gives two short visible dry blasts, then lowers his hand while keeping a severe deadpan face. He does not walk.
04 walk: Low centered tracking shot moving backward smoothly. The referee walks toward camera with long deliberate strides, whistle hanging away from his mouth, arms swinging naturally, expression unchanged. At the end his shoulder crosses into the right edge of the tourist's framing space.
05 reveal: Controlled chest-pocket close-up flowing into a low angle without a cut. The referee reaches into the pocket, removes one vertical blue card, and fully extends his arm straight above his head like a red-card decision. His wrist stops firmly at the top; no smile or shouting.
06 success: Macro product-action shot. The referee rotates the vertical blue card so its face becomes parallel to the reader, taps once, holds steady, and the indicator changes from neutral to a green arrow. Fingers never cover the chip or TOSS logo.
07 relief: Stable 50mm medium portrait. The open gate is behind the tourist. She exhales silently, gives a small relieved smile and a subtle polite bow, then straightens while keeping one hand on the silver suitcase handle.
```

- [ ] **Step 3: Poll and download completed jobs**

Poll job results without modifying prompts. Save raw URLs and local filenames in `jobs.json`. Download with `Invoke-WebRequest` only after status is `completed`.

- [ ] **Step 4: Motion acceptance gate**

Approve: natural card tap, whistle visibly between lips, walking without whistle at lips, fully raised card arm, reader interaction without finger/card fusion. Revise prompts and rerun only failed shots.

### Task 6: Generate seven final Seedance clips

**Files:**
- Create: `edit/generated/video_final/01_fail.mp4` through `07_relief.mp4`
- Modify: `edit/higgsfield/jobs.json`

**Interfaces:**
- Consumes: Mini-approved prompts and references.
- Produces: final silent 1080p sources for the EDL.

- [ ] **Step 1: Preflight final cost**

Use `seedance_2_0`, 9:16, 4 seconds, `resolution=1080p`, `mode=std`, `bitrate_mode=high`, `genre=comedy`, `generate_audio=false`. Expected total cost: approximately 252 credits.

- [ ] **Step 2: Generate one final job per shot**

Copy only the motion-approved prompt and references. Do not combine shots or enable native audio.

- [ ] **Step 3: Download and probe**

Run ffprobe on each local clip. Expected: playable H.264/HEVC video, portrait aspect, duration near 4 seconds, no required audio stream.

- [ ] **Step 4: Frame QA**

Extract first, middle, and last frame of every clip to `edit/verify/final_sources/`. Reject identity drift, wardrobe changes, extra fingers, malformed fare gate, random text, duplicate card, or referee smile.

### Task 7: Build controlled sound and typography assets

**Files:**
- Create: `edit/audio/whistle_master.wav`
- Create: `edit/audio/footsteps.wav`
- Create: `edit/audio/pass_chime.wav`
- Create: `edit/audio/subway_ambience.wav`
- Create: `edit/audio/licenses.md`
- Create: `edit/animations/sfx_overlay.mov`
- Create: `edit/animations/end_card.mov`

**Interfaces:**
- Consumes: CC0/public-domain sound sources and exact product PNG.
- Produces: 48kHz WAV stems and alpha-capable ProRes 4444 overlays.

- [ ] **Step 1: Acquire the locked non-speech sources**

Use the following source pages and record title, author, URL, license, and download date in `licenses.md`:

```text
Whistle: Pablo-F, referee-whistle.wav, CC BY 3.0, https://freesound.org/people/Pablo-F/sounds/90743/
Footsteps: Aerny, Shoes 01 | hard sole.wav, CC0, https://freesound.org/people/Aerny/sounds/578705/
Ambience: HenKonen, Subway station loop (no trains), CC0, https://freesound.org/people/HenKonen/sounds/797671/
```

The whistle attribution must appear in `licenses.md`. Select a quiet ambience range with no intelligible announcement. If a Freesound account is unavailable, use the site's public preview audio under the same license and document that the preview file was used.

- [ ] **Step 2: Normalize audio**

Convert every stem to 48kHz stereo PCM. Trim the whistle to two 90–120ms blasts separated by 80–120ms. Use this one file twice in the final mix. Create `pass_chime.wav` locally as a 70ms 988Hz sine followed by a 170ms 1319Hz sine with 8ms fade-in and 40ms fade-out; do not source or imitate a proprietary transit chime.

- [ ] **Step 3: Render Japanese SFX overlay**

Use `C:\Windows\Fonts\YuGothB.ttc` for clean copy and a locally available Japanese-capable handwritten treatment derived from Yu Gothic Bold with rotation/stroke. Render only `ピッ、ピッ！`, `え？`, `コツ、コツ`, `シャキーン！`, `ピロン♪`. No Korean SFX.

- [ ] **Step 4: Render the exact end card**

Use `pre-card-hologram-front (1).png`, TOSS blue accent, main copy `韓国の交通カードは、TOSSで。`, and small Korean `한국 여행, 교통카드는 TOSS로.` Hold 1.5 seconds with no generated text.

### Task 8: Assemble the 14.7-second preview

**Files:**
- Create: `edit/edl.json`
- Create: `edit/master.srt`
- Create: `edit/preview.mp4`

**Interfaces:**
- Consumes: seven final clips, audio stems, SFX overlay, and end card.
- Produces: reviewable 1080×1920 preview.

- [ ] **Step 1: Select exact visual ranges**

Use the approved design timing: 0.00–3.35 fail/reaction, 3.35–4.55 whistle reveal, 4.55–8.05 walk/frame-in, 8.05–10.25 card reveal, 10.25–13.15 success/reaction, 13.15–14.70 end card.

- [ ] **Step 2: Extract per segment with boundary fades**

Apply 30ms audio fades to every audio-bearing segment. Scale/crop to 1080×1920 before concat. Do not build one monolithic source filtergraph.

- [ ] **Step 3: Composite exact product views**

Replace the readable card plane in reveal and tap windows with the exact PNG using tracked perspective or a locked still/overlay. Verify chip, `Toss Prepaid Card`, hologram, and TOSS logo orientation.

- [ ] **Step 4: Add overlays and subtitles last**

Shift overlays with `setpts=PTS-STARTPTS+T/TB`. Apply the Japanese overlay and final copy after all product compositing. `master.srt` contains only the small Korean translation if it is retained as subtitle rather than graphics.

- [ ] **Step 5: Mix sound**

Place the first whistle at 0.95 seconds near the reader and the exact same whistle at 3.70 seconds with distant corridor reverb. Place footsteps 4.80–6.80, reveal accent at 9.65, pass chime at 11.35, and a short brand tone into the end card. Keep peaks below -1 dBTP.

### Task 9: Verify and deliver

**Files:**
- Create: `edit/verify/preview_timeline.png`
- Create: `edit/verify/qa-report.md`
- Create: `edit/final.mp4`
- Modify: `edit/project.md`

**Interfaces:**
- Consumes: `edit/preview.mp4`.
- Produces: final approved advertisement and persistent session memory.

- [ ] **Step 1: Probe technical output**

Run ffprobe. Expected: 1080×1920, 30fps, 14.2–14.9 seconds, H.264 video, AAC 48kHz stereo.

- [ ] **Step 2: Inspect every cut**

Create ±1.0-second contact sheets at 3.35, 4.55, 8.05, 10.25, and 13.15 seconds. Check flashes, identity drift, card discontinuity, hidden text, and audio spikes.

- [ ] **Step 3: Silent-story test**

Watch muted. Expected story: wrong card fails → tourist puzzled → referee revealed → referee presents TOSS → TOSS succeeds. If this chain is unclear, fix picture timing before audio.

- [ ] **Step 4: Brand and language test**

Confirm the TOSS card never appears before the reveal; all Japanese strings match the approved copy; no Korean SFX or random generated lettering remains.

- [ ] **Step 5: Render final and checkpoint**

After no more than three internal correction passes, render `edit/final.mp4`, append decisions and outstanding items to `edit/project.md`, and link the final video and QA report to the user.
