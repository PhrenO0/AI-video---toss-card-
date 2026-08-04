# 이미지 프롬프트 팩 — 키프레임 S01~S12

도구 비의존적으로 작성했다. 먼저 **앵커(A01~A04)**를 만들어 확정한 뒤,
그것을 레퍼런스로 붙여 S01~S12를 생성한다.

**이 팩의 대원칙:** 전 컷이 **정면 고정 축**이다. 컷마다 앵글이 아니라 **사이즈만** 바뀐다.
그리고 좌우 가장자리에는 항상 **이야기를 듣는 친구들의 어깨**가 흐리게 걸린다.

---

## 공통 토큰

### `[STYLE]` — 공통 스타일 (S컷 전부)

```
Japanese live-action commercial photography, straight-on frontal composition at eye level,
bright airy summer daylight, milky slightly blown highlights, low saturation pastel grade, soft
bloom, extremely shallow depth of field with creamy bokeh, subject sharp in mid-ground and centered,
vertical 9:16 composition, natural skin texture, subtle film grain, photorealistic, no CGI gloss,
natural understated facial acting
```

### `[FG]` — 전경 어깨 프레이밍 (S01~S10 전부)

```
large soft completely out-of-focus shoulders and upper arms of two listeners standing close to the
camera framing the left and right edges of the frame, the camera looking through the gap between
them, these foreground shapes are heavily blurred and unrecognizable
```

### `[STYLE-PLAIN]` — 앵커용 (전경 보케 제거)

```
Japanese live-action commercial photography, bright airy summer daylight, milky slightly blown
highlights, low saturation pastel grade, soft bloom, vertical 9:16 composition, natural skin texture,
subtle film grain, photorealistic, no CGI gloss
```

### `[NEG]` — 공통 네거티브 (전 컷 필수)

```
no text, no lettering, no subtitles, no captions, no speech bubbles, no logos, no brand marks,
no wordmarks, no watermark, no UI elements, no app screen content, no bus route numbers,
no destination signs, no bus company name, no bus stop panel text, no readable signage,
no exaggerated cartoon expression, no comic effect overlays, no motion lines, no oversaturated colors,
no harsh contrast, no plastic CGI skin, no extra fingers, no deformed hands, no duplicated limbs
```

### `[SENPAI]` — 주인공 고정 묘사

```
a Japanese woman in her mid-twenties with a bright cute energy, dark brown medium-length wavy hair
with light see-through bangs, ivory short-sleeve blouse, a coral crossbody bag strap over her
shoulder, minimal accessories
```

### `[FRIENDS]` — 친구 2명 (S12에만 얼굴 등장)

```
two Japanese women slightly younger, one in a light beige summer blouse and one in a pale blue
short-sleeve top, simple small bags, natural everyday summer styling
```

### `[CARD]` — 제품 지시 (카드 등장 컷 필수)

> **첨부:** `assets/toss-card/pre-card-hologram-front (1).png`
> (손에 든 참고: `assets/toss-card/hand-pre-card-hologram.png`)
>
> **프롬프트에 반드시 포함:**
> ```
> the card is the attached reference product exactly: a vertical blue holographic prepaid card;
> preserve its exact proportions, gradient, surface finish and chip position from the attached image;
> do not redraw, invent, translate or restyle any logo, wordmark or lettering on the card;
> if any text on the card would be uncertain, keep that area clean for later compositing
> ```
>
> ⚠️ 생성물의 카드 로고·문자가 원본과 다르면 **원본 PNG를 원근 맞춰 합성**으로 교체한다.

---

# 앵커 (먼저 생성·확정)

## A01 — 캐릭터 락: 주인공

```
character reference sheet, three views of the same person side by side: front view,
three-quarter left view, right profile; [SENPAI]; identical hair, identical wardrobe and identical
accessories in all three views; bright friendly expression; plain bright seamless background;
even soft studio light; upper body visible, [STYLE-PLAIN]
```

**Negative:** `[NEG]`
**체크:** 세 뷰가 동일인인지 · 코랄 스트랩 색이 일치하는지

## A02 — 캐릭터 락: 친구 2명

```
character reference sheet, two young women standing side by side, front view and three-quarter view
of each; [FRIENDS]; identical wardrobe across views; calm neutral expressions; plain bright seamless
background; even soft studio light, [STYLE-PLAIN]
```

**Negative:** `[NEG]`
**체크:** 두 사람이 서로 구별되는지 · 의상 색이 일관되는지

## A03 — 로케이션 마스터: 서울 도심 버스정류장 (정면)

**한국어 해설:** **이 앵커가 전 컷의 배경 기준이다.** 정면 축을 여기서 확정한다.

