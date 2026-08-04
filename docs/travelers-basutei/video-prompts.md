# 영상 프롬프트 팩 — image-to-video S01~S13

[image-prompts.md](./image-prompts.md)로 만든 키프레임을 **시작 프레임**으로 넣고 아래 모션 프롬프트를 쓴다.
총 30.0초 / 9:16 (1080×1920).

## 공통 원칙

- **모션은 최소로.** 이 릴스의 고급스러움은 화려한 무브가 아니라 *얕은 심도와 자연광*에서 나온다.
- **카드가 나오는 컷은 카드를 크게 움직이지 않는다.** 영상 모델이 로고·문자를 뭉갠다.
  카드가 흔들리면 그 컷은 **무음·최소모션으로 다시 뽑고 카드는 후반 합성**한다.
- **선배의 대사는 알아들을 수 있게 만들지 않는다.** 입은 움직여도 되지만(유리 너머라 안 들리는 설정),
  **네이티브 오디오는 끄고** 뽑아 목소리 환각을 막는다. 소리는 전부 후반에 붙인다.
- **자막·로고·앱화면은 절대 영상 단계에서 만들지 않는다.**
- **좌우 관계 고정:** 선배는 화면 오른쪽(버스), 후배는 왼쪽(정류장).

### `[NEG-MOTION]` — 공통 네거티브 모션 (전 컷 필수)

```
no camera shake, no whip pan, no zoom punch, no warping faces, no morphing hands,
no changing clothing, no changing hair, no appearing or disappearing objects, no text appearing,
no logo appearing, no card design changing, no route number appearing on the bus,
no extra people walking into frame, no comic effect overlays, no speech bubbles
```

---

## S01 · 2.0s — 정류장에서 기다리는 후배 둘

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 한 명이 차도 쪽으로 시선을 돌린다 |
| 사운드 큐 | 도심 앰비언스 |

```
locked static shot. The two women wait quietly; one keeps idly scrolling her phone held low, the
other shifts her weight and turns her head to look down the road. Slight natural breeze in their
hair. The right side of the frame stays empty — nothing enters it. Background bokeh unchanged.
[NEG-MOTION]
```

## S02 · 2.0s — 버스가 슥 들어온다

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 버스가 정지하고 차체가 살짝 주저앉는다 |
| 사운드 큐 | 접근음 → **에어브레이크 「プシュー」** |

```
locked shot. A blue city bus glides in from the right side of the frame and comes to a smooth stop,
the body settling down very slightly as it halts. Sky reflections slide across its windows as it
moves. The bus panels stay completely blank for the whole clip — no numbers or markings ever appear.
The two women in the foreground stay mostly still, heads turning slightly toward it.
[NEG-MOTION]
```

⚠️ 버스 이동 중 모델이 노선번호를 **그려 넣는 경우가 많다.** 프레임별로 확인한다.

## S03 · 2.0s — 창문 너머에 선배가 있다

| | |
|---|---|
| 카메라 | 아주 느린 푸시인 |
| 끝 상태 | 선배가 유리 쪽으로 몸을 기울인다 |
| 사운드 큐 | 공회전 + 문 열리는 소리 |

```
extremely slow gentle push-in. Inside the bus she notices her friends, her eyes widen slightly and
she leans in toward the window glass, a warm delighted smile spreading. Soft sky and tree reflections
drift slowly across the glass but never cover her eyes. She stays on the right side of the frame.
Minimal other movement.
[NEG-MOTION]
```

## S04 · 2.0s — 열심히 설명하지만 안 들린다

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 손바닥을 유리에 붙인 채 계속 설명 중 |
| 사운드 큐 | 유리에 먹힌 웅얼거림 + 공회전 |

```
locked static shot. She presses one palm flat against the glass and talks eagerly, mouth moving
continuously, her free hand gesturing busily in small readable movements. Bright and animated but
never exaggerated — no shouting grimace. Reflections drift gently on the glass. Her expression stays
clearly readable throughout.
[NEG-MOTION]
```

⚠️ **네이티브 오디오 끄기.** 목소리가 생성되면 "안 들린다"는 설정이 깨진다.

