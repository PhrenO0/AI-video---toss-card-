# 이미지 프롬프트 팩 — 키프레임 S01~S11

도구 비의존적으로 작성했다. GPT Image·Higgsfield 등 어디서든 그대로 사용할 수 있다.
먼저 **앵커(A01~A03)**를 만들어 확정한 뒤, 그것을 레퍼런스로 붙여 S01~S11을 생성한다.

---

## 공통 토큰

아래 토큰을 각 프롬프트에서 그대로 치환해 사용한다.

### `[STYLE]` — 공통 스타일 (S컷 전부)

```
Japanese live-action commercial photography, bright airy summer daylight, milky slightly blown
highlights, low saturation pastel grade, soft bloom, extremely shallow depth of field with creamy
bokeh, large out-of-focus foreground masses framing the left and right edges so the camera looks
through the gap between them, subject sharp in mid-ground and centered, vertical 9:16 composition,
natural skin texture, subtle film grain, photorealistic, no CGI gloss, natural understated acting
```

### `[STYLE-PLAIN]` — 앵커용 (전경 보케 제거)

```
Japanese live-action commercial photography, bright airy daylight, milky slightly blown highlights,
low saturation pastel grade, soft bloom, vertical 9:16 composition, natural skin texture,
subtle film grain, photorealistic, no CGI gloss
```

### `[NEG]` — 공통 네거티브 (전 컷 필수)

```
no text, no lettering, no subtitles, no captions, no speech bubbles, no logos, no brand marks,
no wordmarks, no watermark, no UI elements, no app screen content, no station name signage,
no readable signs, no exaggerated cartoon expression, no oversaturated colors, no harsh contrast,
no plastic CGI skin, no extra fingers, no deformed hands, no duplicated limbs
```

### `[TOURIST]` — 주인공 고정 묘사

```
a Japanese woman in her mid-twenties, dark brown medium-length wavy hair with light see-through
bangs, ivory short-sleeve blouse, light beige midi skirt, small crossbody bag with a coral strap,
minimal accessories, natural understated expression
```

### `[CARD]` — 제품 지시 (카드 등장 컷 필수)

> **첨부:** `assets/toss-card/pre-card-hologram-front (1).png`
> (손에 든 참고가 필요하면 `assets/toss-card/hand-pre-card-hologram.png` 추가)
>
> **프롬프트에 반드시 포함:**
> ```
> the card is the attached reference product exactly: a vertical blue holographic prepaid card;
> preserve its exact proportions, gradient, surface finish and chip position from the attached image;
> do not redraw, invent, translate or restyle any logo, wordmark or lettering on the card;
> if any text on the card would be uncertain, keep that area clean and let it be composited later
> ```
>
> ⚠️ 생성물의 카드 로고·문자가 원본과 다르면 **원본 PNG를 원근 맞춰 합성**으로 교체한다.

---

# 앵커 (먼저 생성·확정)

## A01 — 캐릭터 락 (주인공)

**한국어 해설:** 전 컷의 얼굴·헤어·의상 기준이 되는 3면 시트. 이걸 확정한 뒤 모든 S컷에 레퍼런스로 붙인다.

```
character reference sheet, three views of the same person side by side: front view,
three-quarter left view, right profile; [TOURIST]; identical hair, identical wardrobe and identical
accessories in all three views; calm neutral friendly expression; standing against a plain bright
seamless background; even soft studio light; full upper body visible, [STYLE-PLAIN]
```

**Negative:** `[NEG]`
**체크:** 세 뷰의 인물이 동일인으로 보이는지, 의상·가방 스트랩 색이 일치하는지.

## A02 — 로케이션 마스터: 지하철 개찰구

**한국어 해설:** S01·S07의 배경 기준. 무인 상태로 만들어 공간을 고정한다.

```
wide frontal view of a clean modern Seoul subway fare gate hall, a row of stainless steel fare
gates with closed flap barriers, contactless card readers on top of the gate housings, glossy tiled
floor, bright morning daylight mixing with cool ceiling lights, no people, calm and spacious,
signage present but completely out of focus and unreadable, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no crowds, no readable station names`
**체크:** 게이트 배열이 물리적으로 자연스러운지, 리더기 위치가 일관되는지.

