# 영상 프롬프트 팩 — image-to-video S01~S11

[image-prompts.md](./image-prompts.md)로 만든 키프레임을 **시작 프레임**으로 넣고 아래 모션 프롬프트를 쓴다.
총 30.0초 / 9:16 (1080×1920) / 컷당 2~4초.

## 공통 원칙

- **모션은 최소로.** 이 릴스의 고급스러움은 화려한 카메라 무브가 아니라 *얕은 심도와 자연광*에서 나온다.
  과한 무브는 톤을 망친다.
- **카드가 나오는 컷은 카드를 크게 움직이지 않는다.** 영상 모델이 로고·문자를 뭉개거나 바꿔버린다.
  카드가 흔들리면 그 컷은 **무음·최소모션으로 다시 만들고 카드는 후반 합성**한다.
- **오디오:** 모델 네이티브 오디오는 참고용으로만 쓰고, 최종 SFX·음악은 후반에 붙인다.
  네이티브 오디오를 끄고 뽑는 편이 안전하다 (사람 목소리 환각 방지).
- **자막·로고는 절대 영상 단계에서 만들지 않는다.**

### `[NEG-MOTION]` — 공통 네거티브 모션 (전 컷 필수)

```
no camera shake, no whip pan, no zoom punch, no warping faces, no morphing hands,
no changing clothing, no changing hair, no appearing or disappearing objects,
no text appearing, no logo appearing, no card design changing, no extra people walking in,
no speaking mouth movement, no lip sync, no subtitles
```

---

## S01 · 2.0s — 훅: 안 닫히는 지갑

| | |
|---|---|
| 시작 프레임 | S01 |
| 끝 상태 | 동전 두세 개가 바닥 쪽으로 떨어져 프레임 아래로 빠진다 |
| 카메라 | 고정. 숨 쉬는 정도의 미세한 흔들림만 |
| 사운드 큐 | 역사 앰비언스 + 동전 「チャリン」 |

```
locked static shot with only a faint breathing micro-movement of the camera. Her hands press the
overstuffed wallet trying to close it and it springs slightly open again. Two or three coins slip
between her fingers and fall down out of the bottom of the frame. The blurred foreground masses at
the left and right edges stay soft and still. Natural light unchanged. No other movement.
[NEG-MOTION]
```

## S02 · 2.0s — 난감한 얼굴

| | |
|---|---|
| 시작 프레임 | S02 |
| 끝 상태 | 작은 한숨과 함께 눈꺼풀이 한 번 내려갔다 올라온다 |
| 카메라 | 아주 느린 푸시인 (2초에 3~4%) |
| 사운드 큐 | 앰비언스 + 작은 한숨 |

```
extremely slow gentle push-in, only three or four percent over the whole clip. She keeps her gaze
down toward her hands below the frame, blinks once slowly, and the corner of her mouth moves into a
small resigned smile. A single faint eyebrow lift. Micro-expression only, nothing theatrical.
Her hair and clothing stay still. Background bokeh unchanged. No mouth opening, no speech.
[NEG-MOTION]
```

## S03 · 3.0s — 플랫레이: 잡동사니

| | |
|---|---|
| 시작 프레임 | S03 |
| 끝 상태 | 손이 동전 무더기를 한 번 헤집고 프레임 밖으로 빠진다 |
| 카메라 | 완전 고정 (탑다운 유지) |
| 사운드 큐 | 동전 부딪히는 소리, 종이 스치는 소리 |

```
completely locked top-down camera, no drift and no rotation. A hand enters from the bottom of the
frame, nudges through the pile of coins so a few coins shift and roll slightly, briefly pushes one
blank card aside, then withdraws out of the bottom of the frame. All objects stay the same objects
throughout — nothing is added and nothing changes appearance. Lighting stays constant.
[NEG-MOTION]
```

⚠️ 이 컷의 카메라가 조금이라도 움직이면 S06과의 매치컷이 깨진다. **완전 고정** 필수.

