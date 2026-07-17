# TOSS 교통카드 AI 광고 릴스 제작 계획 (Higgsfield MCP)

## Context

한국 관광 중인 일본인 여성 관광객이 지하철 개찰구에서 교통카드를 찍는데 삑 소리 대신 호루라기 소리가 나고, 뜬금없이 등장한 축구 심판이 진지한 표정으로 (레드카드 선언하듯) TOSS 카드를 꺼내 개찰구에 찍어주는 개그 광고. 세로형(9:16) 숏폼, 12~15초. 손그림 스토리보드 12컷 + 엔딩컷 기반.

- **톤/색감**: 일본식 시네마틱 + 포카리스웨트 광고 느낌 — 밝고 투명한 자연광, 화이트·시안 계열의 청량한 그레이딩, 소프트 블룸. 심판의 진지함이 웃음 포인트 (데드팬 코미디).
- **언어**: 영상 속 대사·자막은 자연스러운 일본어(음성 + 자막 둘 다). 엔딩 카피는 한국어 메인 + 일본어 병기 (`교통카드는 TOSS로` / `交通カードはTOSSで`). 제작 문서는 전부 한국어로 작성.
- **사용자 결정사항**: ① 토스카드 에셋을 받은 뒤 전체 제작 시작 ② 음성+자막 병행 ③ 엔딩 카피 한·일 병기 ④ 모든 산출물(문서·에셋·클립·최종 영상) 레포에 커밋.

## 스토리보드 해석 (컷 → 클립 매핑)

| 클립 | 스토리보드 컷 | 내용 | 길이 |
|---|---|---|---|
| A | 1–4 | 지하철 개찰구 와이드 → 일본인 관광객(캐리어)이 카드 태그 → 삑 대신 호루라기 "ピピーッ!" + 개찰구 X 표시 → 당황 「え?」 | ~4s |
| B | 5–8 | 호루라기 클로즈업(소리의 정체) → 개찰구 한복판에 뜬금없이 서 있는 축구 심판(흑백 줄무늬, 근엄) → 벙찐 일본인 「えぇ〜!?」 → 심판이 카메라 쪽으로 성큼성큼 | ~4s |
| C | 9–11 | 일본인 프레임에 심판 쑥 들어옴 → 가슴 주머니에서 카드를 꺼냄(일본 게임식 빛나는 이펙트) → TOSS 카드를 레드카드처럼 무언으로 치켜듦 (대사 없이 반짝 효과음만) | ~4s |
| D | 12 + 엔딩 | 손이 프레임인, 개찰구에 카드 띠링! 성공 → 엔딩: 심판이 개찰구를 가리키고 관광객은 말없이 목례 + 카피 `교통카드는 TOSS로 / 交通カードはTOSSで` | ~3s |

대사 원칙: **대사 전면 금지, 감탄사·의성어만 허용**
- 관광객: 「え?」(어?) / 「えぇ〜!?」(에에—?!) — 감탄사만. 엔딩에서는 말없이 가볍게 목례만 (ありがとう도 넣지 않음)
- 심판: **대사 없음** — 호루라기와 카드 제시만으로 연기 (침묵이 데드팬 개그 포인트)
- SFX: 호루라기 ピピーッ, 에러 삑삑, 성공 띠링, 카드 꺼낼 때 게임식 반짝임 효과음

## 카메라 워크 · 장면 전환 설계

컷 리듬은 개그 타이밍이 생명이므로 **하드컷 위주 + 사운드 브리지**로 설계:

| 클립 | 카메라 워크 | 전환 |
|---|---|---|
| A | 와이드 설정샷(고정) → 미드샷 컷인, 태그 순간 **살짝 푸시인**, 개찰구 X 표시 **인서트 컷**, 당황 표정은 정면 클로즈업 | 호루라기 소리가 먼저 들리고 화면이 따라가는 **사운드 브리지**로 B에 연결 |
| B | 휘슬 매크로 클로즈업 **스냅 줌**(집중선 느낌) → 심판 풀샷은 **느린 푸시인**(정적인 뜬금포 강조) → 관광객 리액션 컷백 → 심판 걸어오는 것은 정면 고정 프레임에 인물이 커지는 구도 | B→C는 **휩팬(whip pan)** 또는 하드컷 |
| C | 스토리보드 "Frame in" 그대로 — 고정 프레임에 심판이 **화면 밖에서 쑥 들어옴** → 카드 꺼내는 순간 게임식 스파클 + **미세 슬로모** → 카드 치켜드는 컷은 **로우앵글 히어로샷**(하늘로 치켜든 손) | 카드 제시 정점에서 하드컷 |
| D | 손이 프레임 인 되는 인서트(카드→리더기), 띠링에 맞춰 컷 → 엔딩은 **뒤로 빠지는 와이드**로 개찰구+두 인물+상단 카피 공간 노출 | 띠링 사운드에 맞춘 컷, 엔딩 카피 페이드 인 |

