# Toss Prepaid Card — Bus Window Dialogue · 영상 생성용 프롬프트

기준 문서: `00FINALSTORYBOARD.md` (12.2초 / 10클립) · `01HIGGSFIELDPROMPTS.md`
키프레임: `frames/` 12장 (01A·01B·02·03·04·05·06·07·08·09·10A·10B)

---

## ⚠️ 먼저 — 생성 길이와 편집 길이는 다르다

편집 맵의 길이(0.6~2.8초)는 **최종 타임라인 길이**다. 영상 모델은 **최소 생성 길이**가 있어서
그대로 뽑을 수 없다.

| 모델 | 최소 길이 |
|---|---|
| seedance_2_0 / mini | **4초** |
| kling3_0 | 3초 |
| wan2_7 / grok_video_v15 | 2초 |

**따라서: 모델 최소 길이로 생성한 뒤 편집에서 잘라 쓴다.**

| 클립 | 편집 길이 | 생성 길이 | 트림 지점 |
|---|---|---|---|
| C01 | 1.4s | 4s | 버스가 정지 완료하는 순간까지 |
| C02 | 0.7s | 4s | 눈이 밝아지는 순간만 (아래 주의 참조) |
| C03 | 0.8s | 4s | 「えっ、先輩!?」 발화 구간 |
| C04 | 0.8s | 4s | 「トス！」 발화 구간 |
| C05 | 0.7s | 4s | 「え？ なに？」 발화 구간 |
| C06 | 1.0s | 4s | 「カード！ カード！」 두 마디 |
| C07 | 0.6s | 4s | 「あ、カード！」 발화 구간 |
| C08 | 0.8s | 4s | 「そう！ ラク〜！」 발화 구간 |
| C09 | 2.6s | 4s | 버스가 완전히 빠질 때까지 |
| C10 | 2.8s | 4s | 착지 후 정지까지 |

**C02 주의:** 프롬프트가 묘사하는 동작(창밖 보기 → 발견 → 눈 밝아짐 → 미소 → 기울임 → 숨 들이마심)은
0.7초에 다 안 들어간다. **편집에서 1.2~1.5초로 늘리거나**, 0.7초를 유지하려면
"눈이 밝아지는 순간" 한 비트만 잘라 쓴다.

## 공통 설정

| 항목 | 값 |
|---|---|
| 권장 모델 | **seedance_2_0** (std) — start/end frame + 네이티브 오디오 + image_references 지원 |
| 화면비 | **9:16** |
| 해상도 | 1080p (초안은 720p / mini) |
| 길이 | **4초** (전 클립 동일하게 뽑고 편집에서 트림) |
| 오디오 | **대사 클립은 ON** (C02~C10). C01은 엔진음만 |

**오디오 판단:** 이 편은 대사가 있으므로 네이티브 오디오를 켠다. 다만 모델의 일본어 발음·립싱크가
어색할 확률이 있다. **어색하면 그 클립만 무음으로 다시 뽑고 대사는 후반에 얹는다** —
어차피 유리창 너머 설정이라 립싱크 정밀도가 낮아도 성립한다.

## 음성 락 (선배가 말하는 모든 컷에 동일하게 반복)

```text
Natural Japanese woman in her mid-twenties, standard Japanese with a subtle Tokyo conversational
cadence, medium pitch, warm and bright, friendly and slightly breathless, never anime-like,
never an announcer, never shrill.
```

## 프레임·제품 레퍼런스 매핑

| 클립 | 시작 프레임 | 끝 프레임 | 카드 레퍼런스 |
|---|---|---|---|
| C01 | `01A-empty-road-start.png` | `01B-bus-arrives-side-end.png` | — |
| C02 | `02-senpai-recognizes.png` | — | — |
| C03 | `03-kouhai-recognizes.png` | — | — |
| C04 | `04-first-toss-call.png` | — | **필요** |
| C05 | `05-kouhai-confused.png` | — | — |
| C06 | `06-card-repeat-closeup.png` | — | **필요** |
| C07 | `07-kouhai-understands.png` | — | — |
| C08 | `08-raku-response.png` | — | **필요** |
| C09 | `09-bus-departs-left.png` | — | — |
| C10 | `10A-empty-center-start.png` | `10B-card-thud-end.png` | **필요** |

**카드 레퍼런스 파일:** 프롬프트 문서는 `references/official-pre-card-black-front.png`로 적고 있다.
이 레포에서는 **`assets/toss-card/pre-card-black-front.png`** 다. 경로만 맞춰 첨부하면 된다.