```
straight-on frontal view of a bus stop shelter on a bright summer street in central Seoul, seen from
the sidewalk directly facing it at eye level, simple modern shelter with a bench and a completely
blank unmarked information panel, wide pavement, street trees, mid-rise city buildings softly blurred
behind, a road visible behind the shelter, bright midday summer daylight, no people,
all signage completely blank and unreadable, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no advertisements, no route maps, no timetable text, no shop signs, no people`
**체크:** **완전한 정면인지** · 서울 도심으로 읽히는지 · 안내판이 비었는지

## A04 — 로케이션 마스터: 시내버스

```
a clean blue city bus on a summer city street, seen from the side, large windows with soft sky and
tree reflections, the body panels completely blank with no numbers, no destination display and no
company markings anywhere, bright summer daylight, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no advertising wrap`
**체크:** **버스에 어떤 문자도 없는지(가장 중요)** · 파란 시내버스로 읽히는지

---

# 본 컷 S01~S12

## S01 · 0.0–2.5s — 설명이 시작된다 (정면 와이드)

**한국어 해설:** 정면 축과 전경 어깨를 여기서 확립한다. 그녀가 카메라를 향해 손을 흔들며 시작한다.
카메라 위치가 이야기를 듣는 친구들의 자리라는 게 이 한 컷으로 읽혀야 한다.

```
[SENPAI] standing in front of a Seoul bus stop shelter in bright summer daylight, centred in the
frame, looking straight into the lens and waving one hand toward the camera with a bright excited
smile as if calling out "listen to this", her posture open and friendly, the shelter and a road
visible behind her softly blurred, [FG], 35mm lens at eye level, straight-on frontal view, [STYLE]
```

**Negative:** `[NEG]` + `no bus in frame, no card visible yet`
**첨부:** A01(주인공), A03(정류장)
**체크:** 완전한 정면인지 · **좌우에 흐린 어깨가 걸렸는지(필수)** · 카드가 아직 없는지 · 시선이 렌즈인지

## S02 · 2.5–5.0s — 카드를 들어 보인다 ★제품 최초 노출 (정면 미드)

**한국어 해설:** 레퍼런스의 히어로 제스처. **카드를 얼굴 옆, 전면을 카메라로.**
앵글은 그대로 두고 사이즈만 조인다.

```
[SENPAI] in front of the bus stop holding a single vertical payment card up beside her face at
chest-to-head height, the card front squarely facing the camera, her face in the upper third and the
card in the middle third of the vertical frame, looking straight into the lens with a bright proud
smile as if saying "look at this", [FG], 50mm lens at eye level, straight-on frontal view,
[CARD], [STYLE]
```

**Negative:** `[NEG]` + `no second card, no bent card, no mirrored logo, no invented card text,
no fingers covering the card front`
**첨부:** A01, A03 + **카드 원본 에셋(필수)**
**체크:** 카드면이 선명하고 정면인지 · 로고가 원본과 동일한지(다르면 원본 합성) · 얼굴과 카드가 한 프레임인지

## S03 · 5.0–7.0s — 검지로 카드를 톡톡 (정면 미드)

**한국어 해설:** "이거야"를 손가락 하나로. 동작은 명확하게 하나만.

```
[SENPAI] holding the vertical card in one hand and tapping it clearly with the index finger of her
other hand, pointing at the card in a single readable gesture, eyebrows slightly raised for emphasis,
looking straight into the lens, [FG], 50mm lens at eye level, straight-on frontal view,
[CARD], [STYLE]
```

**Negative:** `[NEG]` + `no overlapping gestures, no motion blur on hands`
**첨부:** A01, A03 + 카드 원본 에셋
**체크:** 손가락이 카드를 명확히 가리키는지 · 두 손이 프레임 안에 있는지

## S04 · 7.0–9.5s — 허공에 찍는 동작 ★시그니처 (정면 미드)

**한국어 해설:** **이 영상의 시그니처 제스처.** 카드를 허공에 대고 손목을 툭 내려 찍는 시늉.
귀엽고, 한눈에 읽히고, 그 자체가 제품의 소구점이다.

```
[SENPAI] miming a card tap in mid-air, holding the vertical card and flicking her wrist downward as
if touching it to an invisible reader in front of her, a playful pleased expression with her lips
rounded as if making a short "pi" sound, both hands fully inside the frame, looking toward the lens,
slightly wider framing so the whole gesture reads at a glance, [FG], 50mm lens at eye level,
straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no actual card reader device, no terminal, no comic effects, no motion lines`
**첨부:** A01, A03 + 카드 원본 에셋
**체크:** **찍는 동작이 한눈에 읽히는지(가장 중요)** · 실제 단말기가 없는지(허공이어야 함) · 표정이 절제됐는지

## S05 · 9.5–12.0s — 버스와 지하철을 가리킨다 (정면 미드)