## A03 — 로케이션 마스터: 플랫레이 표면

**한국어 해설:** **S03과 S06이 반드시 같은 표면·조명이어야 한다.** 이 앵커를 먼저 고정한다.

```
top-down 90 degree view of an empty bright matte tabletop, milky off-white surface with very
subtle texture, soft diffused overhead light, faint soft shadows, nothing on the surface,
clean and minimal, vertical 9:16 framing, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no objects, no patterns, no wood grain`
**체크:** 완전 수직 탑다운인지, 표면 톤이 밀키 화이트인지.

---

# 본 컷 S01~S11

## S01 · 0.0–2.0s — 훅: 안 닫히는 지갑

**한국어 해설:** 첫 2초에 "지갑이 문제"가 읽혀야 한다. 얼굴보다 **손과 지갑**이 주인공인 컷.
두꺼워서 안 닫히는 지갑, 손가락 사이로 떨어지는 동전.

```
close-up of a woman's hands trying and failing to close an overstuffed compact wallet, the wallet
is visibly too thick to shut, banknotes and receipts sticking out of the edges, a few coins slipping
out between her fingers and starting to fall, she is [TOURIST], shot at chest height with a slight
high angle so the crowded inside of the wallet is visible, 50mm lens, in a bright Seoul subway
station concourse, the blurred stainless steel fare gate housings and a commuter's shoulder form
large out-of-focus masses on the left and right edges, warm side daylight from a window,
her face only partially visible at the top edge, [STYLE]
```

**Negative:** `[NEG]` + `no visible card brands, no legible currency serial text, no logos on the wallet`
**첨부:** A01(캐릭터), A02(로케이션)
**체크:** 지갑이 "물리적으로 안 닫힌다"가 보이는지 · 동전이 떨어지는 중인지 · 카드 브랜드 노출 없는지

## S02 · 2.0–4.0s — 난감한 얼굴

**한국어 해설:** 감정 이입 지점. 과장 없이 **작은 미소와 눈썹의 미세한 움직임**만으로.
시선은 아래 지갑 쪽, 고개는 거의 들지 않는다.

```
frontal close-up portrait of [TOURIST], her gaze cast down toward her hands below the frame,
head barely tilted, a small awkward embarrassed smile with a faint eyebrow movement, very subtle
micro-expression, restrained and realistic, 85mm compressed lens at eye level, face positioned in
the upper third of the vertical frame, soft frontal light with a faint rim light on her hair,
bright Seoul subway concourse melted into creamy bokeh behind her, out-of-focus foreground shapes
softly framing both edges, [STYLE]
```

**Negative:** `[NEG]` + `no wide open mouth, no shocked eyes, no comedic reaction, no tears`
**첨부:** A01
**체크:** 표정이 절제됐는지 · 시선이 아래인지 · 얼굴이 상단 1/3에 있는지

## S03 · 4.0–7.0s — 오버헤드 플랫레이: 잡동사니

**한국어 해설:** 지갑 속을 다 꺼내놓은 탑다운. **S06과 프레이밍·조명·표면이 완전히 같아야** 대비가 성립한다.
모든 카드는 무브랜드.

```
top-down 90 degree flat lay on a milky off-white matte tabletop, an open compact wallet in the
centre surrounded by its contents spread out: several folded banknotes, a loose pile of coins,
three or four completely blank unbranded plain plastic cards in muted grey and navy, two folded
paper receipts, one small plain paper coupon, a woman's hand entering from the bottom of the frame
sorting through the pile, cluttered but tidily lit, soft diffused overhead light with faint soft
shadows, vertical 9:16 framing, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no card logos, no bank names, no transit card branding, no chip artwork,
no legible numbers, no smartphone, no Toss card`
**첨부:** A03(표면)
**체크:** **카드가 전부 무지인지(가장 중요)** · 카드는 아직 등장하지 않았는지 · 탑다운 90°인지
· S06과 같은 표면·조명인지

## S04 · 7.0–9.0s — 폰을 꺼낸다 (빈 플레이트)

**한국어 해설:** 실제 앱 화면을 후반에 합성할 **플레이트 컷**. 화면 내용을 절대 생성하지 않는다.
화면은 균일한 밝은 면으로 비워둔다.

