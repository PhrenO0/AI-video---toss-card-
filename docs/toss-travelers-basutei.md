# Toss for Travelers 릴스「バス停」篇 — 통합 제작 문서

작성일: 2026-08-04
상태: 구성 확정(정면 구도) · 프롬프트 팩 완료 · **생성 전 사용자 리뷰 대기**

> 이 문서 하나로 기획부터 프롬프트, 검수까지 전부 다룬다.
> 이전 안 「財布」篇(`docs/travelers-saifu/`)은 폐기되었다.

---

## 목차

- [Part 1. 기획](#part-1-기획)
- [Part 2. 절대 준수 규칙 (컴플라이언스)](#part-2-절대-준수-규칙-컴플라이언스)
- [Part 3. 고정 자산](#part-3-고정-자산)
- [Part 4. 시각 문법](#part-4-시각-문법)
- [Part 5. 제스처 설계](#part-5-제스처-설계)
- [Part 6. 비트시트 (12컷 30초)](#part-6-비트시트-12컷-30초)
- [Part 7. 이미지 프롬프트](#part-7-이미지-프롬프트)
- [Part 8. 영상 프롬프트](#part-8-영상-프롬프트)
- [Part 9. 카피·자막·고지문](#part-9-카피자막고지문)
- [Part 10. 검수 체크리스트](#part-10-검수-체크리스트)
- [Part 11. 작업 순서와 다음 단계](#part-11-작업-순서와-다음-단계)

---

# Part 1. 기획

## 1.1 개요

한국을 여행하는 **일본인 관광객** 대상 **Toss for Travelers(Visitor 서비스)** 홍보 릴스.
세로 9:16, 30초, 12컷. 맥도날드 재팬 인스타 릴스 第二話「踏切」篇의 **연출 구조를 이식**한 오리지널.
토스 Foreigner Bridge Crew 2기 공모전 출품 대비.

**핵심 메시지 (단 하나):**

> 이 카드, 버스도 지하철도 된다. (교통카드로도 쓸 수 있다)

## 1.2 시놉시스

여름 서울 버스정류장. 카메라를 정면으로 바라본 **선배가 친구들에게 토스 카드를 귀여운 제스처로 설명한다.**
카드를 들어 보이고, 허공에 찍는 동작을 하고, 버스와 지하철 방향을 차례로 가리킨다.
그런데 **버스가 들어오면서 시간이 끝난다.** 다급하게 손을 흔들며 마지막까지 설명하다가,
**버스가 프레임을 가로질러 그녀를 가리고**, 지나간 뒤엔 아무도 없다.
남은 정적 — 그리고 **선배가 못 끝낸 설명을 광고가 대신 마무리한다.**

## 1.3 이번 산출물의 범위

- 산출물은 **프롬프트 문서뿐**이다. 이미지·영상 생성은 하지 않는다.
- 오디오 제작, 자막 번인, 어셈블리, 최종 렌더는 **이후 별도 단계**.
- 프롬프트는 **도구 비의존적**으로 작성했다 (GPT Image·Higgsfield 등 어디서든 사용 가능).

## 1.4 레퍼런스 구조의 이식

### 원작「踏切」篇의 구조

1. 귀여운 선배가 후배들에게 버거를 같이 먹자고 하고 싶다
2. 하지만 열차가 와서 **건널목 차단기가 내려가 있다**
3. 기다리는 동안 치즈 등 제품의 매력을 **몸짓과 소리로 귀엽게** 전달한다
4. **열차가 지나가는 화면에서 제품 광고**
5. 열차가 다 가버리자 카메라 앞으로 다가와 "같이 먹자" → 먹는 장면

### 이 광고의 진짜 엔진

**인물이 카메라를 정면으로 보고, 카메라 위치에 있는 상대에게 몸짓으로 제품을 전달한다.**
전경 좌우에 흐릿하게 걸린 어깨가 바로 그 상대다. 차단기나 유리 같은 물리적 장벽은 필수가 아니었다 —
**신나서 손이 바빠지는 것**이 이 광고의 사랑스러움이다.

### 우리식 치환

| 원작 | 우리 |
|---|---|
| 건널목 앞에서 카메라를 향해 「치즈—」 | **정류장 앞에서 카메라를 향해 카드를 설명** |
| 차단기가 내려가 있는 제한 시간 | **버스가 오기 전까지의 제한 시간** |
| 「띵띵띵」 건널목 경보음 | **버스 접근음 → 문 닫힘 경고음** |
| 치즈를 몸짓으로 | **카드 들기 → 허공에 찍는 동작 → 버스·지하철 가리키기** |
| 열차가 화면을 덮으며 제품 광고 | **버스가 프레임을 가로질러 그녀를 가린다 → 제품 인서트** |
| 차단기 열림 → 같이 먹자 | **버스가 지나간 뒤 아무도 없다** (개그 착지) |

**긴장의 방향이 뒤집혔다.** 원작은 열차가 *다가오며* 긴장을 만들지만, 우리는 버스가 *그녀를 데려가려*
하며 만든다. 다급함이 더 크고, "설명을 끝내지 못했다"는 결말이 자연스럽게 나온다.

**장소를 한국으로 바꾼 이유:** 건널목은 일본성의 기호다. 우리 전제는 "일본인이 **한국을** 여행한다"
이므로 배경이 일본처럼 읽히면 전제가 무너진다. 서울 도심 정류장과 시내버스는 한국임이 즉시 읽히고,
버스라서 교통 소구와도 직결된다.

## 1.5 단일 메시지와 가이드 정합성

핵심 메시지 = **"교통카드로도 된다"**. 가이드 추천 각도 중 다음에 해당한다.

> **Payment + transportation:** 결제와 대중교통을 카드 한 장으로 해결

**이 편은 교통에만 집중한다.** 매장 결제 장면은 넣지 않는다 — 기능 나열형으로 흐르는 것을 막기 위해서다.
"결제 카드인데 교통카드로도 된다"는 사실은 카피의 조사(「も」/"도")로만 전달한다.

## 1.6 제품 정보 (표현 정확성 기준)

Toss for Travelers - Visitor 서비스는 한국을 방문한 외국인을 위한 **선불 결제 서비스**다.

- **여권만으로 가입** — ARC·한국 은행 계좌 불필요
- **첫 Visitor 카드 무료**
- **티머니 기능 포함** — 티머니를 지원하는 지하철·버스에서 사용 ← **이 편의 소구점**
- 한국의 카드결제 가능 매장에서 사용
- 토스머니를 충전해 사용

### 표현 금지/허용 대조

| 이렇게 | 이렇게 쓰지 않는다 |
|---|---|
| 티머니 기능으로 지하철·버스를 이용할 수 있어요 | 모든 교통수단에서 조건 없이 쓸 수 있어요 |
| 여권만 있으면 가입할 수 있어요 | 가입하려면 ARC가 필요해요 |
| 첫 Visitor 카드는 무료예요 | 모든 발급·재발급이 항상 무료예요 |
| **선불카드**예요 | 신용카드·체크카드예요 |
| 현금을 많이 들고 다니지 않아도 돼요 | 현금이 전혀 필요 없어요 |

**수치·과장 금지:** "1분 만에", "3초면" 등 검증되지 않은 시간·수치 금지.
"무조건", "100% 안전", "최고의", "다 됩니다" 금지.
**계열사 금지:** 토스뱅크·토스증권 등 계열사 서비스 언급 금지. 브랜드명은 **'토스' / toss**로만.

---

# Part 2. 절대 준수 규칙 (컴플라이언스)

가이드 위반은 공모전 탈락 사유다. 따라서 **프롬프트 단계에서 원천 차단**한다.

| 항목 | 규칙 | 프롬프트 반영 방식 |
|---|---|---|
| **토스 로고** | **AI 생성 절대 금지.** 공식 `toss for travelers` 락업 파일만 후반 합성. 변형·색변경·타그래픽 결합 금지 | 전 컷 로고·문자 네거티브 + S12 **좌상단 여백** 확보 |
| **토스 앱 화면** | **AI 생성 절대 금지.** 제공된 실제 앱 화면만 사용 (JPN 퍼널 스크린샷·녹화 mp4) | S12 폰 화면을 **균일한 빈 플레이트**로 생성 |
| **디스클레이머** | 아래 문구를 **눈에 보이는 위치**에 반드시 삽입 | S11·S12 **하단 여백** 확보 |
| **카드 아트** | 카드 등장 컷은 원본 PNG 첨부. 로고·문자 재그리기 금지 | `[CARD]` 토큰 + 어긋나면 원본 합성으로 교체 |
| **버스·정류장 문자** | 노선번호·행선지·회사명·안내판 문자 전부 생성 금지 | 네거티브 + 배경 버스는 **완전히 흐리게** |
| **타사 비방·비교** | 타 금융사·은행 언급·노출·비교 금지 | 화면에 타사 카드·단말기를 등장시키지 않는다 |
| **자막 번인** | 생성 이미지·영상에 어떤 글자도 넣지 않는다 | 전 컷 자막·말풍선·UI 네거티브 |
| **표현 정확성** | 티머니는 "지원 지하철·버스", 결제는 "카드결제 가능 매장" 범위까지만 | 각주로 범위 명시 |
| **사후 검수** | AI 생성물의 잘못된 명칭·환각 표현 육안 검수 필수 | Part 10 체크리스트 |

**디스클레이머 문구 (제공된 워터마크 이미지 3종 중 선택 — 좌/중앙/우 정렬):**

> 토스 Foreigner Bridge Crew 대외활동으로 콘텐츠 제작을 지원받아 작성된 게시물이며,
> 최종 수상 시 상금 등 혜택을 받을 수 있습니다.

## 이 컨셉에서 특별히 주의할 점

| 위험 | 대응 |
|---|---|
| 버스 노선번호·행선지·회사명이 생성될 수 있다 | 버스 외부 문자 판독 불가. **S09가 가장 위험** — 프레임별 확인 |
| 정류장 안내판·광고판에 문자가 생성될 수 있다 | 안내판은 **비워둔다** |
| "모든 교통수단에서 된다"로 읽힐 수 있다 | 각주로 **"티머니를 지원하는 지하철·버스"** 범위 명시 |
| 그녀의 대사를 자막으로 옮기면 개그가 죽는다 | **자막으로 대사를 옮기지 않는다.** 제스처가 말하게 한다 |
| 제스처가 만화적으로 과장될 수 있다 | 동작은 크게, **표정은 자연스럽게.** 만화 리액션 금지 |

---

# Part 3. 고정 자산

## 3.1 인물 A — 선배 (주인공)

- 일본인 여성, 20대 중반. **밝고 귀여운 에너지.** 동작은 크지만 표정은 자연스럽게
- 다크브라운 세미롱 웨이브, 가벼운 시스루 뱅
- **아이보리 반소매 블라우스**, **코랄 크로스백 스트랩**
- 정류장 앞에 서서 **카메라를 정면으로** 보며 설명한다

## 3.2 인물 B·C — 친구 2명

- **대부분의 컷에서는 전경의 흐린 어깨로만 존재한다** (카메라 위치)
- 마지막 CTA 컷(S12)에서만 얼굴이 나온다
- 담색 여름 옷 (연베이지·라이트블루)

## 3.3 로케이션

- **서울 도심 버스정류장**, 여름 낮, 자연광. **정면 구도**
- 정류장 안내판·광고판은 **비어 있다**
- **파란 시내버스** (간선버스). **노선번호·행선지·회사명 문자 판독 불가**

## 3.4 제품 — Toss Visitor 카드

- 원본: `assets/toss-card/pre-card-hologram-front (1).png` (블루 홀로그램 전면, **세로형**)
- 보조: `assets/toss-card/hand-pre-card-hologram.png` (손에 든 컷 참고)
- **카드 등장 컷(S02·S03·S04·S05·S06·S08)은 원본을 레퍼런스로 첨부** + "로고·문자 재그리기 금지" 명시
- 카드 최초 노출은 **S02**
- **S11 제품 인서트는 카드를 생성하지 않는다** — 배경 플레이트만 만들고 원본 PNG를 컷아웃으로 합성

## 3.5 브랜드 에셋

- 공식 로고: `toss for travelers` 락업 (제공 파일)
- 디스클레이머 워터마크: 좌/중앙/우 정렬 3종 (제공 파일)
- 실제 앱 화면: JPN 퍼널 스크린샷 7종 + 녹화 mp4 3종
  (Registration / Ordering Free Card / Card Activation)

---

# Part 4. 시각 문법

레퍼런스 스크린샷 10장 분석에서 추출했다.

## 4.1 정면 고정 축 ★이 편의 척추

**카메라는 버스정류장을 정면으로 보고, 끝까지 그 축을 벗어나지 않는다.**

- 컷이 바뀔 때 **앵글이 아니라 사이즈만 바뀐다** (와이드 → 미드 → 클로즈업 → 미드 → 와이드)
- **카메라 위치 = 이야기를 듣는 친구들의 위치.** 그녀의 시선은 렌즈를 향한다
- 축이 흔들리지 않아 "누군가에게 설명하는" 느낌이 30초 내내 유지된다

## 4.2 전경 보케 프레이밍 ★최대 특징

화면 **좌·우 가장자리를 초점 밖의 큰 덩어리**가 감싸고, 그 틈으로 피사체를 본다.
레퍼런스에서는 앞에 선 사람들의 머리·어깨가 그 역할을 했다.

- **우리 적용: 이야기를 듣는 친구들의 어깨**를 좌우에 크게 흐리게 → 카메라가 그 사이로 본다.
  이 하나로 "누군가에게 설명하는 상황"이 프레임 안에서 성립한다
- 보조로 정류장 기둥·가로수 잎을 쓴다
- 전경 덩어리는 **완전히 흐리게**, 색은 화면 톤과 같은 계열(밀키 화이트·베이지·연회색)

## 4.3 극도로 얕은 심도

- 피사체만 선명하고 나머지는 크리미한 보케로 녹인다
- 배경 간판·행인·버스는 **형체만 남고 판독 불가**해야 한다 (문자 생성 리스크도 함께 차단)

## 4.4 밝고 통풍감 있는 노출 (밀키 톤)

- **하이라이트가 살짝 날아간** 밝은 노출. 어둡거나 콘트라스트 센 톤은 이 느낌이 아니다
- **낮은 채도, 파스텔.** 원색·비비드 금지
- **소프트 블룸**이 은은하게 번진다
- 여름 정오 직후의 밝은 자연광

## 4.5 제품을 얼굴 옆에 들기 (히어로 제스처)

- 제품과 얼굴이 **한 프레임에 같이** 들어와야 한다. 제품만 클로즈업하는 것과 다르다
- **우리 적용: S02** — 카드 전면을 카메라로 향하게 얼굴 옆에 들기

## 4.6 몸짓·손짓의 귀여움 ★이 편의 핵심

- 동작은 **한 번에 하나씩 명확하게.** 여러 동작을 겹치면 안 읽힌다
- 손이 프레임 안에 완전히 들어오도록 사이즈를 잡는다
- 표정은 밝고 크지만 **과장되지 않게**

## 4.7 모션 블러 컷

- 리듬의 전환점 역할. **우리 적용: S09** — 버스가 프레임을 가로지르며 그녀를 가리는 순간

## 4.8 그래픽 인서트 카드

실사 위에 **플랫 디자인 오버레이**를 얹은 프레임. 레퍼런스에서는 기간 배지 + 제품 컷아웃 +
큰 제품명·가격 + **하단의 작은 고지문**으로 구성됐다.

- **우리의 법적 고지가 들어갈 자리**가 이 구조다
- **우리 적용: S11** — 카드 컷아웃 + 카피 + 각주 + 워터마크

## 4.9 함께함 비트

- 눈을 내리깔며 부드럽게 웃는 따뜻한 보케 컷
- **우리 적용: S12** — 전경의 흐린 어깨였던 친구들이 처음 얼굴을 드러내며 폰을 함께 본다

## 4.10 마지막 프레임 구조

- 레퍼런스: 주인공이 카메라를 보며 웃고, 제품을 들고, **로고가 좌상단에 플랫 오버레이**
- **우리 적용: S12** — 좌상단 로고, 하단 워터마크. 두 영역은 **인물과 겹치지 않게 비운다**

## 4.11 프레이밍 규칙

- 세로 **9:16** (1080×1920)
- **그녀는 화면 중앙**, 얼굴은 **상단 1/3**, 카드는 **중앙 1/3**
- 하단 1/5은 자막·워터마크 안전영역으로 비운다
- 정면 축을 유지하되 사이즈만 바꾼다. **컷마다 카메라 높이를 바꾸지 않는다**
- 버스는 **뒤쪽 차도에서 들어와 프레임을 가로지른다** (방향을 컷 사이에서 뒤집지 않는다)

## 4.12 자연스러운 표정 연기

- **과장된 만화적 리액션 금지** — 입을 크게 벌리거나 눈을 튀어나오게 하지 않는다
- 제스처는 크게, **표정은 자연스럽게** — 이 균형이 귀여움의 조건이다

---

# Part 5. 제스처 설계

말이 아니라 손이 설명한다. **동작은 한 번에 하나씩 명확하게.** 겹치면 읽히지 않는다.

| 순서 | 제스처 | 전달 내용 | 컷 |
|---|---|---|---|
| ① | 카메라를 향해 손을 흔들며 눈을 맞춘다 | "얘들아, 들어봐" | S01 |
| ② | **카드를 얼굴 옆에 들어 정면으로** | "이거 봐" (제품 최초 노출) | S02 |
| ③ | 검지로 카드를 톡톡 두드린다 | "이거야" | S03 |
| ④ | **허공에 카드를 찍는 동작** + 「ピッ！」 입모양 | "찍으면 돼" ★시그니처 | S04 |
| ⑤ | 뒤 차도를 가리킨다 → 아래를 가리킨다 | "버스도, 지하철도" | S05 |
| ⑥ | 엄지 척 + 고개를 살짝 기울인다 | "좋지?" | S06 |
| ⑦ | 다급하게 손을 흔들며 뒷걸음질 | "아 잠깐만—" | S08 |

**④가 이 광고의 시그니처 제스처다.** 허공에 손목을 툭 내려 찍는 시늉은 귀엽고, 한눈에 읽히고,
**그 자체가 제품의 소구점**이다. 「치즈—」가 제품 재료이면서 사진 찍는 말이었던 것과 같은 구조다.

**⑤는 카피와 1:1로 대응한다.** 뒤 차도를 가리키고("버스도") 아래를 가리키는 동작이
메인 카피 「バスも、地下鉄も、これ一枚。」와 정확히 맞물린다.

---

# Part 6. 비트시트 (12컷 30초)

## 6.1 전체 리듬 — 설명이 쌓이다가 버스에 끊긴다

| 구간 | 컷 | 역할 | 템포 |
|---|---|---|---|
| 설명 | S01–S06 | 귀여운 제스처로 카드를 설명한다 | 2~2.5초씩 (여유롭고 리드미컬) |
| **압박** | S07–S09 | 버스 접근 → 경고음 → 가려짐 | **2초씩 조여든다** |
| 착지 | S10 | 아무도 없다. 정적 | 2.5초 (길게 느껴진다) |
| 광고 | S11–S12 | 제품 인서트 → CTA | 4.5초 + 3초 |

**설계 의도:** S01–S06에서 설명이 즐겁게 쌓인다. S07에서 버스 소리가 들어오며 마감이 생기고,
S09에서 버스가 그녀를 가린다. **S10의 정적이 웃음의 착지점**이다. 이 정적을 충분히 주는 것이 중요하다.

## 6.2 긴장감 설계 (원작 「띵띵띵」의 대응)

**소리가 먼저 오고 그녀가 반응한다.** 이 순서가 지켜져야 관객이 그녀보다 먼저 눈치챈다.

| 시점 | 소리 | 시각 |
|---|---|---|
| S07 앞 | **버스 접근음이 뒤에서 서서히 커진다** | 아직 모르고 설명 중 |
| S07 | 에어브레이크 「プシュー」 | 뒤를 돌아본다 — 카운트다운 시작 |
| S08 | **문 닫힘 경고음 「ピピピピ…」** | 다급하게 마지막 설명. 문 램프 점멸 |
| S09 | 「プシュッ」 + 엔진 회전수 상승 | 버스가 프레임을 가로지른다 |
| S10 | **전부 빠지고 도심 앰비언스만** | 텅 빈 정류장 |

## 6.3 컷별 설계

### S01 · 0.0–2.5s — 설명이 시작된다 (정면 와이드)

| 항목 | 설계 |
|---|---|
| 카메라 | **정면 와이드.** 35mm, 눈높이. 고정 |
| 프레이밍 | 그녀가 정류장 앞 **화면 중앙**. 뒤로 정류장과 차도 |
| 전경 보케 | **좌우에 친구들의 어깨**를 크게 흐리게 ★이 편의 기본 구도 |
| 조명 | 여름 정오 직후 자연광. 밝고 통풍감 있게 |
| 제스처 | ① 손을 흔들며 눈을 맞춘다 |
| 표정 | 밝고 신남. 뭔가 알려주고 싶어 못 참는 얼굴 |
| 오디오 | 도심 앰비언스 (차량·매미·먼 신호음) |
| 자막 | 없음 |
| 의도 | 장소·인물·관계를 2.5초에 세팅. **정면 축과 전경 어깨를 여기서 확립** |

### S02 · 2.5–5.0s — 카드를 들어 보인다 ★제품 최초 노출 (정면 미드)

| 항목 | 설계 |
|---|---|
| 카메라 | **정면 미드샷.** 50mm, 눈높이. 고정 (앵글 그대로, 사이즈만 조임) |
| 프레이밍 | 얼굴 상단 1/3, **카드 중앙 1/3** |
| 제스처 | ② 카드를 얼굴 옆, 가슴~머리 높이로 들고 전면을 카메라로 |
| 표정 | "이거 봐!" 하는 밝은 자부심 |
| ⚠️ 제품 | **카드 원본 첨부 필수. 로고·문자 재그리기 금지** |
| 오디오 | 앰비언스. 음악이 살짝 올라온다 |
| 자막 | 없음 (카드가 말한다) |

### S03 · 5.0–7.0s — 검지로 카드를 톡톡 (정면 미드)

| 항목 | 설계 |
|---|---|
| 카메라 | 정면 미드샷 유지. 50mm |
| 제스처 | ③ 검지로 카드를 톡톡. "이거야" |
| 표정 | 눈썹을 살짝 올리며 강조 |
| 오디오 | 앰비언스 + 음악 |
| 자막 | 없음 |

### S04 · 7.0–9.5s — 허공에 찍는 동작 ★시그니처 (정면 미드)

| 항목 | 설계 |
|---|---|
| 카메라 | 정면 미드샷. 두 손이 프레임에 완전히 들어오게 살짝 넓게 |
| 제스처 | ④ **카드를 허공에 대고 손목을 툭 내려 찍는 시늉.** 「ピッ！」 입모양 |
| 표정 | 장난스럽고 뿌듯하게 |
| ⚠️ | **실제 단말기가 프레임에 없어야 한다.** 허공이어야 성립 |
| 오디오 | 앰비언스. 후반에 「ピッ」 효과음을 얹는다 |
| 자막 | SFX 자막 「ピッ！」 (귀여운 손글씨풍) |
| 의도 | **이 광고의 시그니처.** 「치즈—」의 대응 |

### S05 · 9.5–12.0s — 버스와 지하철을 가리킨다 (정면 미드)

| 항목 | 설계 |
|---|---|
| 카메라 | 정면 미드샷 유지 |
| 제스처 | ⑤ 뒤쪽 차도를 가리킨다("버스도") → 손을 내려 아래를 가리킨다("지하철도") |
| 동작 원칙 | **한 번에 하나씩.** 두 동작 사이에 짧은 멈춤 |
| 표정 | "둘 다 돼!" |
| 오디오 | 앰비언스 |
| 자막 | 없음 |
| 의도 | 카피 「バスも、地下鉄も」와 제스처가 1:1 대응 |

### S06 · 12.0–14.0s — 엄지 척 + 카드 디테일 (정면 클로즈업)

| 항목 | 설계 |
|---|---|
| 카메라 | **정면 클로즈업.** 85mm. 축 그대로, 사이즈만 조임 |
| 프레이밍 | 얼굴과 카드를 든 손이 가깝게. 카드 표면 디테일이 보인다 |
| 제스처 | ⑥ 엄지 척 + 고개를 살짝 기울인다 |
| 표정 | 부드럽고 자신 있게 |
| ⚠️ 제품 | 카드 원본 첨부. **이 컷에서 카드가 가장 크게 보인다** |
| 오디오 | 음악이 가장 밝은 지점 |
| 자막 | 없음 |

### S07 · 14.0–16.0s — 버스가 온다 (정면 미드)

| 항목 | 설계 |
|---|---|
| 카메라 | 정면 미드샷으로 되돌아온다 |
| 시각 | 뒤쪽 차도에 **버스가 들어와 정지** (흐리게, 형체만) |
| 제스처 | 말하다 멈추고 **뒤를 돌아본다** → 다시 카메라를 본다 |
| 표정 | "아, 벌써?" 하는 당황이 살짝 |
| 오디오 | **버스 접근음이 커진다** → 에어브레이크 「プシュー」 |
| 자막 | 없음 |
| 의도 | **소리가 먼저 오고 그녀가 반응한다.** 관객이 먼저 눈치챈다 |

### S08 · 16.0–18.0s — 다급하게 마지막 설명 (정면 미드)

| 항목 | 설계 |
|---|---|
| 카메라 | 정면 미드샷 |
| 제스처 | ⑦ **손을 흔들며 뒷걸음질**로 버스 쪽으로. 그러면서도 카드를 계속 들어 보인다 |
| 표정 | 다급하지만 여전히 밝게 |
| 시각 | **문 램프가 깜빡인다** (흐리게) |
| 오디오 | **문 닫힘 경고음 「ピピピピ…」** |
| 자막 | SFX 자막 「ピピピピ…」 |

### S09 · 18.0–20.0s — 버스가 그녀를 가린다 (정면 와이드)

| 항목 | 설계 |
|---|---|
| 카메라 | **정면 와이드.** S01과 같은 사이즈로 돌아온다. 고정 |
| 동작 | 버스가 **프레임을 가로질러** 들어오며 그녀를 완전히 가린다. 강한 수평 모션 블러 |
| ⚠️ 컴플라이언스 | **버스 문자 생성 금지. 이 컷이 가장 위험하다** — 프레임별 확인 |
| 오디오 | 「プシュッ」 + 엔진 회전수 상승 → 「ブロロ…」 |
| 자막 | 없음 |
| 의도 | 원작의 "기차가 지나가는 화면"의 대응 |

### S10 · 20.0–22.5s — 아무도 없다 ★개그 착지 (정면 와이드)

| 항목 | 설계 |
|---|---|
| 카메라 | **S01·S09와 완전히 같은 정면 와이드.** 고정 |
| 변화 | 버스가 지나간 뒤 **정류장에 아무도 없다.** 그녀가 사라졌다 |
| 전경 | 친구들의 어깨는 여전히 좌우에 걸려 있다 (그들은 남았다) |
| 오디오 | **모든 버스 소리가 빠지고 도심 앰비언스만.** 정적을 충분히 |
| 자막 | 「…」 정도 |
| 의도 | **웃음의 착지점.** S01과 같은 구도로 돌아와 "설명이 끝나지 않았다"가 완성된다 |

### S11 · 22.5–27.0s — 제품 인서트 (페이드아웃 후)

| 항목 | 설계 |
|---|---|
| 전환 | S10에서 **페이드아웃** → 제품 인서트로. 이 영상의 유일한 페이드 |
| 구성 | 흐린 실사 배경 위에 **카드 컷아웃 + 카피 + 각주** 플랫 오버레이 |
| 레이아웃 | 카드 중앙, 카피 그 아래, 각주 하단 작게 |
| ⚠️ 제품 | 카드는 **원본 에셋을 그대로 합성**한다 (생성하지 않는다) |
| 오디오 | 음악이 밝게 들어온다 |
| 의도 | **선배가 못 끝낸 설명을 광고가 대신 마무리한다** |

### S12 · 27.0–30.0s — 친구들이 폰을 꺼낸다 (CTA)

| 항목 | 설계 |
|---|---|
| 카메라 | 미드 투샷. 85mm. 아주 느린 푸시인 |
| 반전 | **전경의 흐린 어깨로만 존재했던 친구들이 처음 얼굴을 드러낸다** |
| 동작 | 서로를 보고 끄덕이더니 **폰을 꺼내 함께 들여다본다** |
| 화면 | **폰 화면은 빈 플레이트** → 실제 앱 화면 후반 합성 |
| 여백 | **좌상단(로고), 하단 1/5(워터마크·CTA)** 을 인물과 겹치지 않게 비운다 |
| 오디오 | 음악 마무리 + 잔향 |
| 의도 | 가이드의 "다음 행동" 요건 충족. **듣던 사람이 움직였다**는 마무리 |

## 6.4 전환 설계

| 전환 | 방식 |
|---|---|
| S01→S06 | 전부 **하드컷.** 같은 정면 축에서 사이즈만 바뀐다 |
| S06→S07 | **버스 접근음이 먼저 들리고 화면이 따라간다** (사운드 브리지) |
| S07→S08 | 하드컷. 경고음에 맞춰 |
| S08→S09 | 하드컷 |
| S09→S10 | 버스가 프레임을 빠져나간 직후 컷 — 소리가 한꺼번에 빠진다 |
| **S10→S11** | **페이드아웃 → 페이드인** (유일한 페이드. 개그와 광고를 분리) |
| S11→S12 | 부드러운 컷 |

## 6.5 오디오 총괄

- **음악:** 밝고 귀여운 여름 톤. S01 가볍게 시작 → S02 리프트 → **S06 가장 밝게** →
  S07–S09 긴장 → **S10 완전히 멈춤** → S11 다시 밝게
- **SFX 순서:** 앰비언스(S01–S06) → **버스 접근음+「プシュー」(S07)** →
  **「ピピピピ」(S08)** → 「プシュッ」+엔진(S09) → **정적(S10)**
- **대사:** 알아들을 수 있는 대사는 없다. 「ピッ！」 같은 짧은 의성어만 허용
- **나레이션 없음**

---

# Part 7. 이미지 프롬프트

**대원칙:** 전 컷이 **정면 고정 축**이다. 컷마다 앵글이 아니라 **사이즈만** 바뀐다.
좌우 가장자리에는 항상 **이야기를 듣는 친구들의 어깨**가 흐리게 걸린다.

## 7.1 공통 토큰

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

## 7.2 앵커 (먼저 생성·확정)

### A01 — 캐릭터 락: 주인공

```
character reference sheet, three views of the same person side by side: front view,
three-quarter left view, right profile; [SENPAI]; identical hair, identical wardrobe and identical
accessories in all three views; bright friendly expression; plain bright seamless background;
even soft studio light; upper body visible, [STYLE-PLAIN]
```

**Negative:** `[NEG]` · **체크:** 세 뷰가 동일인인지 · 코랄 스트랩 색이 일치하는지

### A02 — 캐릭터 락: 친구 2명

```
character reference sheet, two young women standing side by side, front view and three-quarter view
of each; [FRIENDS]; identical wardrobe across views; calm neutral expressions; plain bright seamless
background; even soft studio light, [STYLE-PLAIN]
```

**Negative:** `[NEG]` · **체크:** 두 사람이 서로 구별되는지 · 의상 색이 일관되는지

### A03 — 로케이션 마스터: 서울 도심 버스정류장 (정면)

**해설:** **이 앵커가 전 컷의 배경 기준이다.** 정면 축을 여기서 확정한다.

```
straight-on frontal view of a bus stop shelter on a bright summer street in central Seoul, seen from
the sidewalk directly facing it at eye level, simple modern shelter with a bench and a completely
blank unmarked information panel, wide pavement, street trees, mid-rise city buildings softly blurred
behind, a road visible behind the shelter, bright midday summer daylight, no people,
all signage completely blank and unreadable, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no advertisements, no route maps, no timetable text, no shop signs, no people`
**체크:** **완전한 정면인지** · 서울 도심으로 읽히는지 · 안내판이 비었는지

### A04 — 로케이션 마스터: 시내버스

```
a clean blue city bus on a summer city street, seen from the side, large windows with soft sky and
tree reflections, the body panels completely blank with no numbers, no destination display and no
company markings anywhere, bright summer daylight, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no advertising wrap`
**체크:** **버스에 어떤 문자도 없는지(가장 중요)** · 파란 시내버스로 읽히는지

## 7.3 본 컷 S01~S12

### S01 · 설명이 시작된다 (정면 와이드)

**해설:** 정면 축과 전경 어깨를 여기서 확립한다. 카메라 위치가 듣는 친구들의 자리라는 게
이 한 컷으로 읽혀야 한다.

```
[SENPAI] standing in front of a Seoul bus stop shelter in bright summer daylight, centred in the
frame, looking straight into the lens and waving one hand toward the camera with a bright excited
smile as if calling out "listen to this", her posture open and friendly, the shelter and a road
visible behind her softly blurred, [FG], 35mm lens at eye level, straight-on frontal view, [STYLE]
```

**Negative:** `[NEG]` + `no bus in frame, no card visible yet`
**첨부:** A01, A03
**체크:** 완전한 정면인지 · **좌우에 흐린 어깨가 걸렸는지(필수)** · 카드가 아직 없는지 · 시선이 렌즈인지

### S02 · 카드를 들어 보인다 ★제품 최초 노출 (정면 미드)

```
[SENPAI] in front of the bus stop holding a single vertical payment card up beside her face at
chest-to-head height, the card front squarely facing the camera, her face in the upper third and the
card in the middle third of the vertical frame, looking straight into the lens with a bright proud
smile as if saying "look at this", [FG], 50mm lens at eye level, straight-on frontal view,
[CARD], [STYLE]
```

**Negative:** `[NEG]` + `no second card, no bent card, no mirrored logo, no invented card text,
no fingers covering the card front`
**첨부:** A01, A03 + **카드 원본(필수)**
**체크:** 카드면이 선명하고 정면인지 · 로고가 원본과 동일한지 · 얼굴과 카드가 한 프레임인지

### S03 · 검지로 카드를 톡톡 (정면 미드)

```
[SENPAI] holding the vertical card in one hand and tapping it clearly with the index finger of her
other hand, pointing at the card in a single readable gesture, eyebrows slightly raised for emphasis,
looking straight into the lens, [FG], 50mm lens at eye level, straight-on frontal view,
[CARD], [STYLE]
```

**Negative:** `[NEG]` + `no overlapping gestures, no motion blur on hands`
**첨부:** A01, A03 + 카드 원본
**체크:** 손가락이 카드를 명확히 가리키는지 · 두 손이 프레임 안에 있는지

### S04 · 허공에 찍는 동작 ★시그니처 (정면 미드)

**해설:** **이 영상의 시그니처 제스처.** 카드를 허공에 대고 손목을 툭 내려 찍는 시늉.
귀엽고, 한눈에 읽히고, 그 자체가 제품의 소구점이다.

```
[SENPAI] miming a card tap in mid-air, holding the vertical card and flicking her wrist downward as
if touching it to an invisible reader in front of her, a playful pleased expression with her lips
rounded as if making a short "pi" sound, both hands fully inside the frame, looking toward the lens,
slightly wider framing so the whole gesture reads at a glance, [FG], 50mm lens at eye level,
straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no actual card reader device, no terminal, no comic effects, no motion lines`
**첨부:** A01, A03 + 카드 원본
**체크:** **찍는 동작이 한눈에 읽히는지(가장 중요)** · **실제 단말기가 없는지(허공이어야 함)** · 표정이 절제됐는지

### S05 · 버스와 지하철을 가리킨다 (정면 미드)

**해설:** 한 프레임에는 하나의 동작만 — 여기서는 차도를 가리키는 순간을 잡는다.

```
[SENPAI] pointing back over her shoulder toward the road behind her with one hand while still
holding the vertical card in the other, an open enthusiastic expression as if saying "that too",
her gesture clear and unambiguous, looking toward the lens, [FG], 50mm lens at eye level,
straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no bus arriving yet, no overlapping gestures`
**첨부:** A01, A03 + 카드 원본
**체크:** 가리키는 방향이 뒤쪽 차도인지 · 버스가 아직 없는지 · 동작이 하나인지

#### S05b — 아래를 가리키는 순간 (같은 컷 내 두 번째 동작 / 끝 프레임용)

```
[SENPAI] pointing downward toward the ground with one hand while holding the vertical card in the
other, indicating something below, warm confident expression, looking toward the lens, [FG],
50mm lens at eye level, straight-on frontal view, [CARD], [STYLE]
```

### S06 · 엄지 척 + 카드 디테일 (정면 클로즈업)

```
frontal close-up of [SENPAI] giving a small thumbs up with one hand while holding the vertical card
close beside her face with the other, her head tilted very slightly, a soft confident smile, looking
straight into the lens, the card surface detail clearly visible, background fully melted into creamy
bokeh, [FG], 85mm lens at eye level, straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no invented card text, no reflection covering the card face`
**첨부:** A01 + 카드 원본
**체크:** 카드 표면이 선명한지 · 로고가 원본과 동일한지 · 엄지 척이 자연스러운지

### S07 · 버스가 온다 (정면 미드)

**해설:** 소리가 먼저 오고 그녀가 반응한다. 버스는 흐리게 형체만 — 선명해지면 문자가 생성된다.

```
[SENPAI] in front of the bus stop pausing mid-gesture and turning her head to glance back over her
shoulder, a small "oh already?" surprise on her face, still holding the vertical card, and behind
her a blue city bus has pulled in and stopped, rendered completely out of focus as a soft blue mass
with no readable markings, [FG], 50mm lens at eye level, straight-on frontal view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no route number, no destination display, no company logo, no sharp bus,
no panic expression`
**첨부:** A01, A03, A04
**체크:** **버스가 완전히 흐린지(문자 리스크 차단)** · 그녀가 뒤를 돌아보는지 · 당황이 절제됐는지

### S08 · 다급하게 마지막 설명 (정면 미드)

```
[SENPAI] stepping backward toward the bus while still facing the camera, waving one hand urgently
and holding the vertical card up with the other, hurried but still bright and smiling as if saying
"wait, one more thing", her body angled back but her face still toward the lens, the blurred blue
bus behind her with a soft indicator lamp glow, [FG], 50mm lens at eye level, straight-on frontal
view, [CARD], [STYLE]
```

**Negative:** `[NEG]` + `no panic grimace, no comic sweat drops, no route number, no sharp bus`
**첨부:** A01, A03, A04 + 카드 원본
**체크:** 뒷걸음질이 보이는지 · 얼굴이 여전히 카메라를 향하는지 · 다급함이 귀여운 범위인지

### S09 · 버스가 그녀를 가린다 (정면 와이드)

**해설:** 원작의 "기차가 지나가는 화면"의 대응. **S01과 같은 사이즈로 돌아온다.**

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
**체크:** **버스 문자 전무(필수 — 가장 위험한 컷)** · 모션 블러가 충분한지 · 그녀가 가려졌는지 · S01과 사이즈가 같은지

### S10 · 아무도 없다 ★개그 착지 (정면 와이드)

**해설:** **S01·S09와 완전히 같은 정면 와이드.** 전경의 친구 어깨는 여전히 걸려 있다 — 그들은 남았다.

```
straight-on frontal wide view of the same Seoul bus stop, framed identically to the opening shot,
now completely empty with nobody standing in front of the shelter, the road behind clear and quiet,
still bright summer daylight, calm and unchanged, [FG] with the two blurred listeners still framing
the edges, 35mm lens at eye level, [STYLE]
```

**Negative:** `[NEG]` + `no bus in frame, no people in the mid-ground, no main character`
**첨부:** **S01 생성 결과(필수 — 구도 일치용)** + A03
**체크:** **S01과 프레이밍이 일치하는지(가장 중요)** · 주인공이 완전히 없는지 · 버스가 없는지 · 전경 어깨는 남아 있는지

### S11 · 제품 인서트 (배경 플레이트)

**해설:** 카드와 문자는 전부 후반 합성이므로 생성하는 것은 **배경 플레이트뿐**이다.

```
soft defocused background plate of a summer Seoul bus stop and street, everything melted into creamy
pastel bokeh with no recognizable detail, bright milky highlights, gentle warm-to-cool gradient,
the centre and the lower half of the frame kept visually quiet and uncluttered as empty space,
no people, no vehicles in focus, vertical 9:16, [STYLE-PLAIN]
```

**Negative:** `[NEG]` + `no people, no sharp objects, no busy detail in the centre,
no busy detail in the lower half`
**첨부:** A03 · **체크:** 중앙·하단이 비었는지 · 완전히 흐린 보케인지
**후반 합성:** 카드 원본 컷아웃(중앙) + 선행 문구 + 메인 카피 + 각주 + 워터마크

### S12 · 친구들이 폰을 꺼낸다 (CTA)

**해설:** 전경의 흐린 어깨였던 친구들이 처음 얼굴을 드러낸다. **폰 화면은 빈 플레이트.**

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
**첨부:** A02, A03
**체크:** **폰 화면이 완전히 비었는지(필수)** · **좌상단·하단 여백 확보(필수)** · 표정이 부드러운지

---

# Part 8. 영상 프롬프트

Part 7의 키프레임을 **시작 프레임**으로 넣고 아래 모션 프롬프트를 쓴다. 총 30.0초 / 9:16.

## 8.1 공통 원칙

- **카메라는 거의 움직이지 않는다.** 정면 고정 축이 척추다. 무브가 들어가면 축이 흔들린다.
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

## 8.2 컷별 모션 프롬프트

### S01 · 2.5s — 손을 흔든다

```
locked static shot with the camera perfectly still. She looks into the lens and waves one hand toward
the camera twice in a bright friendly motion, smiling and leaning in slightly as if starting to tell
her friends something exciting. The blurred foreground shoulders at the left and right edges stay
soft and almost motionless. Background unchanged.
[NEG-MOTION]
```

### S02 · 2.5s — 카드를 들어올린다

```
locked static shot. She raises the card up beside her face and holds it there — once it is up, the
card must stay flat, vertical and square to the camera with no tilt, no rotation and no reflection
sweeping across its surface. Her proud smile opens slightly and she blinks once. The card design must
remain pixel-stable and unchanged for the rest of the clip.
[NEG-MOTION]
```

⚠️ 카드를 올리는 동작에서 모델이 카드를 기울이는 경우가 많다. **올린 뒤에는 완전히 정지**시킨다.

### S03 · 2.0s — 검지로 톡톡

```
locked static shot. She taps the face of the card twice with her index finger in a small clear
motion, eyebrows lifting slightly on the second tap. The card itself stays flat and stable — only
the pointing finger moves. Single readable gesture, no other movement.
[NEG-MOTION]
```

### S04 · 2.5s — 허공에 찍는 동작 ★시그니처

```
locked static shot. She flicks her wrist downward to mime tapping the card onto an invisible reader
in front of her, holds it there for a beat, then lifts it back up with a pleased playful smile, her
lips rounding briefly as if making a short sound. One single clean tap motion only, not repeated.
No physical reader or terminal ever appears in the frame. The card stays flat and undistorted.
[NEG-MOTION]
```

⚠️ **이 클립이 이 영상의 시그니처다.** 동작이 흐릿하거나 두 번 반복되면 다시 뽑는다.

### S05 · 2.5s — 차도 → 아래를 가리킨다

**설정:** 시작 프레임 S05, **끝 프레임 S05b**를 함께 넣으면 두 동작이 안정적으로 이어진다.

```
locked static shot. She points back over her shoulder toward the road behind her, holds for a beat,
then brings that hand down and points clearly toward the ground. Two distinct gestures with a short
pause between them, never overlapping. The card stays held steady in her other hand throughout.
Her expression stays open and enthusiastic.
[NEG-MOTION]
```

### S06 · 2.0s — 엄지 척

```
locked static close-up. She raises her thumb into a small thumbs up and tilts her head very slightly,
her smile softening into quiet confidence, and blinks once. The card stays completely still beside her
face with its surface sharp and its design unchanged. Minimal movement overall.
[NEG-MOTION]
```

### S07 · 2.0s — 버스가 온다

```
locked static shot. Behind her a blurred blue mass slides in and settles as the bus pulls up and
stops, staying completely out of focus with no markings ever becoming visible. She stops mid-gesture,
turns her head to glance back over her shoulder, then turns back toward the lens with a small
"oh already?" expression. Her surprise stays small and natural.
[NEG-MOTION]
```

⚠️ 버스가 선명해지면 노선번호가 생성된다. **끝까지 흐릿하게** 유지되는지 확인한다.

### S08 · 2.0s — 뒷걸음질

```
locked static shot. She takes two small steps backward toward the bus while keeping her face toward
the camera, waving one hand urgently and still holding the card up with the other, hurried but
smiling. A soft indicator glow pulses on the blurred bus behind her. Her expression stays bright and
cute, never panicked or grimacing.
[NEG-MOTION]
```

### S09 · 2.0s — 버스가 가린다

```
locked static wide shot. The blue city bus sweeps across the frame in front of the shelter, covering
her completely, with strong horizontal motion blur across its body and windows and sky reflections
streaking along the glass. The bus panels stay completely blank throughout — no numbers or markings
ever appear. Steady continuous movement, no sudden acceleration, camera never follows.
[NEG-MOTION]
```

⚠️ 이 클립은 **프레임별로** 버스 문자 생성 여부를 확인한다. 가장 위험한 컷이다.

### S10 · 2.5s — 정적 ★개그 착지

```
locked static wide shot, framed identically to the opening shot, now empty. Nothing moves in the
mid-ground — no people, no bus, nothing enters the frame. Only the faintest breeze in the street
trees and the softest drift in the blurred foreground shoulders. Hold the emptiness and the quiet
for the full duration.
[NEG-MOTION]
```

⚠️ **정적을 충분히 준다.** 여기서 서두르면 웃음이 착지하지 않는다.

### S11 · 4.5s — 제품 인서트 플레이트

```
almost still defocused background plate with only a very slow gentle drift of the creamy bokeh,
like a soft breathing background. Nothing comes into focus, no recognizable shapes form, no people
or vehicles appear. The centre and the lower half stay visually quiet and empty for the whole
duration.
[NEG-MOTION]
```

**전환:** S10에서 **페이드아웃 → 페이드인.** 유일한 페이드로 개그와 광고를 분리한다.

### S12 · 3.0s — 폰을 꺼낸다 (CTA)

```
extremely slow gentle push-in. The two glance at each other, nod once, and lean in together over the
single phone held between them, both smiling softly with eyes gently cast down. The phone screen stays
a completely uniform blank light grey surface for the entire clip — no content ever appears on it.
The upper-left area of the frame and the bottom fifth stay clean and empty throughout — nothing moves
into them. Settle into stillness at the end.
[NEG-MOTION]
```

## 8.3 타임라인

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

---

# Part 9. 카피·자막·고지문

**원칙:** 모든 문자는 **후반 합성**이다. 생성 이미지·영상에는 어떤 글자도 넣지 않는다.
**그녀의 대사를 자막으로 옮기지 않는다** — 제스처가 설명하게 하고, 자막은 SFX와 카피만 담당한다.

## 9.1 메인 카피 — 개그를 광고로 잇는 2단 구조

S11 제품 인서트에서 **작은 선행 문구 + 메인 카피** 2단으로 간다.

| 단 | 일본어 | 한국어 (작게) |
|---|---|---|
| 선행 (작게) | 先輩が言いたかったのは、これ。 | 선배가 하려던 말은, 이거예요 |
| **메인 (크게)** | **バスも、地下鉄も、これ一枚。** | **버스도 지하철도, 이 한 장으로** |

**이 구조를 권하는 이유:** 선행 문구가 S10의 허탈함을 그대로 받아서 웃음을 한 번 더 굴리고,
메인 카피로 자연스럽게 넘어간다. 광고 문구가 아니라 **이야기의 마무리**로 읽힌다.

### 대안

| 대안 | 일본어 | 한국어 |
|---|---|---|
| A (직접형) | トスのカード、交通カードにもなる。 | 토스 카드, 교통카드로도 돼요 |
| B (한 장 강조) | 韓国の移動、これ一枚。 | 한국에서의 이동, 이 한 장으로 |
| C (짧게) | バスも地下鉄も、トスで。 | 버스도 지하철도, 토스로 |

## 9.2 컷별 자막

| 컷 | 일본어 | 한국어 (작게) | 비고 |
|---|---|---|---|
| S01 | — | — | 손 흔들기. 자막 없이 상황만 |
| S02 | — | — | 카드가 말한다 |
| S03 | — | — | 제스처가 말한다 |
| S04 | **ピッ！** (SFX) | — | ★시그니처. 손글씨풍. 찍는 손 옆에 작게 |
| S05 | — | — | 가리키는 동작이 말한다 |
| S06 | — | — | 엄지 척 |
| S07 | — | — | 버스 도착. 표정으로만 |
| S08 | **ピピピピ…** (SFX) | — | 손글씨풍. 버스 쪽에 작게 |
| S09 | — | — | 버스가 가린다 |
| S10 | **…** | — | 정적을 자막으로도 |
| S11 | 先輩が言いたかったのは、これ。<br>**バスも、地下鉄も、これ一枚。** | 선배가 하려던 말은, 이거예요<br>**버스도 지하철도, 이 한 장으로** | 메인 카피 + 각주 |
| S12 | パスポートだけで登録。 | 토스 앱에서 여권만으로 가입 | CTA + 로고 + 워터마크 |

**자막이 거의 없다는 것이 이 편의 설계다.** S01~S09에서 정보를 전달하는 것은 자막이 아니라
**그녀의 손**이다. 자막을 채우면 제스처를 볼 이유가 없어진다.

## 9.3 각주 (정확성 고지)

| 번호 | 일본어 | 위치 |
|---|---|---|
| ① | T-moneyが使える地下鉄・バスでご利用いただけます。 | S11 하단 |
| ② | Visitorカードはプリペイドカードです。 | S11 하단 |
| ③ | ご利用条件は最新のトスアプリの案内をご確認ください。 | S11 또는 S12 하단 |

**①은 이 편에서 특히 중요하다** — 버스가 메인 소재라 "모든 버스에서 조건 없이 된다"로
읽힐 여지를 차단해야 한다.

## 9.4 CTA (S12)

| 일본어 | 한국어 (작게) |
|---|---|
| パスポートだけで登録。 | 토스 앱에서 여권만으로 가입 |

**선택 옵션:** 「初回のVisitorカードは無料です。」 / 「첫 Visitor 카드는 무료」
— 각주 크기로 **작게**만 권장. 크게 넣으면 단일 메시지(교통)가 흐려진다.
넣을 경우 "**첫**" 카드임을 반드시 명시한다.

## 9.5 로고

- **공식 `toss for travelers` 락업 파일만 사용.** AI 생성·변형·색변경·타그래픽 결합 금지
- 위치: **S12 좌상단.** S11 인서트에도 하단 배치 가능
- 크기: 화면 폭의 약 30~35%
- 가독성이 부족하면 로고 뒤에 아주 옅은 화이트 그라데이션만 (로고 자체는 손대지 않는다)

## 9.6 디스클레이머 워터마크 배치

**전 구간 하단에 작게 상시 노출 + S11·S12에서 확실히 보이게.**

- 특정 구간에만 넣으면 스크롤로 놓칠 수 있으므로 **상시 노출이 가장 안전**하다
- 하단 안전영역, 불투명도 70~80%. SFX 자막과 겹치지 않게
- 정렬은 **중앙 정렬 버전** 권장 (세로 영상에서 가장 안정적)
- 인스타그램 UI(하단 계정명·캡션 영역)에 가려지지 않도록 **하단에서 충분히 띄운다**

## 9.7 타이포그래피 규격

| 항목 | 규격 |
|---|---|
| 일본어 폰트 | Noto Sans JP (대안: Yu Gothic) — Bold/Medium |
| 한국어 폰트 | Noto Sans KR — Medium/Regular |
| **SFX 자막** | **손글씨풍 일본어 폰트** |
| 메인 카피 | 화면 폭의 70~80%, 굵게 |
| 선행 문구 | 메인의 40~45% |
| 한국어 소자막 | 일본어 자막의 55~65%, 바로 아래 줄 |
| 각주 | 한국어 소자막의 70%, 불투명도 75% |
| 안전영역 | 하단 1/5, 상단 1/8 비움. 좌상단은 로고용 |
| 색상 | 화이트 기본. 필요시 **아주 옅은 드롭섀도**만 (외곽선 금지) |
| 강조색 | 토스 블루. **카카오·네이버 연상 노랑·초록 메인 금지** |

## 9.8 게시물 캡션 초안

```
第一話「バス停」篇

先輩が言いたかったのは、これでした。
バスも、地下鉄も、これ一枚。

パスポートだけで登録できる Toss for Travelers の Visitor カード。
T-moneyが使える地下鉄・バスでご利用いただけます。

※ Visitorカードはプリペイドカードです。
※ ご利用条件は最新のトスアプリの案内をご確認ください。

버스도 지하철도, 이 한 장으로.
토스 앱에서 여권만으로 가입할 수 있어요.

토스 Foreigner Bridge Crew 대외활동으로 콘텐츠 제작을 지원받아 작성된 게시물이며,
최종 수상 시 상금 등 혜택을 받을 수 있습니다.
```

**「第一話」 표기:** 원작이 시리즈물이므로 형식을 계승했다. 후속편 계획이 없으면 빼도 된다.

---

# Part 10. 검수 체크리스트

## 10.1 이미지 생성 후

- [ ] **전 컷이 정면 축인지** (앵글이 바뀐 컷이 없는지)
- [ ] **S01~S10 좌우에 흐린 어깨가 걸려 있는지**
- [ ] **S01·S09·S10의 프레이밍이 일치하는지**
- [ ] 어떤 컷에도 **생성된 문자·로고**가 없다
- [ ] **버스에 노선번호·행선지·회사명이 없다** (S07·S08·S09 특히)
- [ ] **정류장 안내판이 비어 있다**
- [ ] S04에 **실제 단말기가 없다** (허공에 찍는 동작이어야 함)
- [ ] S12의 폰 화면이 **완전히 비어 있다**
- [ ] 카드 등장 컷(S02·S03·S04·S05·S06·S08)의 카드가 원본과 일치한다 (다르면 원본 합성)
- [ ] S11·S12에 좌상단·하단 여백이 있다
- [ ] 말풍선·집중선·만화 효과가 없다
- [ ] 손가락 개수·형태가 정상이다
- [ ] 의상·헤어·가방이 전 컷 일관된다

## 10.2 영상 생성 후

- [ ] **모든 클립의 카메라가 고정이고 앵글이 바뀌지 않았다**
- [ ] **버스에 문자가 끝까지 나타나지 않는다** (S07·S08·S09 **프레임별** 확인)
- [ ] S04에 실제 단말기가 나타나지 않는다
- [ ] 카드 디자인이 클립 내내 변하지 않는다
- [ ] S12의 폰 화면에 아무것도 나타나지 않는다
- [ ] 어떤 클립에도 문자·로고·말풍선이 생성되지 않았다
- [ ] S01·S09·S10의 구도가 일치하고 S10이 비어 있다
- [ ] 좌우 전경 어깨가 S01~S10 내내 유지된다
- [ ] 제스처가 클립당 하나씩 명확하게 읽힌다
- [ ] 손가락이 뭉개지거나 늘어나지 않았다
- [ ] S11·S12의 좌상단·하단 여백이 끝까지 비어 있다
- [ ] **알아들을 수 있는 목소리가 생성되지 않았다** (네이티브 오디오 끔 확인)

## 10.3 카피·자막 검수

- [ ] 핵심 메시지가 **하나**("교통카드로도 된다")로 읽힌다
- [ ] **그녀의 대사가 자막으로 옮겨지지 않았다**
- [ ] 카드를 **선불카드**로 표현했다 (신용/체크카드 아님)
- [ ] 티머니를 "**지원하는** 지하철·버스" 범위로만 썼다
- [ ] "첫" 카드 무료임을 명시했다 (무료 언급 시)
- [ ] 검증되지 않은 시간·수치가 없다
- [ ] 과장 표현("무조건·100%·최고의·다 됩니다")이 없다
- [ ] 타 금융사·은행 언급·비교가 없다
- [ ] 토스뱅크 등 계열사 서비스 언급이 없다
- [ ] 브랜드명을 '토스'/toss로만 표기했다

## 10.4 최종 납품 전

- [ ] 9:16 (1080×1920), 30초 전후, H.264 + AAC
- [ ] 휴대폰 세로 재생에서 자막·워터마크 가독성 확인
- [ ] **디스클레이머가 영상 안에서 눈에 보인다**
- [ ] 공식 로고 파일 사용 확인 (AI 생성물 아님)
- [ ] 앱 화면이 실제 화면인지 확인 (AI 생성물 아님)
- [ ] 일본어 카피 **원어민 감수**
- [ ] **포리크루봇 국문 검토 통과** (가이드 Mission 3)
- [ ] 보고서 제출 (목요일 오후 1시)

---

# Part 11. 작업 순서와 다음 단계

## 11.1 생성 순서 (권장)

1. **A03 → 확정** — 정면 축이 여기서 결정된다. 전 컷의 배경 기준
2. **A01 → 확정** — 주인공 얼굴·의상이 흔들리면 대부분을 다시 만들어야 한다. 여기서 시간을 쓴다
3. **A04 → 확정** — 버스에 문자가 하나라도 생기면 전부 다시
4. **A02 → 확정**
5. **S01 생성 → 확정** — S09·S10의 구도 기준이므로 먼저
6. **S10 생성** — S01을 레퍼런스로 붙여 구도 일치 (인물만 빼면 된다)
7. 나머지 S02~S09, S05b, S11, S12
8. **실패한 컷만 개별 재생성.** 전체를 다시 만들지 않는다

## 11.2 이후 단계 (이번 범위 밖)

| 단계 | 내용 |
|---|---|
| 생성 | 위 순서로 키프레임 → 클립 생성 |
| 오디오 | 음악 + SFX(버스 접근음·에어브레이크·경고음·「ピッ」) 후반 작업 |
| 합성 | 카드 원본 컷아웃, 실제 앱 화면(S12), 공식 로고 |
| 자막 | 일본어·한국어 자막 + SFX 손글씨 자막 + 각주 + 워터마크 번인 |
| 어셈블리 | ffmpeg 스티칭, 페이드(S10→S11), 최종 렌더 |
| 검증 | Part 10 체크리스트 전항목 |

## 11.3 알려진 위험

| 위험 | 대응 |
|---|---|
| S09에서 버스 노선번호가 생성된다 | 프레임별 확인. 반복 실패 시 버스를 더 흐리게 하거나 속도를 올린다 |
| 카드 로고가 원본과 달라진다 | **원본 PNG를 원근 맞춰 합성**으로 교체 (프롬프트에 폴백 명시됨) |
| 주인공 얼굴이 컷마다 흔들린다 | A01을 모든 컷에 레퍼런스로 첨부. 흔들리는 컷만 재생성 |
| S04 제스처가 안 읽힌다 | 사이즈를 더 넓게 잡아 두 손이 완전히 들어오게. 동작을 한 번만 |
| 영상 모델이 목소리를 생성한다 | 네이티브 오디오를 끄고 생성 |
| 일본어 카피가 어색하다 | 원어민 감수 필수 (제작자 판단만으로 확정하지 않는다) |