**한국어 해설:** "버스도, 지하철도"를 손으로. 뒤 차도를 가리킨 뒤 아래를 가리킨다.
**한 프레임에는 하나의 동작만** — 여기서는 차도를 가리키는 순간을 잡는다.

```
[SENPAI] pointing back over her shoulder toward the road behind her with one hand while still
holding the vertical card in the other, an open enthusiastic expression as if saying "that too",
her gesture clear and unambiguous, looking toward the lens, [FG], 50mm lens at eye level,
straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no bus arriving yet, no overlapping gestures`
**첨부:** A01, A03 + 카드 원본 에셋
**체크:** 가리키는 방향이 뒤쪽 차도인지 · 버스가 아직 없는지 · 동작이 하나인지

### S05b — 아래를 가리키는 순간 (같은 컷 내 두 번째 동작)

```
[SENPAI] pointing downward toward the ground with one hand while holding the vertical card in the
other, indicating something below, warm confident expression, looking toward the lens, [FG],
50mm lens at eye level, straight-on frontal view, [CARD], [STYLE]
```

**용도:** S05 클립 안에서 두 동작을 연결할 때 끝 프레임으로 쓴다.

## S06 · 12.0–14.0s — 엄지 척 + 카드 디테일 (정면 클로즈업)

**한국어 해설:** 카드가 가장 크게 보이는 컷. 축은 그대로, 사이즈만 조인다.

```
frontal close-up of [SENPAI] giving a small thumbs up with one hand while holding the vertical card
close beside her face with the other, her head tilted very slightly, a soft confident smile, looking
straight into the lens, the card surface detail clearly visible, background fully melted into creamy
bokeh, [FG], 85mm lens at eye level, straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no invented card text, no reflection covering the card face`
**첨부:** A01 + 카드 원본 에셋
**체크:** 카드 표면이 선명한지 · 로고가 원본과 동일한지 · 엄지 척이 자연스러운지

## S07 · 14.0–16.0s — 버스가 온다 (정면 미드)

**한국어 해설:** **소리가 먼저 오고 그녀가 반응한다.** 뒤쪽 차도에 버스가 들어와 정지하고,
그녀가 말하다 멈추고 뒤를 돌아본다. 버스는 흐리게 형체만.

```
[SENPAI] in front of the bus stop pausing mid-gesture and turning her head to glance back over her
shoulder, a small "oh already?" surprise on her face, still holding the vertical card, and behind
her a blue city bus has pulled in and stopped, rendered completely out of focus as a soft blue mass
with no readable markings, [FG], 50mm lens at eye level, straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no sharp bus,
no panic expression`
**첨부:** A01, A03, A04(버스)
**체크:** **버스가 완전히 흐린지(문자 리스크 차단)** · 그녀가 뒤를 돌아보는지 · 당황이 절제됐는지

## S08 · 16.0–18.0s — 다급하게 마지막 설명 (정면 미드)

**한국어 해설:** 손을 흔들며 뒷걸음질로 버스 쪽으로 물러나면서도 카드를 계속 들어 보인다.
다급하지만 여전히 밝게.

```
[SENPAI] stepping backward toward the bus while still facing the camera, waving one hand urgently
and holding the vertical card up with the other, hurried but still bright and smiling as if saying
"wait, one more thing", her body angled back but her face still toward the lens, the blurred blue
bus behind her with a soft indicator lamp glow, [FG], 50mm lens at eye level, straight-on frontal
view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no panic grimace, no comic sweat drops, no route number, no sharp bus`
**첨부:** A01, A03, A04 + 카드 원본 에셋
**체크:** 뒷걸음질이 보이는지 · 얼굴이 여전히 카메라를 향하는지 · 다급함이 귀여운 범위인지

## S09 · 18.0–20.0s — 버스가 그녀를 가린다 (정면 와이드)

**한국어 해설:** 원작의 "기차가 지나가는 화면"의 대응. **S01과 같은 사이즈로 돌아와**
버스가 프레임을 가로지르며 그녀를 완전히 가린다. 강한 수평 모션 블러.

```
straight-on frontal wide view of the bus stop, framed the same as the opening shot, with a blue city
bus sweeping across the frame in front of the shelter and almost completely covering it, strong
horizontal motion blur across the bus body and windows, sky reflections streaking along the glass,
the bus panels completely blank with no markings of any kind, bright summer daylight, [FG],
35mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no sharp frozen bus,
no visible person behind the bus`
**첨부:** A03, A04
**체크:** **버스 문자 전무(필수)** · 모션 블러가 충분한지 · 그녀가 가려졌는지 · S01과 사이즈가 같은지

## S10 · 20.0–22.5s — 아무도 없다 ★개그 착지 (정면 와이드)