- 세로 9:16 기준 인물 배치: 얼굴·카드가 화면 상단 1/3에 오도록, 자막은 하단 안전영역
- 모션 프롬프트에 위 카메라 지시(push-in, whip pan, low angle, frame-in, slow motion)를 명시

## 장소 일관성 전략

1. **로케이션 마스터샷 고정**: A1(개찰구 와이드, 무인)을 가장 먼저 생성·확정하고, 이 이미지를 **location reference**로 이후 모든 키프레임 생성 시 medias에 첨부 (nano_banana_pro 멀티 레퍼런스: 캐릭터 element + 로케이션 마스터샷 + 카드 에셋 조합)
2. 가능한 컷은 마스터샷을 **편집(이미지 에디팅)으로 파생** — 같은 배경 위에 인물만 배치/변경해 개찰구 디자인·"타는 곳" 표지판·바닥·기둥이 전 컷 동일하게 유지
3. 프롬프트에 장소 고정 토큰 반복: `same subway station as reference, same fare gate design, same "타는 곳" signage`
4. 조명·시간대 고정(아침의 밝은 자연광), 카메라 높이도 컷 표에 맞춰 일관 유지
5. 로케이션 마스터샷도 캐릭터 시트와 함께 **사용자 확정 게이트**에 포함

## 실행 단계

### 0. 에셋 인테이크 (제작 시작 조건)
사용자에게서 토스카드 에셋 수령. 수령 경로(아무거나 가능): ① 이미지 URL → `media_import_url` ② `media_upload_widget`으로 브라우저 업로드 ③ 레포에 커밋 → `media_upload`로 업로드. **에셋 수령 전에는 생성 작업을 시작하지 않음** (문서/레포 세팅은 먼저 진행).

### 1. 사전 준비 (읽기/저비용)
- `get_workflow_instructions()` → 광고(ad/commercial) 워크플로우 카탈로그 확인, 매칭되면 해당 SKILL.md 로드해서 권장 파이프라인 반영
- `balance()` 크레딧 확인, 주요 생성마다 `get_cost:true`로 비용 프리플라이트
- `models_explore`로 최종 모델 파라미터(길이·해상도·오디오 지원) 확정
- 레포 세팅: 브랜치 `claude/toss-transit-card-ad-reel-79odj3`에 `docs/storyboard.md`(위 컷 해석), `docs/production-log.md`(진행 로그) 초기 커밋

### 2. 캐릭터 element 구축 (일관성 확보) — **사용자 확정 게이트**
힉스필드 **element 기능**으로 캐릭터 일관성을 만들고, 다양한 각도 이미지로 element를 보강한다:
1. 캐릭터별 **멀티앵글 캐릭터 시트** 생성 (`nano_banana_pro` / `soul_2`): 정면 · 좌측면 · 우측면 · 3/4 앵글 · 전신 · 상반신 클로즈업 — 동일 인물/의상/조명으로 각도만 변경
   - 일본인 여성 관광객: 20대 후반~30대, 캐주얼 여행복, 기내용 캐리어
   - 축구 심판: 흑백 줄무늬 유니폼, 호루라기, 근엄한 표정
2. **캐릭터 시트를 사용자에게 전달(SendUserFile) → 직접 확인·확정** 받을 때까지 다음 단계 진행하지 않음 (수정 요청 시 해당 앵글만 재생성)
3. 확정된 멀티앵글 이미지로 **element 등록** (`show_characters` Soul 학습 / `show_reference_elements`) → 이후 모든 키프레임·클립 생성에서 이 보강된 element(soul_id/element id)를 레퍼런스로 사용
- **로케이션 마스터샷(A1 와이드)도 이 단계에서 함께 생성·확정** → 이후 모든 컷의 location reference로 사용 (위 '장소 일관성 전략' 참조)

### 3. 컷별 키프레임 이미지 생성 — **프롬프트 선제시 게이트**
- **생성 전에 컷별 프롬프트 전체(아래 초안 기반 최종본)를 사용자에게 먼저 제시하고 컨펌** 받은 뒤 생성 시작
- 클립 A~D의 시작(필요시 끝) 프레임을 `nano_banana_pro`(확정된 element + 토스카드 에셋을 reference media로) 9:16으로 생성
- 카드 등장 컷(10~12)은 반드시 토스카드 에셋을 레퍼런스로 사용
- 게임식 반짝 이펙트, 개찰구 X/O 표시 등 연출 요소 포함

