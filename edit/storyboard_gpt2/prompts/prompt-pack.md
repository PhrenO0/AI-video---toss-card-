# GPT Image Prompt Pack

All prompts use the built-in GPT Image tool. Every listed input is a reference image, not an edit target.

## Shared visual header

```text
Use case: ads-marketing, sketch-to-render, identity-preserve.
Asset type: a single photorealistic 9:16 keyframe for a premium Japanese television commercial.
Scene: an unmistakably Korean Seoul subway fare-gate hall with gray tiled columns, blue route boards and a black overhead sign reading exactly “타는 곳  Tracks  ①  →”; cool cyan-white fluorescent lighting, realistic stainless-steel gate housings, dark glass swing flaps, rubber edges and pale stone floor.
Continuity: G3 is the center tourist gate; G4 is the adjacent lane on screen-right; G3's reader is on the tourist's right, screen-right of her body. Preserve the supplied identities exactly.
Style: live-action commercial photography, natural skin and fabric texture, subtle film grain, plausible transit architecture, no glossy CGI look.
Text constraint: preserve only the exact large overhead “타는 곳  Tracks  ①  →”; keep other background words too small to read; no subtitles, dialogue, speech balloons, watermark or UI text.
```

## A01 — gate master

Inputs: S01 sketch = composition reference.

```text
Create the empty spatial master with exactly six separate gate cabinets forming five walk-through lanes. Front-facing eye-level vertical wide shot from the unpaid side. The center third lane is G3 and the adjacent screen-right lane is G4. Preserve physically plausible entry readers and dark glass flaps. Add gray tiled columns, blue route-information boards, a long Korean concourse and one large black overhead sign reading exactly “타는 곳  Tracks  ①  →”. Keep the foreground open for a traveler entering from screen-left. Straight 24mm architecture, natural steel and tile reflections. Avoid generic airport styling, duplicated housings, merged lanes, floating readers, impossible flap placement and extra large text.
```

## A02 — tourist blocking master

Inputs: S02 sketch = composition reference; tourist sheet = exact identity/wardrobe reference; A01 = exact environment/geography reference.

```text
Preserve A01's Korean station, exact `타는 곳  Tracks  ①  →` sign, camera height, six cabinets/five lanes and G3/G4 geography. Add exactly one locked Japanese woman entering from offscreen-left and stopping at the G3 entrance. She remains before the closed dark glass flap. Her right arm reaches toward the screen-right G3 reader; her silver suitcase trails behind-left and remains outside the gate. Full body plus gate context, calm travel posture, beige crossbody bag visible. Do not move the reader, alter the sign, open the flap, place her beyond the flap, add a referee, reveal a TOSS card or add foreground travelers.
```

## A03 — referee blocking master

Inputs: S06 sketch = composition reference; referee sheet = exact identity/wardrobe reference; tourist sheet = exact identity/wardrobe reference; A01 and A02 = environment/blocking references.

```text
Preserve the exact Korean station, overhead `타는 곳  Tracks  ①  →` sign and tourist placement from A01/A02. The tourist stays at G3 before the closed flap. Add exactly one locked Korean soccer referee standing unexpectedly in G4 on screen-right, full body visible, squared shoulders, arms relaxed, stern deadpan face, black whistle and black watch present. He must not stand inside G3 or on screen-left. The comedy comes only from his absurdly formal presence in a real Korean subway. No stadium, crowd, card, smile or dramatic rays.
```

## S01

Inputs: S01 sketch = composition; A01 = environment reference. Use A01 framing as the shot. Empty frontal establishing view, G3 centered, open foreground, stable 28mm lens, all flaps closed, no hero characters.

## S02

Inputs: S02 sketch = composition; A01/A02 = environment and blocking; tourist sheet = identity. Same locked camera as S01. Capture the tourist mid-entry from screen-left, suitcase rolling behind-left, right hand beginning to reach for G3 reader, feet still before the flap.

## S03

Inputs: S03 sketch = composition; A02 = blocking; tourist sheet = identity. 45-degree high angle over the tourist's right shoulder. Show her correct right hand presenting one generic matte-gray unbranded transit card flat over the G3 reader, a small red failure light, closed flaps ahead and suitcase behind-left. No TOSS colors or logo. Anatomically correct hand, reader and card contact.

## S04

Inputs: S04 sketch = composition; A02 = blocking; tourist sheet = identity. Tight natural close-up. She looks down and slightly screen-right toward her hand and reader, brows lifted and lips barely parted, restrained confusion. She does not look into camera or toward the referee yet. Soft 50mm depth, no text.

