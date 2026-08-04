# 이미지 프롬프트 팩 — 키프레임 S01~S13

도구 비의존적으로 작성했다. 먼저 **앵커(A01~A04)**를 만들어 확정한 뒤,
그것을 레퍼런스로 붙여 S01~S13을 생성한다.

---

## 공통 토큰

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
Japanese live-action commercial photography, bright airy summer daylight, milky slightly blown
highlights, low saturation pastel grade, soft bloom, vertical 9:16 composition, natural skin texture,
subtle film grain, photorealistic, no CGI gloss
```

### `[NEG]` — 공통 네거티브 (전 컷 필수)

```
no text, no lettering, no subtitles, no captions, no speech bubbles, no logos, no brand marks,
no wordmarks, no watermark, no UI elements, no app screen content, no bus route numbers,
no destination signs, no bus company name, no readable signage, no exaggerated cartoon expression,
no oversaturated colors, no harsh contrast, no plastic CGI skin, no extra fingers,
no deformed hands, no duplicated limbs
```

### `[SENPAI]` — 선배 (주인공, 버스 안) 고정 묘사

```
a Japanese woman in her mid-twenties with a bright cute energy, dark brown medium-length wavy hair
with light see-through bangs, ivory short-sleeve blouse, a coral crossbody bag strap over her
shoulder, minimal accessories
```

### `[KOUHAI]` — 후배 2명 (정류장) 고정 묘사

```
two Japanese women slightly younger, one in a light beige summer blouse and one in a pale blue
short-sleeve top, simple small bags, natural everyday summer styling, visually less prominent
than the main character
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

### `[GLASS]` — 유리 너머 촬영 지시 (S03~S10)

```
seen through the bus window glass, soft reflections of sky and street trees drifting across the
glass surface, but her face and expression stay clearly readable and not obscured by reflections
```

---

# 앵커 (먼저 생성·확정)

## A01 — 캐릭터 락: 선배

```
character reference sheet, three views of the same person side by side: front view,
three-quarter left view, right profile; [SENPAI]; identical hair, identical wardrobe and identical
accessories in all three views; bright friendly expression; plain bright seamless background;
even soft studio light; upper body visible, [STYLE-PLAIN]
```

**Negative:** `[NEG]`
**체크:** 세 뷰가 동일인인지 · 코랄 스트랩 색이 일치하는지

## A02 — 캐릭터 락: 후배 2명

```
character reference sheet, two young women standing side by side, front view and three-quarter view
of each; [KOUHAI]; identical wardrobe across views; calm neutral expressions; plain bright seamless
background; even soft studio light, [STYLE-PLAIN]
```

**Negative:** `[NEG]`
**체크:** 두 사람이 서로 구별되는지 · 의상 색이 일관되는지

## A03 — 로케이션 마스터: 서울 도심 버스 정류장

```
a bus stop shelter on a bright summer street in central Seoul, simple modern shelter with a bench
and a blank unmarked information panel, wide sidewalk, street trees, a pedestrian crossing visible
further along the road, mid-rise city buildings softly blurred behind, bright midday summer daylight,
no people, all signage completely blank and unreadable, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no advertisements, no route maps, no timetable text, no shop signs`
**체크:** 서울 도심으로 읽히는지 · 문자가 전부 비어 있는지

## A04 — 로케이션 마스터: 시내버스 (외부 + 창문)

```
a clean blue city bus stopped at a bus stop, seen at a slight angle from the sidewalk, large side
windows with soft sky and tree reflections on the glass, front door open, the body panels completely
blank with no numbers, no destination display and no company markings anywhere, bright summer
daylight, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no advertising wrap`
**체크:** **버스에 어떤 문자도 없는지(가장 중요)** · 파란 시내버스로 읽히는지 · 창문 반사가 자연스러운지

---

# 본 컷 S01~S13

## S01 · 0.0–2.0s — 정류장에서 기다리는 후배 둘

**한국어 해설:** 장소와 인물을 2초에 세팅. **오른쪽을 비워** 버스가 들어올 자리를 예고한다.

```
medium two shot of [KOUHAI] waiting at a bus stop on a bright summer street in central Seoul,
both standing on the left and centre of the frame with the roadside area on the right kept open and
empty, one of them idly looking at her phone held low, the other glancing down the road, slightly
bored relaxed posture, the blurred bus stop pole and shelter edge forming a large out-of-focus mass
on the left edge, bright midday summer daylight, city buildings melted into bokeh behind them,
35mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no bus in frame, no readable phone screen`
**첨부:** A02(후배), A03(정류장)
**체크:** 오른쪽 여백이 비었는지 · 폰 화면이 판독 불가한지 · 두 사람 의상이 A02와 일치하는지