```
over-the-shoulder shot of [TOURIST] holding up a smartphone in one hand, the phone screen faces
the camera and is a completely uniform blank light grey surface with no content whatsoever, just a
clean flat empty screen, gentle screen glow on her cheek, 50mm lens, bright Seoul subway concourse
softly blurred behind her, out-of-focus foreground masses framing left and right edges, [STYLE]
```

**Negative:** `[NEG]` + `no app interface, no icons, no buttons, no text on screen, no notch content,
no reflections showing content, no wallpaper`
**첨부:** A01
**체크:** **화면이 완전히 비어 있는지(필수)** · 손가락 형태가 자연스러운지

## S05 · 9.0–11.0s — 히어로 제스처

**한국어 해설:** 카드 최초 노출. 레퍼런스의 제품 히어로 포즈를 그대로 계승한다 —
**카드를 얼굴 옆, 가슴~머리 높이로 들고 전면을 카메라로**. 얼굴과 카드가 한 프레임에.

```
frontal medium shot of [TOURIST] holding a single vertical payment card up beside her face at
chest-to-head height, the card front squarely facing the camera, her face in the upper third and
the card in the middle third of the vertical frame, bright but restrained genuine smile, eyes toward
the camera, 85mm lens at eye level, soft frontal light plus a warm rim light on her hair, bright
Seoul subway concourse fully melted into creamy bokeh, out-of-focus foreground masses framing both
edges, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no second card, no bent card, no mirrored logo, no invented card text,
no fingers covering the card face`
**첨부:** A01 + **카드 원본 에셋(필수)**
**체크:** 카드가 세로·정면인지 · 카드 로고가 원본과 동일한지(다르면 원본 합성) · 손가락이 카드면을 가리지 않는지

## S06 · 11.0–13.0s — ★핵심: 카드 한 장만 남는다

**한국어 해설:** 이 영상에서 **가장 중요한 컷**. S03과 완전히 같은 구도에서 잡동사니만 사라지고
카드 한 장만 남는다. 말 없이 메시지가 완결된다.

```
top-down 90 degree flat lay on the same milky off-white matte tabletop as the previous flat lay,
identical camera height, identical framing and identical soft diffused overhead lighting, but now
the surface is almost empty: a single vertical blue holographic prepaid card lies alone in the
centre of the frame, nothing else on the table, no wallet, no coins, no other cards, calm and
minimal negative space around it, [CARD], vertical 9:16 framing, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no coins, no banknotes, no other cards, no wallet, no receipts,
no clutter, no shadows of removed objects`
**첨부:** **S03 생성 결과(필수 — 구도 일치용)** + **카드 원본 에셋(필수)** + A03
**체크:** **S03과 프레이밍·조명·표면이 일치하는지(가장 중요)** · 카드 외에 아무것도 없는지

## S07 · 13.0–16.0s — 사용 ①: 개찰구

**한국어 해설:** "지하철에서 쓴다"의 근거. 개찰구 화면에는 **문자를 만들지 않고** 초록 픽토그램만.

```
close-up of a hand tapping a vertical blue holographic prepaid card on the contactless reader on
top of a stainless steel subway fare gate, the reader glowing soft green with a simple green arrow
pictogram only, the flap barrier beginning to open, 50mm lens, the blurred gate housings form large
out-of-focus masses on the left and right edges of the frame, bright cool station light mixed with
daylight, clean metal and glass surfaces, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no text on the reader display, no numbers, no fare amount,
no station signage, no red X, no error state`
**첨부:** A02(로케이션) + 카드 원본 에셋
**체크:** 리더기 화면에 문자가 없는지 · 초록(성공) 상태인지 · 카드가 원본과 일치하는지

## S08 · 16.0–19.0s — 사용 ②: 매장 결제

**한국어 해설:** "카드결제 가능 매장에서 쓴다"의 근거. 매장 브랜드는 식별 불가하게.

```
close-up of a hand holding a vertical blue holographic prepaid card against a small countertop
card payment terminal at a bright convenience store counter, the terminal showing a simple green
check pictogram only, blurred shelves and counter structures forming large out-of-focus masses on
the left and right edges, bright clean daylight-balanced store lighting, 50mm lens, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no store brand, no product packaging text, no price display,
no terminal text, no receipts with text`
**첨부:** 카드 원본 에셋
**체크:** 매장 브랜드·상품 문자가 판독 불가한지 · 단말기에 문자가 없는지