#### 컷별 프롬프트 초안 (실행 시 최종본을 다시 제시하고 컨펌 후 생성)
공통 스타일 서픽스(모든 프롬프트에 부착) — `[STYLE]`:
> Japanese cinematic commercial aesthetic, Pocari Sweat ad color grade, bright airy natural daylight, clean whites with soft cyan-blue tint, soft bloom, film-like grain, vertical 9:16
> *(한국어: 일본식 시네마틱 광고 톤, 포카리풍 청량한 화이트·시안 그레이딩, 세로 9:16)*

**캐릭터 시트 (element 소스)**
- 관광객: `character sheet, Japanese female tourist in her late 20s, casual travel outfit (white blouse, beige skirt), small carry-on suitcase, {front view / left profile / right profile / three-quarter view / full body / upper-body close-up}, neutral expression, plain bright background, consistent identity and outfit, [STYLE]` — *(같은 인물·의상 고정, 중괄호 앵글만 바꿔 6장)*
- 심판: `character sheet, stern middle-aged Korean male soccer referee, black-and-white vertical striped jersey, black shorts, whistle on lanyard, deadpan serious expression, {앵글 6종 동일}, plain bright background, [STYLE]` — *(근엄+무표정이 핵심)*

**키프레임 (nano_banana_pro, element + 필요시 카드 에셋 레퍼런스)**
- A1 (컷1, 개찰구 와이드): `wide shot of a clean Korean subway station fare gates, sign reading "타는 곳" with line number icons, morning commuter light, no people, [STYLE]` — *(무인 개찰구 설정샷)*
- A2 (컷2–4, 태그+당황): `Japanese female tourist [element] tapping a transit card on the subway fare gate reader, gate display showing red X, her face turning puzzled, mouth slightly open saying "え?", small suitcase beside her, [STYLE]` — *(에러 X + 당황 표정)*
- B1 (컷5, 호루라기 클로즈업): `dramatic macro close-up of a silver referee whistle on a lanyard, radial speed lines, sudden reveal feeling, subway station bokeh background, [STYLE]` — *(소리의 정체 등장 컷, 만화식 집중선)*
- B2 (컷6–8, 심판 등장): `stern soccer referee [element] standing absurdly still in the middle of subway fare gates under the "타는 곳" sign, whistle in mouth, deadpan expression, tourist [element] staring in disbelief in foreground edge, [STYLE]` — *(뜬금없는 존재감이 포인트)*
- C1 (컷9, 프레임 인): `over-the-shoulder two shot, referee [element] stepping firmly into frame beside the puzzled tourist [element], subway gates background, [STYLE]`
- C2 (컷10–11, 카드 선언): `referee [element] solemnly pulling a TOSS card [card asset] from his chest pocket and raising it high like a red card, Japanese video-game style sparkle glow effect around the card, deadpan serious face, low angle, [STYLE]` — *(레드카드 판정 패러디, 게임식 반짝임)*
- D1 (컷12, 태그 성공): `close-up of a hand tapping the TOSS card [card asset] on the fare gate reader, reader glowing green with a circle mark, cheerful chime feeling, [STYLE]`
- D2 (엔딩): `referee [element] pointing the way through the open fare gate, tourist [element] bowing slightly in silence, copy space at top for headline, [STYLE]` — *(무언의 목례, 상단에 카피 공간 확보: 교통카드는 TOSS로 / 交通カードはTOSSで)*

**클립별 모션 프롬프트 (image-to-video, 카메라 지시 포함)**
- A: `static wide shot, then cut to mid shot with a subtle push-in as she taps the card, gate buzzes with a shrill whistle sound "ピピーッ" instead of a beep, insert cut of the blinking red X, front close-up as she tilts her head puzzled` — *(푸시인+X 인서트+갸웃)*
- B: `snap zoom macro reveal of the whistle, then slow push-in on the referee standing motionless among the gates, cutback to the tourist's jaw dropping "えぇ〜!?", referee strides toward the locked camera growing larger in frame` — *(스냅줌→느린 푸시인→고정 프레임 접근)*
- C: `locked frame, referee steps in from off-screen, solemnly draws a glowing card from his chest pocket with a game-like sparkle effect and subtle slow motion, low-angle hero shot as he raises it high in silence` — *(프레임 인+미세 슬로모+로우앵글)*
- D: `insert shot of a hand entering frame tapping the card on the reader, pleasant chime "띠링" and green circle, gate opens, camera pulls back to a wide shot as the referee points the way and the tourist bows silently, no speech, headline space at top` — *(띠링 인서트→풀백 와이드 엔딩)*