## S02 · 2.0–4.0s — 버스가 슥 들어온다

**한국어 해설:** 버스가 오른쪽에서 들어와 멈춘다. **버스에 어떤 문자도 없어야 한다.**

```
over-the-shoulder view past [KOUHAI] toward the road as a clean blue city bus pulls in and stops at
the bus stop, the bus entering from the right side of the frame, its body panels completely blank
with no numbers or markings of any kind, bright sky reflecting and sliding across the bus windows,
the shoulders of the two waiting women forming soft out-of-focus masses in the foreground,
bright summer daylight, 35mm lens, [STYLE]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no advertising wrap,
no other vehicles in focus`
**첨부:** A02, A03, A04(버스)
**체크:** **버스 문자 전무(필수)** · 버스가 오른쪽에서 들어오는지

## S03 · 4.0–6.0s — 창문 너머에 선배가 있다

**한국어 해설:** 발견의 순간. **선배는 화면 오른쪽(버스 안)** — 이 좌우 관계를 끝까지 유지한다.

```
[SENPAI] sitting by the window inside the stopped bus, positioned on the right side of the vertical
frame, the bus window frame dividing the composition, she has just noticed her friends outside and
her eyes widen as she leans toward the glass, warm surprised delight, [GLASS], the blurred window
frame and a handrail forming out-of-focus masses at the frame edges, bright summer daylight coming
through the glass, 50mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no other passengers in focus, no reflections covering her eyes`
**첨부:** A01(선배), A04(버스)
**체크:** 선배가 화면 오른쪽인지 · 유리 반사가 눈을 가리지 않는지 · 표정이 읽히는지

## S04 · 6.0–8.0s — 열심히 설명하지만 안 들린다

**한국어 해설:** **이 광고의 엔진이 되는 컷.** 유리에 손바닥을 붙이고 열심히 말하지만 목소리는 닿지 않는다.
접촉이 귀여움을 만든다.

```
medium close-up of [SENPAI] pressed close to the bus window from the inside, one palm flat against
the glass, mouth actively moving as she explains something eagerly, her free hand gesturing busily,
bright and animated but not exaggerated, [GLASS], the glass surface subtly separating her from the
camera, out-of-focus foreground masses at the frame edges, 85mm lens, [STYLE]
```

**Negative:** `[NEG]` + `no speech bubble, no motion lines, no comic effects, no wide open shouting mouth`
**첨부:** A01, A04
**체크:** 손바닥이 유리에 닿아 있는지 · 표정이 절제된 범위인지 · 말풍선·집중선이 없는지

## S05 · 8.0–10.0s — 카드를 자랑스럽게 들어 보인다

**한국어 해설:** 제품 최초 노출. 레퍼런스의 히어로 제스처 — **얼굴 옆, 카드 전면을 카메라로.**
유리 반사가 카드면을 가리지 않게 한다.

```
frontal medium shot of [SENPAI] inside the bus holding a single vertical payment card up beside her
face at chest-to-head height, the card front squarely facing the camera, her face in the upper third
and the card in the middle third of the vertical frame, a bright proud smile as if saying "this one",
[GLASS] but with minimal reflection over the card so the card surface stays clean and sharp,
85mm lens at eye level, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no second card, no bent card, no mirrored logo, no invented card text,
no reflection covering the card face, no fingers covering the card front`
**첨부:** A01, A04 + **카드 원본 에셋(필수)**
**체크:** 카드면이 선명하고 정면인지 · 로고가 원본과 동일한지(다르면 원본 합성) · 얼굴과 카드가 한 프레임인지

## S06 · 10.0–12.0s — 카드 → 버스 → 후배들 가리키기

**한국어 해설:** "이 카드 = 이 버스 = 너희도"를 말 없이 전달. 동작은 한 번에 하나씩 명확하게.

```
medium shot of [SENPAI] inside the bus, holding the card in one hand and pointing at it clearly with
the index finger of her other hand, eyes wide and eyebrows raised as if asking "do you get it?",
her whole gesture readable in one glance, slightly wider framing so both hands are fully inside the
frame, [GLASS], out-of-focus foreground masses at the edges, 50mm lens, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no multiple overlapping gestures, no motion blur on hands, no comic effects`
**첨부:** A01, A04 + 카드 원본 에셋
**체크:** 손동작이 한눈에 읽히는지 · 두 손이 프레임 안에 있는지

