# GPT Image Prompt Pack

All prompts use the built-in GPT Image tool. Every listed input is a reference image, not an edit target.

## Shared visual header

```text
Use case: ads-marketing, sketch-to-render, identity-preserve.
Asset type: a single photorealistic 9:16 keyframe for a premium Japanese television commercial.
Scene: an unmistakably Korean Seoul subway with gray tiled columns, functionally mounted wayfinding, cool cyan-white fluorescent lighting, realistic stainless-steel gate housings, dark glass swing flaps, rubber edges and pale stone floor. Interpret the supplied reality photographs only as architectural and installation references; never copy or composite them.
Continuity: G3 is the center tourist gate; G4 is the adjacent lane on screen-right; G3's reader is on the tourist's right, screen-right of her body. Preserve the supplied identities exactly.
Style: live-action commercial photography, natural skin and fabric texture, subtle film grain, plausible transit architecture, no glossy CGI look.
Sign constraint: retain one slim matte-black “타는 곳 / Tracks” panel on the front-gate axis. It has visible thickness, two narrow metal hanger rods, ceiling plates, correct perspective and a subtle underside shadow. No oversized hero sign, floating sign, paper-thin panel, repeated blue placards or showroom symmetry.
Text constraint: keep secondary words distant or optically defocused instead of generating readable gibberish; no subtitles, dialogue, speech balloons, watermark or UI text.
Character grounding: preserve the exact supplied identity. Capture action in progress with grounded feet, contact shadows, cloth and hair inertia and plausible suitcase-wheel direction; no idle mannequin pose.
```

## A01 — gate master

Inputs: S01 sketch = composition reference.

```text
Create the empty spatial master with exactly six separate gate cabinets forming five walk-through lanes. Front-facing eye-level vertical wide shot from the unpaid side. The center third lane is G3 and the adjacent screen-right lane is G4. Preserve physically plausible entry readers and dark glass flaps. Add gray tiled columns, blue route-information boards, a long Korean concourse and one large black overhead sign reading exactly “타는 곳  Tracks  ①  →”. Keep the foreground open for a traveler entering from screen-left. Straight 24mm architecture, natural steel and tile reflections. Avoid generic airport styling, duplicated housings, merged lanes, floating readers, impossible flap placement and extra large text.
```

## A02 — tourist blocking master

Inputs: S02 sketch = composition reference; `tourist_lock_JP_v2.jpg` = exact Photo 1 identity; A01 = exact environment/geography reference.

```text
Preserve A01's Korean station, exact `타는 곳  Tracks  ①  →` sign, camera height, six cabinets/five lanes and G3/G4 geography. Add exactly the Photo 1 Japanese woman with straight dark-brown shoulder-length hair and light full bangs, entering from offscreen-left and stopping at the G3 entrance. She remains before the closed dark glass flap. Her right arm reaches toward the screen-right G3 reader; her silver suitcase trails behind-left and remains outside the gate. Full body plus gate context, white blouse, light-blue jeans, beige flats and beige crossbody bag visible. Do not move the reader, alter the sign, open the flap, place her beyond the flap, add a referee, reveal a TOSS card or add foreground travelers.
```

## A03 — referee blocking master

Inputs: S06 sketch = timing reference; referee sheet = exact identity/wardrobe reference; `tourist_lock_JP_v2.jpg` = exact Photo 1 identity; A01 and A02 = environment/blocking references.

```text
Preserve the exact Korean station, overhead `타는 곳  Tracks  ①  →` sign and tourist placement from A01/A02. The tourist stays at G3 before the closed flap. Add exactly one locked Korean soccer referee standing unexpectedly in G4 on screen-right, full body visible, squared shoulders, arms relaxed, stern deadpan face, black whistle and black watch present. He must not stand inside G3 or on screen-left. The comedy comes only from his absurdly formal presence in a real Korean subway. No stadium, crowd, card, smile or dramatic rays.
```

## A05 — structure-aware gate hall

Inputs: `gate-hall-reference.jpg` = architecture and installation logic only; A01 = modern gate design only.