## S05

Inputs: S05 sketch = emphasis; referee sheet = identity; A03 = Korean setting. Tight head-and-shoulders sports-broadcast portrait of the adult referee performing the ordinary action of blowing his black whistle. Full stern face visible, whistle naturally at mouth, hands outside frame, striped shirt and lanyard preserved, restrained pale radial streaks at background edges. No card, stadium, captions or exaggerated expression.

## S06

Inputs: old S06 = story beat only; A04 = mandatory right-side corridor; `tourist_lock_JP_v2.jpg` and referee sheet = identity. True over-the-shoulder view from behind and slightly left of the tourist: her straight-haired rear head and left shoulder fill the soft-focus screen-left foreground while the referee, 6–8m away and slightly screen-right, looks at her, finishes the whistle beat and takes his first deliberate step toward her. Same A04 wall map, blue signs, tiled columns, ceiling-light rhythm and floor axis. No gates, gate readers, large `타는 곳` sign, TOSS card or extra people.

## S07

Inputs: S07 sketch = composition; A02/A03 = direction; tourist sheet = identity. Tight reaction of the tourist turning only her eyes and chin toward screen-right at the referee, small realistic disbelief, no smile, no dialogue text. Eyeline must exit frame right.

## S08

Inputs: approved S06 + A04 = exact geography and approach axis; `tourist_lock_JP_v2.jpg` and referee sheet = identity. Continue one beat later from the same over-the-shoulder direction with the camera 10–15% closer and slightly lower. Referee advances in a large natural mid-stride toward the tourist, full body and shoes visible, stern deadpan face, whistle lowered and black watch on left wrist. Keep a blurred sliver of the tourist's straight rear hair and left shoulder at the screen-left edge to prove the target. No gates, gate readers, large `타는 곳` sign, TOSS card, runway symmetry or effects.

## S09

Inputs: S09 sketch = composition; A02/A03 = geography; both character sheets = identity. Preserve the tourist's medium profile frame at G3. The referee intrudes from screen-right toward screen-left in the near foreground, shoulder and torso crossing into frame, then stops close but respectful. Tourist looks at him. Only two people, no merged bodies, no cards.

## S10

Inputs: S10 sketch = composition; S09/A03 = blocking; referee sheet = identity; exact TOSS PNG = product insert reference. Medium-tight chest shot. The referee looks down and pulls exactly one card from his striped shirt chest pocket like a soccer booking; only the top corner of the exact blue holographic TOSS card is visible. Restrained blue-gold Japanese game rays begin behind the pocket. Preserve live-action subway background, correct fingers, whistle and watch.

## S11

Inputs: S11 sketch = composition; S10/A03 = continuity; referee sheet = identity; exact TOSS PNG = product reference. Low-angle vertical hero shot. The referee raises exactly one vertical TOSS card fully overhead with one straight arm, front face toward camera, other arm down, stern face below. Exact blue holographic gradient, chip, proportions and TOSS wordmark. Strong controlled blue-gold radial rays, real station still visible, no extra cards or malformed hand.

## S12

Inputs: old S12 = reader design and success state only; corrected S13 = screen relationship; referee sheet = identity; exact TOSS PNG = product reference. Three-quarter medium close-up wide enough to prove hand ownership: reader on screen-left and referee torso on screen-right. His watch-free RIGHT shoulder and arm extend toward screen-left; his RIGHT hand taps one exact TOSS card flat on the green reader. His LEFT arm hangs beside his torso with the black watch clearly visible on the lowered LEFT wrist. Preserve natural five-finger grip, single card and realistic metal reflections. No watch on card hand, left-hand tag, mirrored anatomy, cropped shoulders, tourist hand or failure X.

## S13

Inputs: S13 sketch = composition; A01/A02/A03/S12 = environment and continuity; both character sheets = identity; exact TOSS PNG = product reference. Elegant side-profile vertical wide shot. The G3 glass flaps are now open. Tourist and silver suitcase cross together toward the paid side while she glances back with relieved gratitude. Referee is physically on SCREEN-RIGHT of the reader, facing screen-left, and taps the exact card with his RIGHT HAND; his watch-bearing LEFT ARM hangs straight down. The overhead Korean subway sign reads `타는 곳 / Tracks / ① →`. Leave the upper-left third quiet and uncluttered for later copy. Calm premium end-frame light, no generated overlay text, no mirrored anatomy or hand swap.