---

# 클립별 프롬프트

각 블록을 그대로 복붙한다. 대사가 있는 컷에는 위의 **음성 락**을 함께 넣는다.

## C01 · 편집 1.4s — 버스 측면 진입

**Start:** `01A-empty-road-start.png` · **End:** `01B-bus-arrives-side-end.png`

```text
Use the supplied images as the exact start and end frames. Create one locked vertical 9:16 wide shot in bright natural summer daylight. Preserve the exact two younger women seen from behind, their hair, pale-blue and ivory clothing, bags, scale and positions; preserve the bus shelter, trees, buildings, pavement, lane markings, perspective, light and camera.

The road is empty at the start. One clean blue city bus enters from the right edge, travelling laterally toward screen-left. Its long side remains parallel to the camera. It decelerates smoothly and stops precisely in the supplied end-frame position beside the stop. The front of the bus always points left. The bus must drive into frame; it must not fade in, materialize, grow, rotate or transform from the background. The two women remain almost still.

Natural approaching engine and tyre sound only. No dialogue or music. The bus exterior is blank: no route number, destination display, company name, advertisement or transit logo. No camera movement, zoom, shake, background morphing, extra vehicles, pedestrians, subtitles, logos or generated text.
```

## C02 · 편집 0.7s — 선배가 먼저 발견

**Start:** `02-senpai-recognizes.png`

```text
Use the supplied image as the exact first frame. Locked eye-level medium close-up inside the stopped bus. Preserve the exact senior woman, face, dark-brown semi-long hair, ivory blouse, coral crossbody strap, seat, window, daylight, reflections and composition.

She is initially looking casually through the window. She suddenly recognizes her two juniors outside: her eyes brighten, her eyebrows lift slightly, a delighted smile begins and she leans only a few centimetres closer to the glass. Finish with one small natural intake of breath as if she is about to call them. Restrained realistic performance.

No dialogue. Natural stopped-bus ambience only. No card, waving, large mouth, camera movement, face morphing, clothing change, extra passengers, subtitles, logos or generated text.
```

## C03 · 편집 0.8s — 「えっ、先輩!?」

**Start:** `03-kouhai-recognizes.png`

```text
Use the supplied image as the exact first frame. Keep the frontal bus-inside POV and locked camera. Preserve the exact two younger Japanese women, faces, hairstyles, ivory and pale-blue clothing, bags, window frame, summer light, reflection and composition.

Only the woman in the ivory blouse speaks. Her eyes widen slightly, she leans forward a few centimetres and says exactly: 「えっ、先輩!?」 Her delivery is spontaneous, friendly and conversational. The woman in pale blue remains silent and gives one small curious head tilt.

No overlapping voice, exaggerated shock, camera movement, extra people, distorted hands, subtitles, captions, speech bubbles, logos or generated text.
```

## C04 · 편집 0.8s — 「トス！」 (첫 시도)

**Start:** `04-first-toss-call.png` · **제품 레퍼런스 필요**

```text
Use the supplied senior image as the exact first frame and the official black Toss Prepaid Card PNG as the strict product reference. Locked frontal long shot through the closed bus window. Preserve the senior, ivory blouse, coral strap, bus, window geometry, juniors' blurred shoulders, lighting and single card.

The senior keeps the card high in one hand, cups her other hand beside her mouth and calls exactly once: 「トス！」 Use the locked senior voice. She makes one readable presentation gesture of less than three centimetres, then holds the card still. Bright and hopeful, as if she assumes one word will be enough.

The glass softly muffles the voice but the word remains audible. Preserve the exact card proportions, matte black colour, chip, title and white toss mark. No extra dialogue, card bending, rotation, duplicate card, camera movement, subtitles or generated text.
```

## C05 · 편집 0.7s — 「え？ なに？」 (실패)

**Start:** `05-kouhai-confused.png`

```text
Use the supplied image as the exact first frame. Keep the locked frontal view from inside the bus through the closed window. Preserve the two younger women, faces, hair, ivory and pale-blue clothing, bags, positions, window frame, background, reflections and depth of field.

Only the woman in ivory speaks. She keeps one hand gently cupped behind her ear, leans a few centimetres closer and says exactly: 「え？ なに？」 in a quiet, naturally puzzled tone. The woman in pale blue stays silent, tilts her head slightly and briefly glances toward her friend before looking back inside. Hold a tiny blank beat after the line.

Confusion is mild, not shock or slapstick. No card, broad shrug, laughter, camera movement, extra people, subtitles, speech bubbles, logos or generated text.
```