## S05 · 2.0s — 카드를 자랑스럽게 들어 보인다

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 카드를 든 채 미소가 조금 더 열린다 |
| 사운드 큐 | 음악 리프트 |

```
locked static shot. She holds the card steady beside her face — the card must stay flat, vertical and
square to the camera the entire time, with no tilt, no rotation and no reflection sweeping across its
surface. Her proud smile opens very slightly and she blinks once. Only her hair moves a little.
The card design must remain pixel-stable and unchanged.
[NEG-MOTION]
```

⚠️ 카드가 기울거나 유리 반사가 카드면을 지나가면 로고가 뭉개진다. **카드는 정지**시킨다.

## S06 · 2.0s — 카드 → 버스 → 후배들 가리키기

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 후배들을 가리키며 눈썹을 올린다 |
| 사운드 큐 | 웅얼거림 + 공회전 |

```
locked static shot. She points clearly at the card with her index finger, then lifts the same finger
to indicate the bus interior around her, then points toward her friends outside — three distinct
readable beats, one at a time, never overlapping. Eyebrows raised as if asking "do you get it?".
The card stays flat and stable in her other hand throughout.
[NEG-MOTION]
```

## S07 · 2.0s — 단말기에 찍는다 → 「삑」

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 초록 점등 후 엄지 척 |
| 사운드 큐 | **「삑」 (선명하게 건너온다)** |

```
locked shot. Her hand brings the card to the small reader, taps it once, the reader's simple green
pictogram brightens, and she pulls the card back and gives a small pleased thumbs up. No text or
numbers ever appear on the reader. The card stays flat and stable while visible. Single clean action,
no repetition.
[NEG-MOTION]
```

⚠️ 단말기에 **문자·로고가 나타나면 그 테이크는 버린다.**

## S08 · 2.0s — 문 닫힘 경고음 시작

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 다급하게 설명을 서두른다 |
| 사운드 큐 | **문 닫힘 경고음 「ピピピピ…」** |

```
locked shot. Her gestures speed up and she leans closer to the glass, hurrying her explanation while
still holding the card. The small door indicator lamp near the frame edge blinks steadily. Urgency
stays cute and warm, never panicked or grimacing.
[NEG-MOTION]
```

### S08b · 1.0s — 후배들 리액션 (컷백)

```
locked static shot. The two women look up at the bus window, heads tilting slightly, mild puzzled
confusion, one raising a hand uncertainly and letting it drop. Small quiet reactions only.
The blurred bus stays on the right edge of the frame.
[NEG-MOTION]
```

**편집:** S08(2초) 안에 S08b(1초)를 끼워 넣어 **컷백 2회**로 쪼개도 좋다.
그러면 컷이 짧아지는 압박감이 더 살아난다.

## S09 · 1.0s — 문이 닫힌다 (가장 짧은 컷)

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 유리에 붙어 마지막으로 외친다 |
| 사운드 큐 | 「プシュッ」 + 엔진 회전수 상승 |

```
locked tight shot. Both her palms press against the glass as she calls out one last time, mouth
moving urgently, the closing door edge sliding into the frame. Reflections strengthen slightly on
the glass. Urgent but still cute and warm. Very short, single beat.
[NEG-MOTION]
```

## S10 · 2.0s — 버스 출발, 여전히 설명 중

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 버스가 프레임 왼쪽으로 완전히 빠진다 |
| 사운드 큐 | 「ブロロ…」 엔진음이 멀어진다 |

```
locked wide shot. The bus pulls away and slides out of the left side of the frame with strong natural
horizontal motion blur across its body and windows. Through one receding blurred window she is still
visibly gesturing and explaining right until she is out of sight. Sky reflections streak across the
glass. The bus panels stay completely blank throughout. Steady speed, no sudden acceleration.
[NEG-MOTION]
```

## S11 · 2.0s — 텅 빈 정류장 ★개그 착지

| | |
|---|---|
| 카메라 | 고정 |
| 끝 상태 | 서로를 한 번 보고 멈춘다 |
| 사운드 큐 | **버스 소리 전부 빠지고 도심 앰비언스만. 정적** |