## S04 · 2.0s — 폰을 꺼낸다 (빈 플레이트)

| | |
|---|---|
| 시작 프레임 | S04 |
| 끝 상태 | 엄지가 화면을 한 번 가볍게 터치한다 |
| 카메라 | 고정 + 미세한 핸드헬드감 |
| 사운드 큐 | 아주 작은 터치음 |

```
near-static handheld feel. She steadies the phone and her thumb taps the screen once, lightly.
The phone screen stays a completely uniform blank light grey surface for the entire clip — no
content ever appears on it, no glow change, no icons, no interface. Her face stays calm and still.
[NEG-MOTION]
```

⚠️ **화면에 무언가 나타나면 그 테이크는 버린다.** 실제 앱 화면은 후반 합성이다.

## S05 · 2.0s — 히어로 제스처

| | |
|---|---|
| 시작 프레임 | S05 |
| 끝 상태 | 카드를 든 손이 살짝 안정되고 미소가 조금 더 열린다 |
| 카메라 | 고정 |
| 사운드 큐 | 음악 리프트 |

```
locked static shot. She holds the card steady beside her face — the card must stay flat, vertical
and square to the camera the entire time, with no tilt, no rotation and no reflection sweep across
its surface. Her smile opens very slightly and she blinks once. Only her hair moves a little.
The card design must remain pixel-stable and unchanged.
[NEG-MOTION]
```

⚠️ 카드가 기울거나 표면 반사가 흐르면 로고가 뭉개진다. **카드는 정지**시킨다.

## S06 · 2.0s — ★핵심: 카드 한 장만

| | |
|---|---|
| 시작 프레임 | S06 |
| 끝 상태 | 카드만 놓인 상태로 정적 유지 (한 박자 쉼) |
| 카메라 | 완전 고정 (S03과 동일) |
| 사운드 큐 | 짧은 스와이프 + 맑은 단음 → **정적** |

```
completely locked top-down camera, identical to the earlier flat lay shot. The single card lies
still in the centre of the empty surface. Almost nothing moves — only the faintest shift of soft
shadow. Nothing enters the frame, nothing is added, the card does not move or change.
Hold the stillness for the full duration.
[NEG-MOTION]
```

**전환 연출 (편집 단계):** S03 → S06은 **매치컷**. 두 컷이 같은 구도이므로, 컷 순간
잡동사니가 사라지고 카드 한 장만 남는 것으로 보인다. 별도 트랜지션 효과를 넣지 않는 편이 강하다.
(대안: S03 끝에서 손이 프레임을 쓸고 지나가는 프레임에 컷을 걸어 "손이 정리한" 느낌으로 붙인다.)

## S07 · 3.0s — 사용 ①: 개찰구

| | |
|---|---|
| 시작 프레임 | S07 |
| 끝 상태 | 플랩이 열리고 그녀가 통과해 프레임을 빠져나간다 |
| 카메라 | 고정 → 통과에 맞춰 아주 짧게 따라감 |
| 사운드 큐 | 「ピッ」 성공음 → 플랩 기계음 |

```
the hand taps the card onto the reader, the reader's green pictogram brightens, the flap barriers
retract smoothly to the sides, and she walks through and out of frame. The camera holds still and
then follows only very slightly. The reader display shows only a simple green pictogram — no text
or numbers ever appear on it. The card stays flat and stable while it is visible.
[NEG-MOTION]
```

## S08 · 3.0s — 사용 ②: 매장 결제

| | |
|---|---|
| 시작 프레임 | S08 |
| 끝 상태 | 결제 완료 후 카드를 거두고 살짝 미소 |
| 카메라 | 고정 → 표정 컷백은 별 클립으로 분리 |
| 사운드 큐 | 결제 완료음 |

```
the hand holds the card to the terminal, the terminal's green check pictogram brightens once,
then the hand lowers the card away. Small natural pause. No text or numbers appear anywhere on the
terminal or the shelves. Store background stays melted and unreadable. Minimal camera movement.
[NEG-MOTION]
```