## C06 · 편집 1.0s — 「カード！ カード！」 (반복)

**Start:** `06-card-repeat-closeup.png` · **제품 레퍼런스 필요**

```text
Use the supplied senior image as the exact first frame and the official black Toss Prepaid Card PNG as the strict product reference. Locked frontal close-up through the bus window. Preserve the exact senior, face, hair, ivory blouse, coral strap, window, light, reflections and single card.

She does not lose confidence. The hand holding the card remains stationary, vertical and parallel to the camera. Her other index finger makes two tiny emphatic pointing pulses without covering the printed face. She says exactly: 「カード！ カード！」 Use the locked senior voice. The first word is crisp; the second is slightly more deliberate with a tiny eyebrow lift.

Keep the woman, fingers and card behind the same glass layer. Preserve the exact artwork, chip, title, logo, colour and proportions. No wobble, bending, rotation, duplicate card, extra dialogue, morphing, extra fingers, camera movement, subtitles or generated text.
```

## C07 · 편집 0.6s — 「あ、カード！」 (이해)

**Start:** `07-kouhai-understands.png`

```text
Use the supplied image as the exact first frame. Preserve the locked bus-inside POV, the two younger women, faces, hair, clothing, bags, positions, window frame, background, reflections and light.

Only the woman in ivory speaks. She raises her index finger slightly at chest height, gives a small understanding smile and says exactly: 「あ、カード！」 The woman in pale blue stays silent, straightens her head and completes one tiny confirming nod. Both keep looking at the senior.

Restrained immediate reaction. No card, laughter, large gesture, camera movement, identity change, extra people, subtitles, logos or generated text.
```

## C08 · 편집 0.8s — 「そう！ ラク〜！」 (확정)

**Start:** `08-raku-response.png` · **제품 레퍼런스 필요**

```text
Use the supplied image as the exact first frame and the official card as strict product reference. Locked frontal medium shot through the bus window. Preserve the senior, face, hair, ivory blouse, coral strap, bus interior, window, light, reflections and single official card.

She gives one small affirmative nod, keeps the card steady, holds the existing thumbs-up and says exactly: 「そう！ ラク〜！」 Use the locked senior voice. "そう" is quick and confirming; "ラク〜" is warm, light and gently stretched. Her shoulders relax slightly at the end.

No extra gesture, card rotation, bending, duplicate card, extra dialogue, camera movement, morphing, subtitles, captions or generated text.
```

## C09 · 편집 2.6s — 출발 + 마지막 외침

**Start:** `09-bus-departs-left.png`

```text
Use the supplied image as the exact first frame. Locked vertical 9:16 wide shot. Preserve the blue bus, senior through the window, two juniors from behind, road, buildings, trees, bright summer light and composition.

A brief departure warning begins: 「ピピピ…」 The bus accelerates smoothly toward screen-left and exits completely through the left edge. The bus never reverses. Through the moving window, the senior leans toward the glass, makes one final small wave and calls exactly: 「韓国で、ぜったい使ってみてねー！」 Use the same locked senior voice. Lightly stress 「ぜったい」 and stretch 「ねー」 until she disappears.

Horizontal motion blur appears only on the bus. The juniors, pavement, trees and buildings remain sharp and stationary. The blue body briefly fills most of the screen to create a wipe. No route number, destination, company name, advertisement or transit logo. No camera tracking, pan, zoom, shake, reverse movement, bus deformation, extra vehicles, subtitles or generated text.
```

## C10 · 편집 2.8s — 카드 낙하 + 「ドン」

**Start:** `10A-empty-center-start.png` · **End:** `10B-card-thud-end.png` · **제품 레퍼런스 필요**

```text
Use the supplied empty-road image as the exact start frame, the supplied impact image as the exact end frame, and the official black Toss Prepaid Card PNG as the strict product reference. Locked vertical 9:16 camera. Preserve the road, bus shelter, trees, buildings, crosswalk, light, depth of field and both juniors' blurred shoulders completely still.

Hold the empty centre for the first fraction of a second. One giant rigid official black Toss Prepaid Card drops straight down from just above the top edge. It stays front-facing, vertical and parallel to the camera without rotating, bending or wobbling. It accelerates naturally and lands exactly in the end-frame position. At contact, add one compact low dust puff, two or three tiny pebbles and a short crisp contact shadow. Play one heavy but clean comedic 「ドン」 followed immediately by a bright product chime. Settle into complete stillness.

Preserve the exact matte black surface, rounded corners, chip, "Toss Prepaid Card" title and white toss wordmark throughout. No background movement, camera shake, crater, explosion, excessive debris, bounce out of frame, floating card, duplicated card, extra objects, captions, additional logos or generated text.
```