**한국어 해설:** **S01·S09와 완전히 같은 정면 와이드.** 버스가 지나간 뒤 정류장에 아무도 없다.
전경의 친구 어깨는 여전히 걸려 있다 — 그들은 남았다.

```
straight-on frontal wide view of the same Seoul bus stop, framed identically to the opening shot,
now completely empty with nobody standing in front of the shelter, the road behind clear and quiet,
still bright summer daylight, calm and unchanged, [FG] with the two blurred listeners still framing
the edges, 35mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no bus in frame, no people in the mid-ground, no main character`
**첨부:** **S01 생성 결과(필수 — 구도 일치용)** + A03
**체크:** **S01과 프레이밍이 일치하는지(가장 중요)** · 주인공이 완전히 없는지 · 버스가 없는지 ·
전경 어깨는 남아 있는지

## S11 · 22.5–27.0s — 제품 인서트 (배경 플레이트)

**한국어 해설:** 페이드아웃 후 제품 인서트. **카드와 문자는 전부 후반 합성**이므로
생성하는 것은 **배경 플레이트뿐**이다. 중앙과 하단을 비워둔다.

```
soft defocused background plate of a summer Seoul bus stop and street, everything melted into creamy
pastel bokeh with no recognizable detail, bright milky highlights, gentle warm-to-cool gradient,
the centre and the lower half of the frame kept visually quiet and uncluttered as empty space,
no people, no vehicles in focus, vertical 9:16, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no people, no sharp objects, no busy detail in the centre,
no busy detail in the lower half`
**첨부:** A03
**체크:** 중앙·하단이 비었는지 · 완전히 흐린 보케인지
**후반 합성:** 카드 원본 컷아웃(중앙) + 선행 문구 + 메인 카피 + 각주 + 워터마크

## S12 · 27.0–30.0s — 친구들이 폰을 꺼낸다 (CTA)

**한국어 해설:** **전경의 흐린 어깨였던 친구들이 처음 얼굴을 드러낸다.**
폰 화면은 빈 플레이트로 생성하고 실제 앱 화면을 후반 합성한다.
**좌상단·하단 여백**을 비워 로고와 워터마크 자리를 만든다.

```
medium two shot of [FRIENDS] standing at the bus stop looking down together at one smartphone held
between them, both smiling softly with eyes gently cast down, warm and relaxed, the phone screen is
a completely uniform blank light grey surface with no content whatsoever, the two women placed
slightly right of centre so the upper-left area of the frame stays visually quiet and empty, the
bottom fifth of the frame kept clean and uncluttered, bright backlight with fully melted bokeh
background, 85mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no app interface, no icons, no text on screen, no logo, no headline,
no busy elements in the upper-left area, no busy elements in the bottom fifth`
**첨부:** A02(친구), A03
**체크:** **폰 화면이 완전히 비었는지(필수)** · **좌상단·하단 여백 확보(필수)** · 표정이 부드러운지

---

## 생성 순서 권장

1. **A03 → 확정** (정면 축이 여기서 결정된다. 전 컷의 배경 기준)
2. **A01 → 확정** (주인공 얼굴·의상이 흔들리면 대부분을 다시 만들어야 한다)
3. **A04 → 확정** (버스에 문자가 하나라도 생기면 전부 다시)
4. **A02 → 확정**
5. **S01 생성 → 확정** (S09·S10의 구도 기준이 되므로 먼저)
6. **S10 생성** (S01을 레퍼런스로 붙여 구도 일치 — 인물만 빼면 된다)
7. 나머지 S02~S09, S05b, S11, S12
8. 실패한 컷만 개별 재생성. 전체를 다시 만들지 않는다

## 생성 후 필수 육안 검수

- [ ] **전 컷이 정면 축인지** (앵글이 바뀐 컷이 없는지)
- [ ] **S01~S10 좌우에 흐린 어깨가 걸려 있는지**
- [ ] **S01·S09·S10의 프레이밍이 일치하는지**
- [ ] 어떤 컷에도 **생성된 문자·로고**가 없다
- [ ] **버스에 노선번호·행선지·회사명이 없다** (S07·S08·S09 특히)
- [ ] **정류장 안내판이 비어 있다**
- [ ] S04에 **실제 단말기가 없다** (허공에 찍는 동작이어야 함)
- [ ] S12의 폰 화면이 **완전히 비어 있다**
- [ ] 카드 등장 컷(S02·S03·S04·S05·S06·S08)의 카드가 원본 에셋과 일치한다 (다르면 원본 합성)
- [ ] S11·S12에 좌상단·하단 여백이 있다
- [ ] 말풍선·집중선·만화 효과가 없다
- [ ] 손가락 개수·형태가 정상이다
- [ ] 의상·헤어·가방이 전 컷 일관된다
