# 영상 프롬프트 팩 — image-to-video S01~S12

[image-prompts.md](./image-prompts.md)로 만든 키프레임을 **시작 프레임**으로 넣고 아래 모션 프롬프트를 쓴다.
총 30.0초 / 9:16 (1080×1920).

## 공통 원칙

- **카메라는 거의 움직이지 않는다.** 이 편은 정면 고정 축이 척추다. 무브가 들어가면 축이 흔들린다.
  움직임은 **그녀의 제스처**가 담당한다.
- **제스처는 한 클립에 하나만.** 두 동작을 넣으면 둘 다 안 읽힌다.
- **카드가 나오는 컷은 카드를 크게 움직이지 않는다.** 영상 모델이 로고·문자를 뭉갠다.
  카드가 흔들리면 그 컷은 **최소모션으로 다시 뽑고 카드는 후반 합성**한다.
- **네이티브 오디오는 끄고** 뽑는다. 목소리·문장이 생성되면 톤이 깨진다. 소리는 전부 후반에 붙인다.
- **자막·로고·앱화면은 절대 영상 단계에서 만들지 않는다.**

### `[NEG-MOTION]` — 공통 네거티브 모션 (전 컷 필수)

```
no camera shake, no camera pan, no camera tilt, no orbit, no zoom punch, no angle change,
no warping faces, no morphing hands, no changing clothing, no changing hair,
no appearing or disappearing objects, no text appearing, no logo appearing, no card design changing,
no route number appearing on the bus, no extra people walking into frame, no comic effect overlays,
no motion lines, no speech bubbles, no lip sync to words
```

---

## S01 · 2.5s — 설명이 시작된다

| | |
|---|---|
| 카메라 | 완전 고정 |
| 제스처 | 카메라를 향해 손을 흔든다 |
| 사운드 큐 | 도심 앰비언스 |

```
locked static shot with the camera perfectly still. She looks into the lens and waves one hand toward
the camera twice in a bright friendly motion, smiling and leaning in slightly as if starting to tell
her friends something exciting. The blurred foreground shoulders at the left and right edges stay
soft and almost motionless. Background unchanged.
[NEG-MOTION]
```

## S02 · 2.5s — 카드를 들어 보인다

| | |
|---|---|
| 카메라 | 완전 고정 |
| 제스처 | 카드를 얼굴 옆으로 들어올린다 |
| 사운드 큐 | 음악 리프트 |

```
locked static shot. She raises the card up beside her face and holds it there — once it is up, the
card must stay flat, vertical and square to the camera with no tilt, no rotation and no reflection
sweeping across its surface. Her proud smile opens slightly and she blinks once. The card design must
remain pixel-stable and unchanged for the rest of the clip.
[NEG-MOTION]
```

⚠️ 카드를 올리는 동작에서 모델이 카드를 기울이는 경우가 많다. **올린 뒤에는 완전히 정지**시킨다.

## S03 · 2.0s — 검지로 카드를 톡톡

| | |
|---|---|
| 카메라 | 완전 고정 |
| 제스처 | 검지로 카드를 두 번 두드린다 |
| 사운드 큐 | 앰비언스 + 음악 |

```
locked static shot. She taps the face of the card twice with her index finger in a small clear
motion, eyebrows lifting slightly on the second tap. The card itself stays flat and stable — only
the pointing finger moves. Single readable gesture, no other movement.
[NEG-MOTION]
```

## S04 · 2.5s — 허공에 찍는 동작 ★시그니처

| | |
|---|---|
| 카메라 | 완전 고정 |
| 제스처 | 손목을 툭 내려 허공에 찍는 시늉 |
| 사운드 큐 | 후반에 「ピッ」 효과음을 얹는다 |

```
locked static shot. She flicks her wrist downward to mime tapping the card onto an invisible reader
in front of her, holds it there for a beat, then lifts it back up with a pleased playful smile, her
lips rounding briefly as if making a short sound. One single clean tap motion only, not repeated.
No physical reader or terminal ever appears in the frame. The card stays flat and undistorted.
[NEG-MOTION]
```

⚠️ **이 클립이 이 영상의 시그니처다.** 동작이 흐릿하거나 두 번 반복되면 다시 뽑는다.