**폴백:** 배경이 움직이면 그 테이크는 쓰지 않는다. 안전한 대안은 공식 카드 PNG를 `10A` 위에
**2D 레이어로 트래킹 애니메이션**하고, 충돌 순간에 `10B`로 컷하는 것이다.

---

# 편집

## 타임라인 (12.2초)

| 시간 | 클립 | 대사·사운드 |
|---|---|---|
| 0.0–1.4 | C01 | 접근 엔진음 |
| 1.4–2.1 | C02 | 숨 들이마심 |
| 2.1–2.9 | C03 | 「えっ、先輩!?」 |
| 2.9–3.7 | C04 | 「トス！」 |
| 3.7–4.4 | C05 | 「え？ なに？」 |
| 4.4–5.4 | C06 | 「カード！ カード！」 |
| 5.4–6.0 | C07 | 「あ、カード！」 |
| 6.0–6.8 | C08 | 「そう！ ラク〜！」 |
| 6.8–9.4 | C09 | 「韓国で、ぜったい使ってみてねー！」 + 「ピピピ…」 |
| 9.4–12.2 | C10 | 낙하음 + 「ドン」 + 제품 차임 |

## 전환 규칙

- **C04 → C05 → C06은 하드컷.** 디졸브를 쓰지 않는다 (시도–실패–반복 리듬)
- **C09 → C10A는 파란 차체가 프레임을 가장 많이 덮는 순간** 하드컷
- **C10A의 빈 중앙을 0.18~0.25초** 보여준 뒤 카드가 착지해야 한다

## 엔딩 카피 (후반 합성)

카드 착지 후 **6~8프레임 뒤**에 추가한다. **이미지 모델로 글자를 생성하지 않는다.**

```text
韓国旅行、これ一枚でラク。
支払いも、地下鉄も、バスも。
Toss Prepaid Card
```

상단 빈 공간에 배치하고, **카드 표면 위에는 어떤 문구도 얹지 않는다.**

## 후반 합성 목록

| 대상 | 위치 |
|---|---|
| 일본어 대사 자막 | 전 대사 컷 (생성 자막 금지) |
| 엔딩 카피 | C10 착지 후 |
| 공식 로고 | 엔딩 (AI 생성 금지, 공식 파일만) |
| **디스클레이머 워터마크** | **전 구간 하단 상시** (필수) |
| 카드 교체 (필요시) | C04·C06·C08·C10 — 로고가 원본과 다르면 원근 맞춰 합성 |

---

# 검수

## 생성 직후

- [ ] `01A`·`01B`에서 **버스 외의 배경·인물·카메라가 움직이지 않는다**
- [ ] 버스가 **오른쪽 → 왼쪽**으로만 움직인다 (전 클립 방향 일관)
- [ ] 버스 외부에 **노선번호·행선지·회사명·광고·교통 로고가 없다**
- [ ] `02`에서 선배가 후배보다 **먼저** 알아본다
- [ ] `05`가 놀람이 아니라 **"잘 안 들림"**으로 읽힌다
- [ ] `04 → 05 → 06`이 **시도–실패–반복**으로 즉시 이해된다
- [ ] 카드 글자·칩·로고·비율이 모든 프레임에서 유지된다 (다르면 원본 합성)
- [ ] `09`의 버스가 왼쪽으로만 움직이고 배경은 고정된다
- [ ] `10`에서 배경이 움직이지 않는다 (움직이면 2D 합성 폴백)
- [ ] 일본어 발음이 자연스럽다 (어색하면 무음 재생성 + 후반 더빙)
- [ ] 생성된 자막·문자·로고가 없다

## 어셈블리 후

- [ ] `10A`에서 빈 중앙이 **0.18~0.25초** 보인 뒤 카드가 착지한다
- [ ] 총 길이 12.2초 전후, 9:16, H.264 + AAC
- [ ] 대사 7줄이 모두 알아들을 수 있다
- [ ] 휴대폰 세로 재생에서 자막·워터마크 가독성 확인
- [ ] **디스클레이머가 영상 안에서 눈에 보인다**
- [ ] 엔딩 카피가 카드 표면을 가리지 않는다