```
locked static shot, framed the same as the earlier waiting shot with the right side of the frame now
completely empty. The two women keep staring off in the direction the bus went, hold still for a beat,
then slowly turn to glance at each other with small blank deflated expressions, and settle into
stillness. Nothing enters the frame. Hold the quiet.
[NEG-MOTION]
```

⚠️ **정적을 충분히 준다.** 여기서 서두르면 웃음이 착지하지 않는다.

## S12 · 5.0s — 제품 인서트 (배경 플레이트)

| | |
|---|---|
| 카메라 | 거의 정지 (아주 느린 드리프트) |
| 끝 상태 | 그대로 유지 |
| 사운드 큐 | 음악이 밝게 들어온다 |

```
almost still defocused background plate with only a very slow gentle drift of the creamy bokeh,
like a soft breathing background. Nothing comes into focus, no recognizable shapes form, no people
or vehicles appear. The centre and the lower half stay visually quiet and empty for the whole
duration.
[NEG-MOTION]
```

**전환:** S11에서 **페이드아웃 → 페이드인.** 이 영상의 유일한 페이드로, 개그와 광고를 분리한다.
**후반 합성:** 카드 원본 컷아웃(중앙) + 메인 카피 + 각주 + 워터마크

## S13 · 4.0s — 후배들이 폰을 꺼낸다 (CTA)

| | |
|---|---|
| 카메라 | 아주 느린 푸시인 |
| 끝 상태 | 폰을 보며 부드럽게 웃는다 |
| 사운드 큐 | 음악 마무리 + 잔향 |

```
extremely slow gentle push-in. The two glance at each other, nod once, and lean in together over the
single phone held between them, both smiling softly with eyes gently cast down. The phone screen
stays a completely uniform blank light grey surface for the entire clip — no content ever appears on
it. The upper-left area of the frame and the bottom fifth stay clean and empty throughout — nothing
moves into them. Settle into stillness at the end.
[NEG-MOTION]
```

⚠️ 좌상단·하단 여백에 **아무것도 들어오지 않아야** 로고·워터마크를 얹을 수 있다.
⚠️ 화면에 무언가 나타나면 그 테이크는 버린다. 실제 앱 화면은 후반 합성이다.

---

## 타임라인 합계

| 컷 | 길이 | 누적 | 비고 |
|---|---|---|---|
| S01 | 2.0s | 2.0 | |
| S02 | 2.0s | 4.0 | |
| S03 | 2.0s | 6.0 | |
| S04 | 2.0s | 8.0 | |
| S05 | 2.0s | 10.0 | 카드 최초 노출 |
| S06 | 2.0s | 12.0 | |
| S07 | 2.0s | 14.0 | 「삑」 |
| S08 (+S08b) | 2.0s | 16.0 | 경고음 시작 · 컷백으로 쪼갬 |
| S09 | 1.0s | 17.0 | **가장 짧은 컷** |
| S10 | 2.0s | 19.0 | |
| S11 | 2.0s | 21.0 | **정적 · 개그 착지** |
| S12 | 5.0s | 26.0 | 페이드 후 제품 인서트 |
| S13 | 4.0s | **30.0** | CTA |

## 생성 후 필수 육안 검수

- [ ] **버스에 노선번호·행선지·회사명이 끝까지 나타나지 않는다** (S02·S10 프레임별 확인)
- [ ] **S07 단말기에 문자·로고가 나타나지 않는다**
- [ ] 카드 디자인이 클립 내내 **변하지 않는다** (S05·S06·S07·S08)
- [ ] S13의 폰 화면에 **아무것도 나타나지 않는다**
- [ ] 어떤 클립에도 **문자·로고·말풍선이 생성되지 않았다**
- [ ] **선배가 계속 화면 오른쪽, 후배가 왼쪽**이다
- [ ] 유리 반사가 선배의 눈을 가리지 않는다
- [ ] S01과 S11의 구도가 일치하고 S11의 오른쪽이 비어 있다
- [ ] 의상·헤어·가방이 클립 사이에서 바뀌지 않는다
- [ ] 손가락이 뭉개지거나 늘어나지 않았다
- [ ] S12·S13의 좌상단·하단 여백이 끝까지 비어 있다
- [ ] **알아들을 수 있는 목소리가 생성되지 않았다** (네이티브 오디오 끔 확인)
