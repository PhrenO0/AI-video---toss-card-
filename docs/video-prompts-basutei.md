# 「バス停」篇 영상 프롬프트 — 생성용

이미지 키프레임 → image-to-video. **총 30.0초 / 12클립 / 9:16 (1080×1920)**
전체 기획은 [toss-travelers-basutei.md](./toss-travelers-basutei.md) 참조.

---

## 공통 설정

| 항목 | 값 |
|---|---|
| 화면비 | **9:16** |
| 해상도 | 1080×1920 (모델이 지원하면 1080p, 초안은 720p) |
| 오디오 | **끈다 (generate_audio = false / sound = off)** |
| 길이 | 클립별 아래 표 참조 (2.0~4.5초) |

**오디오를 끄는 이유:** 모델이 목소리·문장을 만들면 톤이 깨진다.
이 영상은 알아들을 수 있는 대사가 없어야 한다. 소리는 전부 후반에 붙인다.

## 네거티브 프롬프트 (전 클립 동일)

네거티브 입력란에 그대로 붙여넣는다. **입력란이 없는 도구라면 프롬프트 맨 끝에 붙인다.**

```
no camera shake, no camera pan, no camera tilt, no orbit, no zoom punch, no angle change,
no warping faces, no morphing hands, no changing clothing, no changing hair,
no appearing or disappearing objects, no text appearing, no logo appearing, no card design changing,
no route number appearing on the bus, no extra people walking into frame, no comic effect overlays,
no motion lines, no speech bubbles, no lip sync to words
```

## 작업 원칙 4가지

1. **카메라는 거의 움직이지 않는다.** 이 편은 정면 고정 축이 척추다. 무브가 들어가면 축이 흔들린다.
   움직임은 **그녀의 제스처**가 담당한다.
2. **제스처는 한 클립에 하나만.** 두 동작을 넣으면 둘 다 안 읽힌다.
3. **카드를 크게 움직이지 않는다.** 모델이 로고·문자를 뭉갠다. 흔들리면 그 클립은
   최소모션으로 다시 뽑고 **카드는 후반 합성**한다.
4. **자막·로고·앱화면은 영상 단계에서 만들지 않는다.** 전부 후반 합성이다.

---

## 시작 프레임 매핑

| 클립 | 길이 | 시작 프레임 | 끝 프레임 | 사운드 큐 (후반) |
|---|---|---|---|---|
| C01 | 2.5s | S01 | — | 도심 앰비언스 |
| C02 | 2.5s | S02 | — | 음악 리프트 |
| C03 | 2.0s | S03 | — | 앰비언스 |
| C04 | 2.5s | S04 | — | **「ピッ」** |
| C05 | 2.5s | S05 | **S05b** | 앰비언스 |
| C06 | 2.0s | S06 | — | 음악 최고점 |
| C07 | 2.0s | S07 | — | **버스 접근음 → 「プシュー」** |
| C08 | 2.0s | S08 | — | **「ピピピピ…」** |
| C09 | 2.0s | S09 | — | 「プシュッ」 + 엔진 상승 |
| C10 | 2.5s | S10 | — | **정적** (버스 소리 전부 빠짐) |
| C11 | 4.5s | S11 (플레이트) | — | 음악 밝게 |
| C12 | 3.0s | S12 | — | 음악 마무리 |

**C05만 끝 프레임을 쓴다.** 두 동작(차도 가리키기 → 아래 가리키기)을 안정적으로 잇기 위해서다.

---

# 클립별 프롬프트

## C01 · 2.5s — 손을 흔든다

```
locked static shot with the camera perfectly still. She looks into the lens and waves one hand toward
the camera twice in a bright friendly motion, smiling and leaning in slightly as if starting to tell
her friends something exciting. The blurred foreground shoulders at the left and right edges stay
soft and almost motionless. Background unchanged.
```

## C02 · 2.5s — 카드를 들어올린다

```
locked static shot. She raises the card up beside her face and holds it there — once it is up, the
card must stay flat, vertical and square to the camera with no tilt, no rotation and no reflection
sweeping across its surface. Her proud smile opens slightly and she blinks once. The card design must
remain pixel-stable and unchanged for the rest of the clip.
```

⚠️ 카드를 올리는 동작에서 모델이 카드를 기울이는 경우가 많다. **올린 뒤에는 완전히 정지**해야 한다.

## C03 · 2.0s — 검지로 톡톡