### 4. 클립 생성 (image-to-video)
- 키프레임 → `kling3_0`(멀티샷·오디오·start/end frame) 또는 `seedance_2_0`(인물 일관성) — 실행 시 `models_explore` 결과로 확정
- 클립당 3~5초 × 4클립, 9:16 (1080×1920), 모델 오디오 생성 지원 시 호루라기/삑/띠링 SFX를 프롬프트에 명시

### 5. 오디오 (대사 없음 — 감탄사·SFX만)
- 비디오 모델 네이티브 오디오로 감탄사(え? / えぇ〜!?)와 SFX(호루라기·삑·띠링·반짝임)를 프롬프트에 명시해 생성 — 문장 대사는 생성 금지
- 감탄사가 어색하게 나오면 해당 클립만 재생성하거나 무음+자막으로 대체 (TTS는 사용하지 않는 것이 기본)

### 6. 어셈블리 + 자막 + 엔딩 카피
- `explainer_video`로 클립 스티칭(+클립별 음성 오버레이, 총 길이 정확히 제어)
- 일본어 자막·한일 병기 엔딩 카피는 내장 자막(라틴계 폰트라 일어/한글 미보장) 대신 **로컬 ffmpeg + Noto Sans JP/KR 폰트로 번인** — 클립 다운로드 → drawtext/ass 자막 → 최종 mp4
- 필요시 `upscale_video`로 화질 보강

### 7. 납품
- `output/final.mp4` + `assets/`(카드·캐릭터 레퍼런스·키프레임) + `clips/`(클립별 mp4) + `docs/production-log.md`(전체 프롬프트와 한국어 해설, job_id, 크레딧 사용 내역) 레포에 커밋
- `git push -u origin claude/toss-transit-card-ad-reel-79odj3`
- 최종 영상은 SendUserFile로도 바로 전달

## 토큰 절약 전략 (과업별 모델 티어링)

메인 모델(Fable)은 창작 판단이 필요한 곳에만 쓰고, 기계적 과업은 **Haiku 서브에이전트**에 위임:

| 과업 | 담당 | 이유 |
|---|---|---|
| 스토리보드 해석·프롬프트 설계·이미지/영상 QC·컷 연출 판단 | 메인 (Fable) | 창작 품질이 결과물을 좌우 |
| 레포 문서 스캐폴딩, production-log 기록, git 커밋/푸시 | Haiku 서브에이전트 | 정형화된 작업 |
| 생성 결과 다운로드, ffmpeg 어셈블리·자막 번인, ffprobe 검증 | Haiku 서브에이전트 | 스크립트 실행 위주 |
| 폰트(Noto Sans JP/KR) 설치 등 환경 준비 | Haiku 서브에이전트 | 단순 셋업 |

추가 절약 수칙: 이미 로드한 MCP 스키마 재로드 금지, 생성 실패 시에만 상세 로그 확인, production-log는 간결하게(프롬프트 원문 + 1줄 한국어 해설), 대형 툴 출력은 요약만 유지.

**codebase-memory-mcp 검토 결과**: 이 서버는 대형 코드베이스를 그래프로 인덱싱해서 "코드 탐색" 토큰을 줄이는 도구입니다. 이 프로젝트는 레포가 사실상 비어 있는 미디어 제작 작업이라 인덱싱할 코드가 없어 절약 효과가 없고, 오히려 MCP 스키마 로딩으로 토큰이 늘어납니다. 이 프로젝트의 토큰 비용은 코드 탐색이 아니라 생성 프롬프트·이미지 QC에서 발생하므로 위의 모델 티어링으로 대응합니다. (나중에 코드가 많은 프로젝트에서 쓰시면 유효합니다 — 원하시면 그때 설치해 드릴게요.)

## 검증
- 각 생성 단계마다 결과물을 다운로드해 사용자에게 공유(SendUserFile)하고 컷별 컨펌 후 다음 단계 진행 (특히 캐릭터 레퍼런스, 카드 클로즈업 컷) — 다운로드·공유 실무는 Haiku 서브에이전트, 판단은 메인 모델
- 최종 영상: 길이 12~15초/9:16 확인(ffprobe), 자막 오탈자·일본어 자연스러움 확인, 휴대폰 세로 재생 기준 텍스트 가독성 확인
- 크레딧: 매 생성 전 get_cost 프리플라이트, production-log에 사용 크레딧 기록

## 리스크 / 대응
- 심판·관광객 얼굴 일관성 흔들림 → 캐릭터 레퍼런스 고정 + 동일 reference media 재사용, 필요시 재생성
- 실사 카드(에셋)의 텍스트/로고 왜곡 → nano_banana_pro(텍스트 강함) 사용, 클로즈업 컷은 에셋 원본을 최대한 유지하는 프롬프트
- 일본어 립싱크 어색 → 대사 컷은 입이 크게 안 보이는 앵글로 연출하거나 TTS+자막 위주로 처리