```text
Create a portrait 9:16 photorealistic Korean subway fare-gate hall. Interpret only the architecture and installation logic of gate-hall-reference.jpg; do not copy or composite the photograph. Keep the project's modern stainless flap gates from A01. Retain one slim matte-black “타는 곳 / Tracks” panel, physically suspended from the ceiling by two narrow metal rods with visible ceiling plates, realistic panel thickness, subtle underside shadow and correct passenger clearance. Gates, readers, ceiling fixtures, columns and floor grout share one vanishing point. Add restrained depth from columns and distant displays. No people, no TOSS card, no oversized sign, no repeated placards, no readable gibberish and no showroom symmetry.
```

## A06 — structure-aware right concourse

Inputs: `right-concourse-reference.jpg` = architecture and installation logic only; A04 = station palette and right-facing axis only.

```text
Create a portrait 9:16 photorealistic Korean subway side concourse. Interpret only the spatial rules of right-concourse-reference.jpg; do not copy or composite the photograph. Use a low metal-panel ceiling with linear fluorescent fixtures, tiled round columns on the left, a flat tiled service wall on the right, one column-mounted vertical wayfinding panel with a real metal bracket, one framed route map recessed on the right wall, tactile paving and grounded maintenance details. All fixtures follow one vanishing point. No fare gates, no “타는 곳” hero panel, no people, no readable gibberish and no repeated blue signs.
```

## S01

Inputs: S01 sketch = composition; A05 = mandatory environment reference. Use A05 as the exact spatial master. Empty frontal establishing view from slightly below eye level, G3 centered, open foreground, stable 28–35mm lens, all flaps closed, no hero characters. Preserve the slim physically suspended panel, lived-in depth and mild architectural asymmetry.

## S02

Inputs: S02 sketch = story beat only; A05 = exact environment; `tourist_lock_JP_v2.jpg` = exact identity and rear silhouette. Strict rear view from 2–3m behind and slightly above waist height; no face or cheek visible. Capture her finishing the last half-step toward G3 while facing the gates squarely. Weight settles on her left foot, the right heel is still moving, her right arm begins to rise toward the reader and the silver suitcase trails diagonally 30–40 degrees behind-left. Match ceiling light, floor contact shadow, subtle hair and blouse inertia. No card yet.

## S03

Inputs: S03 sketch = composition; A05/S02 = environment and blocking; `tourist_lock_JP_v2.jpg` = identity and straight-hair silhouette. First failed tap only. Use a 45-degree high angle over her right shoulder. Show her correct right hand presenting one generic matte-gray unbranded transit card flat over the G3 reader, a red failure X, closed flaps ahead and the suitcase behind-left. No TOSS colors or logo. Anatomically correct hand, reader and card contact.

## S04

Inputs: A05/S03 = exact gate, card and second-attempt continuity; `tourist_lock_JP_v2.jpg` = exact face, full bangs, eye shape, jawline and straight shoulder-length hair. Second and final failed tap. Reader-level bottom view from beside the card sensor. The same generic matte-gray card and her right hand dominate the near lower foreground as she taps again. Beyond the card, her exact face is visible; her eyes look downward at the card-reader contact point, never at camera. Eyebrows draw together slightly and lips part minimally in restrained puzzlement. Red failure state, closed flap, no exaggerated face, no selfie angle, no TOSS card.

## S05

Inputs: S05 sketch = emphasis; referee sheet = identity; A03 = Korean setting. Tight head-and-shoulders sports-broadcast portrait of the adult referee performing the ordinary action of blowing his black whistle. Full stern face visible, whistle naturally at mouth, hands outside frame, striped shirt and lanyard preserved, restrained pale radial streaks at background edges. No card, stadium, captions or exaggerated expression.

## S06

Inputs: old S06 = story beat only; A06 = mandatory right-side corridor; `tourist_lock_JP_v2.jpg` and referee sheet = identity. True over-the-shoulder view from behind and slightly left of the tourist while her shoulders are still turning toward the whistle: her exact straight-haired rear head and left shoulder fill the soft-focus screen-left foreground. The referee, 6–8m away and slightly screen-right, looks at her, finishes the whistle and takes his first deliberate step. Preserve A06's restrained mounted signs, wall map, tiled columns, ceiling-light rhythm and floor axis. Match both people to the corridor light and contact shadows. No gates, gate readers, `타는 곳` panel, TOSS card or extra people.