## S05 · 2.5s — 버스와 지하철을 가리킨다

| | |
|---|---|
| 카메라 | 완전 고정 |
| 시작/끝 프레임 | S05 → **S05b** (아래를 가리키는 프레임) |
| 사운드 큐 | 앰비언스 |

```
locked static shot. She points back over her shoulder toward the road behind her, holds for a beat,
then brings that hand down and points clearly toward the ground. Two distinct gestures with a short
pause between them, never overlapping. The card stays held steady in her other hand throughout.
Her expression stays open and enthusiastic.
[NEG-MOTION]
```

**설정:** 시작 프레임 S05, 끝 프레임 S05b를 함께 넣으면 두 동작이 안정적으로 이어진다.

## S06 · 2.0s — 엄지 척 + 카드 디테일

| | |
|---|---|
| 카메라 | 완전 고정 |
| 제스처 | 엄지를 세우고 고개를 살짝 기울인다 |
| 사운드 큐 | 음악이 가장 밝은 지점 |

```
locked static close-up. She raises her thumb into a small thumbs up and tilts her head very slightly,
her smile softening into quiet confidence, and blinks once. The card stays completely still beside her
face with its surface sharp and its design unchanged. Minimal movement overall.
[NEG-MOTION]
```

## S07 · 2.0s — 버스가 온다

| | |
|---|---|
| 카메라 | 완전 고정 |
| 동작 | 뒤를 돌아본다 → 다시 카메라를 본다 |
| 사운드 큐 | **버스 접근음 → 에어브레이크 「プシュー」** |

```
locked static shot. Behind her a blurred blue mass slides in and settles as the bus pulls up and
stops, staying completely out of focus with no markings ever becoming visible. She stops mid-gesture,
turns her head to glance back over her shoulder, then turns back toward the lens with a small
"oh already?" expression. Her surprise stays small and natural.
[NEG-MOTION]
```

⚠️ 버스가 선명해지면 노선번호가 생성된다. **끝까지 흐릿하게** 유지되는지 확인한다.

## S08 · 2.0s — 다급하게 마지막 설명

| | |
|---|---|
| 카메라 | 완전 고정 |
| 제스처 | 손을 흔들며 뒷걸음질 |
| 사운드 큐 | **문 닫힘 경고음 「ピピピピ…」** |

```
locked static shot. She takes two small steps backward toward the bus while keeping her face toward
the camera, waving one hand urgently and still holding the card up with the other, hurried but
smiling. A soft indicator glow pulses on the blurred bus behind her. Her expression stays bright and
cute, never panicked or grimacing.
[NEG-MOTION]
```

## S09 · 2.0s — 버스가 그녀를 가린다

| | |
|---|---|
| 카메라 | 완전 고정 |
| 동작 | 버스가 프레임을 가로지르며 그녀를 덮는다 |
| 사운드 큐 | 「プシュッ」 + 엔진 회전수 상승 → 「ブロロ…」 |

```
locked static wide shot. The blue city bus sweeps across the frame in front of the shelter, covering
her completely, with strong horizontal motion blur across its body and windows and sky reflections
streaking along the glass. The bus panels stay completely blank throughout — no numbers or markings
ever appear. Steady continuous movement, no sudden acceleration, camera never follows.
[NEG-MOTION]
```

⚠️ 이 클립은 **프레임별로** 버스 문자 생성 여부를 확인한다. 가장 위험한 컷이다.

## S10 · 2.5s — 아무도 없다 ★개그 착지

| | |
|---|---|
| 카메라 | 완전 고정 |
| 동작 | 거의 없음. 정적을 유지한다 |
| 사운드 큐 | **버스 소리 전부 빠지고 도심 앰비언스만. 정적** |

```
locked static wide shot, framed identically to the opening shot, now empty. Nothing moves in the
mid-ground — no people, no bus, nothing enters the frame. Only the faintest breeze in the street
trees and the softest drift in the blurred foreground shoulders. Hold the emptiness and the quiet
for the full duration.
[NEG-MOTION]
```

⚠️ **정적을 충분히 준다.** 여기서 서두르면 웃음이 착지하지 않는다.