```
locked static shot. She taps the face of the card twice with her index finger in a small clear
motion, eyebrows lifting slightly on the second tap. The card itself stays flat and stable — only
the pointing finger moves. Single readable gesture, no other movement.
```

## C04 · 2.5s — 허공에 찍는 동작 ★시그니처

```
locked static shot. She flicks her wrist downward to mime tapping the card onto an invisible reader
in front of her, holds it there for a beat, then lifts it back up with a pleased playful smile, her
lips rounding briefly as if making a short sound. One single clean tap motion only, not repeated.
No physical reader or terminal ever appears in the frame. The card stays flat and undistorted.
```

⚠️ **이 클립이 이 영상의 시그니처다.** 동작이 흐릿하거나 두 번 반복되면 다시 뽑는다.
⚠️ 실제 단말기가 나타나면 버린다 — 허공이어야 성립한다.

## C05 · 2.5s — 차도 → 아래를 가리킨다

**시작 S05 · 끝 S05b** (두 프레임을 함께 넣는다)

```
locked static shot. She points back over her shoulder toward the road behind her, holds for a beat,
then brings that hand down and points clearly toward the ground. Two distinct gestures with a short
pause between them, never overlapping. The card stays held steady in her other hand throughout.
Her expression stays open and enthusiastic.
```

## C06 · 2.0s — 엄지 척

```
locked static close-up. She raises her thumb into a small thumbs up and tilts her head very slightly,
her smile softening into quiet confidence, and blinks once. The card stays completely still beside her
face with its surface sharp and its design unchanged. Minimal movement overall.
```

## C07 · 2.0s — 버스가 온다

```
locked static shot. Behind her a blurred blue mass slides in and settles as the bus pulls up and
stops, staying completely out of focus with no markings ever becoming visible. She stops mid-gesture,
turns her head to glance back over her shoulder, then turns back toward the lens with a small
"oh already?" expression. Her surprise stays small and natural.
```

⚠️ 버스가 선명해지면 노선번호가 생성된다. **끝까지 흐릿하게** 유지되는지 확인한다.

## C08 · 2.0s — 뒷걸음질

```
locked static shot. She takes two small steps backward toward the bus while keeping her face toward
the camera, waving one hand urgently and still holding the card up with the other, hurried but
smiling. A soft indicator glow pulses on the blurred bus behind her. Her expression stays bright and
cute, never panicked or grimacing.
```

## C09 · 2.0s — 버스가 그녀를 가린다

```
locked static wide shot. The blue city bus sweeps across the frame in front of the shelter, covering
her completely, with strong horizontal motion blur across its body and windows and sky reflections
streaking along the glass. The bus panels stay completely blank throughout — no numbers or markings
ever appear. Steady continuous movement, no sudden acceleration, camera never follows.
```

⚠️ **가장 위험한 클립.** 버스 문자 생성 여부를 **프레임별로** 확인한다.
반복 실패하면 버스를 더 흐리게 하거나 통과 속도를 올린다.

## C10 · 2.5s — 정적 ★개그 착지

```
locked static wide shot, framed identically to the opening shot, now empty. Nothing moves in the
mid-ground — no people, no bus, nothing enters the frame. Only the faintest breeze in the street
trees and the softest drift in the blurred foreground shoulders. Hold the emptiness and the quiet
for the full duration.
```

⚠️ **정적을 충분히 준다.** 여기서 서두르면 웃음이 착지하지 않는다.

## C11 · 4.5s — 제품 인서트 플레이트

```
almost still defocused background plate with only a very slow gentle drift of the creamy bokeh,
like a soft breathing background. Nothing comes into focus, no recognizable shapes form, no people
or vehicles appear. The centre and the lower half stay visually quiet and empty for the whole
duration.
```

**후반 합성:** 카드 원본 컷아웃(중앙) + 선행 문구 + 메인 카피 + 각주 + 워터마크

## C12 · 3.0s — 폰을 꺼낸다 (CTA)

```
extremely slow gentle push-in. The two glance at each other, nod once, and lean in together over the
single phone held between them, both smiling softly with eyes gently cast down. The phone screen stays
a completely uniform blank light grey surface for the entire clip — no content ever appears on it.
The upper-left area of the frame and the bottom fifth stay clean and empty throughout — nothing moves
into them. Settle into stillness at the end.
```