## S07

Inputs: S07 sketch = composition; A02/A03 = direction; `tourist_lock_JP_v2.jpg` = exact Photo 1 identity. Tight reaction of the straight-haired tourist turning only her eyes and chin toward screen-right at the referee, small realistic disbelief, no smile, no dialogue text. Eyeline must exit frame right.

## S08

Inputs: approved S06 + A06 = exact geography and approach axis; `tourist_lock_JP_v2.jpg` and referee sheet = identity. Continue one beat later from the same over-the-shoulder direction with the camera 10–15% closer and slightly lower. Referee advances two steps closer in a natural mid-stride, full body and shoes visible, stern deadpan face, whistle lowered and black watch on left wrist. Keep the same blurred sliver of the tourist's exact rear hair and left shoulder at screen-left. Opposite arm and leg cross naturally; front shoe has grounded contact and a plausible shadow. No gates, gate readers, `타는 곳` panel, TOSS card, runway symmetry or effects.

## S09

Inputs: S09 sketch = composition; A05 = mandatory gate-hall geography; `tourist_lock_JP_v2.jpg` and referee sheet = identities. Preserve the exact tourist's medium profile frame at G3 with her supplied face, straight shoulder-length hair and full bangs. The referee intrudes from screen-right toward screen-left in the near foreground, shoulder and torso crossing into frame, then stops close but respectful. Tourist follows him with her eyes while her body remains naturally grounded at the gate. Only two people, no merged bodies, no cards.

## S10

Inputs: S10 sketch = composition; S09/A05 = blocking and gate-hall structure; `tourist_lock_JP_v2.jpg` = exact foreground hair silhouette; referee sheet = identity; exact TOSS PNG = product insert reference. Medium-tight chest shot. The referee looks down and pulls exactly one card from his striped shirt chest pocket like a soccer booking; only the top corner of the exact blue holographic TOSS card is visible. The tourist remains a blurred screen-left foreground fragment with her exact straight shoulder-length hair. Restrained blue-gold Japanese game rays begin behind the pocket. Preserve A05's physical overhead panel and live-action subway depth, correct fingers, whistle and watch.

## S11

Inputs: S11 sketch = composition; S10/A05 = continuity and gate-hall structure; referee sheet = identity; exact TOSS PNG = product reference. Low-angle vertical hero shot. The referee raises exactly one vertical TOSS card fully overhead with one straight arm, front face toward camera, other arm down, stern face below. Exact blue holographic gradient, chip, proportions and TOSS wordmark. Strong controlled blue-gold radial rays, A05 station and suspended panel still physically plausible, no extra cards or malformed hand.

## S12

Inputs: old S12 = reader design and success state only; A05 = mandatory gate-hall structure; corrected S13 = screen relationship; referee sheet = identity; exact TOSS PNG = product reference. Three-quarter medium close-up wide enough to prove hand ownership: reader on screen-left and referee torso on screen-right. His watch-free RIGHT shoulder and arm extend toward screen-left; his RIGHT hand taps one exact TOSS card flat on the green reader. His LEFT arm hangs beside his torso with the black watch clearly visible on the lowered LEFT wrist. Preserve A05's physical panel and depth, natural five-finger grip, single card and realistic metal reflections. No watch on card hand, left-hand tag, mirrored anatomy, cropped shoulders, tourist hand or failure X.

## S13

Inputs: S13 sketch = composition; A05/S12 = environment and continuity; `tourist_lock_JP_v2.jpg` and referee sheet = identities; exact TOSS PNG = product reference. Elegant side-profile vertical wide shot. The G3 glass flaps are now open. The exact supplied tourist with straight shoulder-length hair and her silver suitcase cross together toward the paid side while she glances back with relieved gratitude. Referee is physically on SCREEN-RIGHT of the reader, facing screen-left, and taps the exact card with his RIGHT HAND; his watch-bearing LEFT ARM hangs straight down. Preserve the slim physically suspended `타는 곳 / Tracks` panel from A05. Leave the upper-left third quiet and uncluttered for later copy. Calm premium end-frame light, no generated overlay text, readable gibberish, mirrored anatomy or hand swap.