## S11 · 4.5s — 제품 인서트 (배경 플레이트)

| | |
|---|---|
| 카메라 | 거의 정지 (아주 느린 드리프트) |
| 사운드 큐 | 음악이 밝게 들어온다 |

```
almost still defocused background plate with only a very slow gentle drift of the creamy bokeh,
like a soft breathing background. Nothing comes into focus, no recognizable shapes form, no people
or vehicles appear. The centre and the lower half stay visually quiet and empty for the whole
duration.
[NEG-MOTION]
```

**전환:** S10에서 **페이드아웃 → 페이드인.** 이 영상의 유일한 페이드로, 개그와 광고를 분리한다.
**후반 합성:** 카드 원본 컷아웃(중앙) + 선행 문구 + 메인 카피 + 각주 + 워터마크

## S12 · 3.0s — 친구들이 폰을 꺼낸다 (CTA)

| | |
|---|---|
| 카메라 | 아주 느린 푸시인 (3초에 3~4%) |
| 동작 | 서로를 보고 끄덕이더니 폰을 함께 본다 |
| 사운드 큐 | 음악 마무리 + 잔향 |

```
extremely slow gentle push-in. The two glance at each other, nod once, and lean in together over the
single phone held between them, both smiling softly with eyes gently cast down. The phone screen stays
a completely uniform blank light grey surface for the entire clip — no content ever appears on it.
The upper-left area of the frame and the bottom fifth stay clean and empty throughout — nothing moves
into them. Settle into stillness at the end.
[NEG-MOTION]
```

⚠️ 좌상단·하단 여백에 **아무것도 들어오지 않아야** 로고·워터마크를 얹을 수 있다.
⚠️ 화면에 무언가 나타나면 그 테이크는 버린다. 실제 앱 화면은 후반 합성이다.

---

## 타임라인 합계

| 컷 | 길이 | 누적 | 비고 |
|---|---|---|---|
| S01 | 2.5s | 2.5 | 정면 와이드 |
| S02 | 2.5s | 5.0 | **카드 최초 노출** |
| S03 | 2.0s | 7.0 | |
| S04 | 2.5s | 9.5 | **시그니처 제스처** |
| S05 | 2.5s | 12.0 | 두 동작 (S05→S05b) |
| S06 | 2.0s | 14.0 | 클로즈업 |
| S07 | 2.0s | 16.0 | 버스 도착 |
| S08 | 2.0s | 18.0 | 경고음 |
| S09 | 2.0s | 20.0 | 버스가 가린다 |
| S10 | 2.5s | 22.5 | **정적 · 개그 착지** |
| S11 | 4.5s | 27.0 | 페이드 후 제품 인서트 |
| S12 | 3.0s | **30.0** | CTA |

## 생성 후 필수 육안 검수

- [ ] **모든 클립의 카메라가 고정이고 앵글이 바뀌지 않았다** (정면 축 유지)
- [ ] **버스에 노선번호·행선지·회사명이 끝까지 나타나지 않는다** (S07·S08·S09 프레임별 확인)
- [ ] S09에서 버스가 끝까지 무문자 상태다
- [ ] S04에 **실제 단말기가 나타나지 않는다** (허공에 찍는 동작 유지)
- [ ] 카드 디자인이 클립 내내 **변하지 않는다** (S02·S03·S04·S05·S06·S08)
- [ ] S12의 폰 화면에 **아무것도 나타나지 않는다**
- [ ] 어떤 클립에도 **문자·로고·말풍선이 생성되지 않았다**
- [ ] S01·S09·S10의 구도가 일치하고 S10이 비어 있다
- [ ] 좌우 전경 어깨가 S01~S10 내내 유지된다
- [ ] 제스처가 클립당 하나씩 명확하게 읽힌다
- [ ] 의상·헤어·가방이 클립 사이에서 바뀌지 않는다
- [ ] 손가락이 뭉개지거나 늘어나지 않았다
- [ ] S11·S12의 좌상단·하단 여백이 끝까지 비어 있다
- [ ] **알아들을 수 있는 목소리가 생성되지 않았다** (네이티브 오디오 끔 확인)