## S09 · 19.0–22.0s — 모션 블러: 가벼운 발걸음

**한국어 해설:** "가벼워졌다"를 대사 없이 몸으로 증명. **지갑은 없고 작은 크로스백만.**
강한 모션 블러로 리듬을 전환한다.

```
[TOURIST] walking lightly and quickly up a subway station staircase seen slightly from behind and
below, wearing only her small crossbody bag with no wallet in her hands, strong natural motion blur
across her body and the handrail conveying light quick movement, bright daylight pouring down from
the top of the stairs as backlight with generously blown highlights, 35mm lens at low eye level,
out-of-focus foreground masses framing the edges, [STYLE]
```

**Negative:** `[NEG]` + `no wallet, no shopping bags, no heavy luggage, no frozen sharp pose`
**첨부:** A01
**체크:** 손에 지갑이 없는지 · 모션 블러가 충분한지 · 역광이 시원하게 날아갔는지

## S10 · 22.0–26.0s — 함께함

**한국어 해설:** 감정의 해소. 레퍼런스의 "눈을 내리깔며 부드럽게 웃는" 함께함 표정을 계승한다.

```
medium two shot of [TOURIST] and a friend of the same age in soft-toned summer clothes stepping
into a subway train together, both smiling softly with eyes gently cast down, relaxed and warm,
the friend slightly less prominent in the frame, 85mm lens, blurred train handrails and a pole
forming out-of-focus masses in the foreground edges, soft daylight coming through the train windows,
[STYLE]
```

**Negative:** `[NEG]` + `no crowded train, no wide laughing mouths, no direct camera stare,
no visible train line numbers`
**첨부:** A01
**체크:** 주인공 의상·헤어가 일관되는지 · 표정이 부드럽고 절제됐는지

## S11 · 26.0–30.0s — 사인오프

**한국어 해설:** 마지막 프레임. **좌상단(로고)과 하단 1/5(워터마크·카피)을 인물과 겹치지 않게 비운다.**
로고·문자는 전부 후반 합성이므로 생성 단계에서는 넣지 않는다.

```
frontal medium shot of [TOURIST] looking straight into the camera with a warm gentle closed-lip
smile, holding the vertical blue holographic prepaid card in one hand at chest height, her figure
placed slightly right of centre so that the upper-left area of the frame stays visually quiet and
empty, the bottom fifth of the frame kept clean and uncluttered, bright backlight with fully melted
bokeh background, 85mm lens at eye level, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no logo, no headline, no copy text, no busy elements in the upper-left area,
no busy elements in the bottom fifth`
**첨부:** A01 + 카드 원본 에셋
**체크:** **좌상단·하단 여백이 확보됐는지(필수)** · 카드가 정면인지 · 시선이 카메라인지

---

## 생성 순서 권장

1. **A01 → 확정** (얼굴·의상이 흔들리면 전부 다시 해야 하므로 여기서 시간을 쓴다)
2. **A02, A03 → 확정**
3. **S03 생성 → 확정** (S06의 기준이 되므로 먼저)
4. **S06 생성** (S03을 레퍼런스로 붙여 구도 일치)
5. 나머지 S01·S02·S04·S05·S07·S08·S09·S10·S11
6. 실패한 컷만 개별 재생성. 전체를 다시 만들지 않는다

## 생성 후 필수 육안 검수

- [ ] 어떤 컷에도 **생성된 문자·로고**가 없다
- [ ] S03의 카드가 전부 **무브랜드**다
- [ ] S04의 폰 화면이 **완전히 비어 있다**
- [ ] 카드 등장 컷(S05·S06·S07·S08·S11)의 카드가 원본 에셋과 일치한다 (다르면 원본 합성)
- [ ] S03과 S06의 프레이밍·조명·표면이 일치한다
- [ ] S11에 좌상단·하단 여백이 있다
- [ ] 손가락 개수·형태가 정상이다
- [ ] 인물 의상·헤어·가방이 전 컷 일관된다