## S09 · 3.0s — 모션 블러: 가벼운 발걸음

| | |
|---|---|
| 시작 프레임 | S09 |
| 끝 상태 | 계단 위 밝은 빛 쪽으로 올라가며 실루엣이 밝게 날아간다 |
| 카메라 | 뒤따라 올라가는 느낌 (부드러운 팔로우) |
| 사운드 큐 | 발걸음 + 음악 고조 |

```
smooth following movement up the staircase behind her, with strong natural motion blur on her body
and the handrail. She keeps climbing lightly and quickly toward the bright daylight at the top,
her figure gradually washing into the blown-out backlight. Her hands stay empty — she carries only
the small crossbody bag and never holds a wallet. No sudden speed change.
[NEG-MOTION]
```

## S10 · 4.0s — 함께함

| | |
|---|---|
| 시작 프레임 | S10 |
| 끝 상태 | 둘이 나란히 서서 부드럽게 웃는다 |
| 카메라 | 아주 느린 푸시인 |
| 사운드 큐 | 지하철 도착음 + 짧은 웃음 |

```
very slow gentle push-in. The two step in together and settle side by side, both smiling softly
with eyes gently cast down, then one glances briefly at the other. Warm, quiet, unhurried.
Clothing and hair remain consistent. Soft daylight through the windows stays steady.
Mouths may move only as natural soft smiling — no dialogue, no lip sync.
[NEG-MOTION]
```

**대사 옵션:** 짧은 「一緒に行こう」를 넣고 싶다면 **영상 모델로 만들지 말고** 후반에 오디오만 얹는다.
(모델의 립싱크는 어색해질 확률이 높다.)

## S11 · 4.0s — 사인오프

| | |
|---|---|
| 시작 프레임 | S11 |
| 끝 상태 | 카메라를 보며 은은한 미소 유지, 정적으로 마무리 |
| 카메라 | 고정 (또는 거의 감지되지 않는 풀백) |
| 사운드 큐 | 음악 마무리 + 잔향 |

```
locked static shot, or an almost imperceptible pull-back. She holds the card at chest height and
looks into the camera with a warm gentle closed-lip smile, blinking once. The card stays flat,
vertical and square to camera with a stable unchanged design. The upper-left area of the frame and
the bottom fifth stay clean and empty for the whole clip — nothing moves into them.
Settle into stillness at the end.
[NEG-MOTION]
```

⚠️ 좌상단·하단 여백에 **아무것도 들어오지 않아야** 로고·워터마크를 얹을 수 있다.

---

## 타임라인 합계

| 컷 | 길이 | 누적 |
|---|---|---|
| S01 | 2.0s | 2.0 |
| S02 | 2.0s | 4.0 |
| S03 | 3.0s | 7.0 |
| S04 | 2.0s | 9.0 |
| S05 | 2.0s | 11.0 |
| S06 | 2.0s | 13.0 |
| S07 | 3.0s | 16.0 |
| S08 | 3.0s | 19.0 |
| S09 | 3.0s | 22.0 |
| S10 | 4.0s | 26.0 |
| S11 | 4.0s | **30.0** |

## 생성 후 필수 육안 검수

- [ ] 카드 디자인이 클립 내내 **변하지 않는다** (S05·S06·S07·S08·S11)
- [ ] S04의 폰 화면에 **아무것도 나타나지 않는다**
- [ ] S03과 S06의 카메라가 **완전 고정**이고 두 컷 구도가 일치한다
- [ ] 어떤 클립에도 **문자·로고가 생성되지 않았다**
- [ ] 의상·헤어·가방이 클립 사이에서 바뀌지 않는다
- [ ] 손가락이 뭉개지거나 늘어나지 않았다
- [ ] 입 모양이 말하는 것처럼 움직이지 않는다
- [ ] S11의 좌상단·하단 여백이 끝까지 비어 있다