## S07 · 12.0–14.0s — 단말기에 찍는다 → 「삑」

**한국어 해설:** **메시지를 증명하는 컷.** 단말기는 무브랜드, 초록 픽토그램만.
태그음 「삑」만 열린 문으로 건너오는 것이 개그의 핵이다.

```
medium close-up from the open front door of the bus showing [SENPAI]'s hand tapping the vertical
blue holographic card onto a small card reader mounted on a pole inside the bus, the reader lit with
a simple green pictogram only and no text anywhere on it, her other hand giving a small thumbs up,
her pleased face partly visible above, the blurred open door frame forming out-of-focus masses at
the frame edges, bright daylight spilling into the bus interior, 50mm lens, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no text on the reader, no numbers, no fare display, no transit brand mark,
no T-money logo, no red error state`
**첨부:** A01, A04 + 카드 원본 에셋
**체크:** **단말기에 로고·문자 전무(필수)** · 초록 성공 상태인지 · 엄지 척이 자연스러운지

## S08 · 14.0–16.0s — 문 닫힘 경고음 시작

**한국어 해설:** 카운트다운 시작. **문 램프가 깜빡인다.** 선배는 다급해지고 후배는 어리둥절.
(리액션 컷백용으로 후배 컷도 별도 생성 — 아래 S08b)

```
medium shot of [SENPAI] inside the bus becoming visibly hurried, leaning closer to the glass and
speeding up her gestures, still holding the card, a small door indicator lamp glowing near the door
edge of the frame, [GLASS], out-of-focus foreground masses at the edges, 50mm lens, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no panic grimace, no comic sweat drops, no motion lines`
**첨부:** A01, A04 + 카드 원본 에셋

### S08b — 후배들 리액션 (컷백용)

```
medium two shot of [KOUHAI] at the bus stop looking up at the bus window with puzzled expressions,
heads slightly tilted, one of them starting to raise a hand uncertainly, mild confusion not shock,
the blurred bus body forming a large out-of-focus mass on the right edge, 50mm lens, [STYLE]
```

**Negative:** `[NEG]` + `no shocked faces, no open mouths, no comic effects`
**첨부:** A02, A04
**체크:** 어리둥절함이 절제됐는지 · 버스가 오른쪽에 있는지(좌우 관계 유지)

## S09 · 16.0–17.0s — 문이 닫힌다 (1초)

**한국어 해설:** **가장 짧은 컷.** 리듬의 정점. 유리에 붙어 마지막으로 외치지만 이제 완전히 안 들린다.

```
tight close-up of [SENPAI]'s face and both palms pressed against the bus window glass from the
inside as she calls out one last time, urgent but still warm and cute, the closing door edge just
entering the frame, [GLASS] with slightly stronger reflections now, bright daylight, 85mm lens,
[STYLE]
```

**Negative:** `[NEG]` + `no distressed crying face, no comic effects, no reflections covering her eyes`
**첨부:** A01, A04
**체크:** 다급함이 귀여운 범위인지 · 표정이 읽히는지

## S10 · 17.0–19.0s — 버스 출발, 여전히 설명 중

**한국어 해설:** 창문이 흘러가며 모션 블러. **멀어지는 창문 너머로 아직도 설명하고 있는 것**이 웃음 포인트.

```
locked wide shot from the sidewalk as the blue city bus pulls away and slides out of the left side
of the frame, natural horizontal motion blur across the bus body and windows, and through one
receding blurred window [SENPAI] is still visibly gesturing and explaining, bright sky reflections
streaking across the glass, the bus panels completely blank, bright summer daylight, 35mm lens,
[STYLE]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no sharp frozen bus`
**첨부:** A01, A03, A04
**체크:** 모션 블러가 충분한지 · 선배가 여전히 설명 중인 게 보이는지 · 버스 문자 전무한지

## S11 · 19.0–21.0s — 텅 빈 정류장 ★개그 착지

**한국어 해설:** **S01과 거의 같은 구도로 돌아온다.** 버스가 사라진 오른쪽 여백이 비어 있고,
후배 둘만 남아 허탈하게 서로를 본다. 정적이 웃음의 착지점.