⚠️ 화면에 무언가 나타나면 버린다. 실제 앱 화면은 후반 합성이다.
⚠️ 좌상단·하단 여백에 아무것도 들어오지 않아야 로고·워터마크를 얹을 수 있다.

---

# 편집 (클립 생성 후)

## 컷 순서와 전환

| 전환 | 방식 |
|---|---|
| C01→C06 | 전부 **하드컷.** 같은 정면 축에서 사이즈만 바뀐다 |
| C06→C07 | **버스 접근음이 먼저 들리고 화면이 따라간다** (사운드 브리지) |
| C07→C09 | 하드컷. 경고음 리듬에 맞춰 조여든다 |
| C09→C10 | 버스가 프레임을 빠져나간 직후 컷 — 소리가 한꺼번에 빠진다 |
| **C10→C11** | **페이드아웃 → 페이드인** (이 영상의 유일한 페이드. 개그와 광고를 분리) |
| C11→C12 | 부드러운 컷 |

## 사운드 설계

- **음악:** C01 가볍게 시작 → C02 리프트 → **C06 가장 밝게** → C07–C09 긴장 →
  **C10 완전히 멈춤** → C11 다시 밝게
- **SFX 순서:** 앰비언스(C01–C06) → **버스 접근음 + 「プシュー」(C07)** →
  **「ピピピピ」(C08)** → 「プシュッ」 + 엔진(C09) → **정적(C10)**
- **대사 없음.** 「ピッ」 같은 짧은 의성어만. 나레이션 없음

## 후반 합성 목록

| 대상 | 클립 | 비고 |
|---|---|---|
| 카드 원본 컷아웃 | C11 | 생성하지 않고 원본 PNG 합성 |
| 카드 교체 (필요시) | C02·C03·C04·C05·C06·C08 | 로고가 원본과 다르면 원근 맞춰 합성 |
| 실제 앱 화면 | C12 | **AI 생성 금지.** JPN 퍼널 스크린샷·녹화 mp4 사용 |
| 공식 로고 | C12 좌상단 (C11 하단도 가능) | **AI 생성 금지.** 공식 파일만 |
| SFX 자막 | C04 「ピッ！」 · C08 「ピピピピ…」 | 귀여운 손글씨풍 |
| 메인 카피 | C11 | 선행 문구 + 메인 2단 |
| 각주 | C11 하단 | 티머니 범위·선불카드 명시 |
| **디스클레이머 워터마크** | **전 구간 하단 상시** | 필수. 눈에 보이는 위치 |

---

# 검수 체크리스트

## 클립별 (생성 직후)

- [ ] **카메라가 고정이고 앵글이 바뀌지 않았다** (정면 축 유지)
- [ ] **버스에 노선번호·행선지·회사명이 끝까지 없다** — C07·C08·**C09 프레임별 확인**
- [ ] C04에 **실제 단말기가 나타나지 않는다** (허공 태그 유지)
- [ ] 카드 디자인이 클립 내내 변하지 않는다 (C02·C03·C04·C05·C06·C08)
- [ ] C12의 폰 화면에 아무것도 나타나지 않는다
- [ ] 어떤 클립에도 **문자·로고·말풍선이 생성되지 않았다**
- [ ] **알아들을 수 있는 목소리가 생성되지 않았다** (오디오 끔 확인)
- [ ] 제스처가 클립당 하나씩 명확하게 읽힌다
- [ ] 손가락이 뭉개지거나 늘어나지 않았다
- [ ] 의상·헤어·가방이 클립 사이에서 바뀌지 않는다

## 어셈블리 후

- [ ] C01·C09·C10의 구도가 일치하고 **C10이 비어 있다**
- [ ] 좌우 전경 어깨가 C01~C10 내내 유지된다
- [ ] C10의 정적이 충분히 길다 (서두르지 않았다)
- [ ] C10→C11 페이드가 유일한 페이드다
- [ ] C11·C12의 좌상단·하단 여백이 비어 있다
- [ ] 총 길이 30초 전후, 9:16, H.264 + AAC
- [ ] 휴대폰 세로 재생에서 자막·워터마크 가독성 확인
- [ ] **디스클레이머가 영상 안에서 눈에 보인다**

## 재생성 원칙

**실패한 클립만 개별 재생성한다.** 전체를 다시 만들지 않는다.
카드가 계속 뭉개지면 그 클립은 **카드를 최소모션으로 두고 후반 합성**으로 해결한다.