```
medium two shot of [KOUHAI] left alone at the bus stop, framed almost identically to the earlier
waiting shot with the roadside area on the right now completely empty, both staring off in the
direction the bus went, then glancing at each other with small blank deflated expressions, quiet and
still, the blurred bus stop pole forming an out-of-focus mass on the left edge, bright summer
daylight, 35mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no bus in frame, no laughing, no exaggerated shrug, no other pedestrians in focus`
**첨부:** **S01 생성 결과(필수 — 구도 일치용)** + A02, A03
**체크:** **S01과 프레이밍이 일치하는지(중요)** · 버스가 완전히 없는지 · 표정이 허탈한지

## S12 · 21.0–26.0s — 제품 인서트 (배경 플레이트)

**한국어 해설:** 페이드아웃 후 제품 인서트. **카드와 문자는 전부 후반 합성**이므로
생성하는 것은 **배경 플레이트뿐**이다. 중앙과 하단을 비워둔다.

```
soft defocused background plate of a summer Seoul bus stop and street, everything melted into
creamy pastel bokeh with no recognizable detail, bright milky highlights, gentle warm-to-cool
gradient, the centre and the lower half of the frame kept visually quiet and uncluttered as empty
space, no people, no vehicles in focus, vertical 9:16, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no people, no sharp objects, no busy detail in the centre,
no busy detail in the lower half`
**첨부:** A03
**체크:** 중앙·하단이 비었는지 · 완전히 흐린 보케인지
**후반 합성:** 카드 원본 컷아웃(중앙) + 메인 카피 + 각주 + 워터마크

## S13 · 26.0–30.0s — 후배들이 폰을 꺼낸다 (CTA)

**한국어 해설:** 가이드의 "다음 행동" 요건 충족. **폰 화면은 빈 플레이트**로 생성하고
실제 앱 화면을 후반 합성한다. **좌상단·하단 여백**을 비워 로고와 워터마크 자리를 만든다.

```
medium two shot of [KOUHAI] at the bus stop looking down together at one smartphone held between
them, both smiling softly with eyes gently cast down, warm and relaxed, the phone screen is a
completely uniform blank light grey surface with no content whatsoever, the two women placed
slightly right of centre so the upper-left area of the frame stays visually quiet and empty, the
bottom fifth of the frame kept clean and uncluttered, bright backlight with fully melted bokeh
background, 85mm lens, [STYLE]
```

**Negative:** `[NEG]` + `no app interface, no icons, no text on screen, no logo, no headline,
no busy elements in the upper-left area, no busy elements in the bottom fifth`
**첨부:** A02, A03
**체크:** **폰 화면이 완전히 비었는지(필수)** · **좌상단·하단 여백 확보(필수)** · 표정이 부드러운지

---

## 생성 순서 권장

1. **A01 → 확정** (선배 얼굴·의상이 흔들리면 대부분을 다시 만들어야 한다. 여기서 시간을 쓴다)
2. **A02 → 확정**
3. **A04 → 확정** (버스에 문자가 하나라도 생기면 전부 다시. 여기서 확실히 잡는다)
4. **A03 → 확정**
5. **S01 생성 → 확정** (S11의 구도 기준이 되므로 먼저)
6. **S11 생성** (S01을 레퍼런스로 붙여 구도 일치)
7. 나머지 S02~S10, S08b, S12, S13
8. 실패한 컷만 개별 재생성. 전체를 다시 만들지 않는다

## 생성 후 필수 육안 검수

- [ ] 어떤 컷에도 **생성된 문자·로고**가 없다
- [ ] **버스에 노선번호·행선지·회사명이 없다** (S02·S10 특히)
- [ ] **S07 단말기에 로고·문자가 없고 초록 픽토그램만** 있다
- [ ] S13의 폰 화면이 **완전히 비어 있다**
- [ ] 카드 등장 컷(S05·S06·S07·S08)의 카드가 원본 에셋과 일치한다 (다르면 원본 합성)
- [ ] S01과 S11의 프레이밍이 일치한다
- [ ] **선배는 항상 화면 오른쪽, 후배는 왼쪽** (좌우 관계가 뒤집히지 않았다)
- [ ] 유리 반사가 선배의 눈·표정을 가리지 않는다
- [ ] S12·S13에 좌상단·하단 여백이 있다
- [ ] 말풍선·집중선·만화 효과가 없다
- [ ] 손가락 개수·형태가 정상이다
- [ ] 인물 의상·헤어·가방이 전 컷 일관된다
