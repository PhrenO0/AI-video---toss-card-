# 4. 노션 연동 — 콘텐츠 목록 자동 채우기

목표: **콘텐츠 목록 DB에 주제 한 줄만 적으면**, 자동화가 레퍼런스를 찾아 붙이고 카드뉴스 카피까지 써 넣기.

```
[사람]  DB에 행 추가 → 주제만 입력, 상태는 비워둠
          ↓
[자동]  레퍼런스 수집 → 카피 생성 → 속성 기입 + 본문 작성 → 상태 '완료'
```

## 먼저 알아야 할 것

### API가 2025-09-03에 바뀌었습니다

Notion 데이터베이스 안에 여러 개의 **data source**가 들어갈 수 있게 되면서 조회 경로가 바뀌었습니다.

```
(구) POST /v1/databases/{database_id}/query      ← deprecated
(신) POST /v1/data_sources/{data_source_id}/query
```

`database_id`와 `data_source_id`는 **다른 객체**입니다. 사용자가 URL에서 복사하는 건 `database_id`이므로, 이 툴킷이 자동으로 data source를 찾아 변환합니다. 신경 쓰지 않으셔도 됩니다.

### 칼럼 구성을 몰라도 동작합니다

상대 DB의 칼럼 이름과 타입은 팀마다 다릅니다. 그래서 이렇게 처리합니다.

1. 실행할 때마다 **실제 스키마를 읽습니다**
2. 논리 필드(`주제`, `상태`, `카피`…)를 실제 칼럼명으로 **자동 매칭**합니다 (한국어·영어 별칭 지원)
3. **타입에 맞춰 값을 만듭니다** — 같은 '상태'라도 `select`면 select로, `status` 타입이면 status로
4. **없는 칼럼은 건너뜁니다** — 칼럼 하나 없다고 전체가 실패하지 않습니다

자동 매칭이 틀리면 설정으로 직접 지정할 수 있습니다(아래 참조).

---

## 설정

### 1) 통합(Integration) 만들기

1. https://www.notion.so/my-integrations → **New integration**
2. 이름 `TOSS 콘텐츠 자동화`, 연결할 워크스페이스 선택
3. Capabilities: **Read content**, **Update content**, **Insert content** 체크
4. **Internal Integration Secret** 복사 (`ntn_` 으로 시작)

```bash
# automation/.env
NOTION_TOKEN=ntn_...
```

### 2) DB에 통합 연결 (이걸 빼먹으면 404가 납니다)

토큰만 만들면 아무것도 못 읽습니다. **대상 DB에 통합을 명시적으로 연결**해야 합니다.

Notion에서 콘텐츠 목록 DB를 열고 → 우측 상단 **⋯** → **연결(Connections)** → `TOSS 콘텐츠 자동화` 추가

### 3) DB ID 찾기

```bash
toss-content notion find
```

통합에 공유된 DB 목록과 `database_id`가 출력됩니다. 이걸 설정에 넣으세요.

```yaml
# automation/config/sources.yaml
notion:
  database_id: "39ab9019-0357-8006-9199-f931d52b86b4"
```

> ⚠️ **페이지 URL이 아니라 데이터베이스 URL이어야 합니다.**
> 주신 링크(`app.notion.com/p/26-TOSS-Foreigner-Bridge-...`)는 **페이지**입니다.
> 그 안의 콘텐츠 목록 DB를 전체 페이지로 연 뒤 주소창 URL을 쓰거나,
> `notion find` 로 찾는 편이 확실합니다. URL 전체를 그대로 넣어도 ID를 알아서 뽑습니다.

### 4) 칼럼 매핑 확인

```bash
toss-content notion schema
```

실제 칼럼과 자동 매칭 결과가 나옵니다.

```
실제 칼럼:
  · 주제                       title
  · 상태                       status
  · 카피 초안                   rich_text

논리 필드 매핑 (자동 감지 결과):
  ✅ topic          → 주제
  ✅ status         → 상태
  ⬜ copy           → (없음 — 이 필드는 건너뜁니다)
```

`copy`가 `카피 초안`을 못 찾았다면 직접 지정합니다.

```yaml
notion:
  properties:
    copy: 카피 초안
```

---

## 권장 DB 구성

없어도 동작하지만, 있으면 자동으로 채워지는 칼럼입니다.

| 칼럼 | 타입 | 채워지는 내용 |
|---|---|---|
| 주제 | title | **사람이 입력** — 자동화는 덮어쓰지 않습니다 |
| 상태 | status 또는 select | `완료` / `실패` 로 갱신 |
| 요약 | rich_text | 커버 카드 문구 |
| 카피 | rich_text | 카드뉴스 전체 카피 |
| 레퍼런스 | rich_text | 참고한 게시물 링크 목록 |
| 플랫폼 | multi_select | 레퍼런스 출처 (x / instagram / threads) |
| 슬러그 | rich_text | 카드뉴스 식별자 (Figma 플러그인에 넣을 spec 이름) |
| 카드수 | number | 생성된 카드 장수 |
| 갱신일 | date | 처리 시각 |
| 피그마 | url | Figma 파일 링크 |

**상태 칼럼은 만드는 걸 권합니다.** 어떤 행을 처리할지 판단하고 중복 실행을 막는 기준이라서요. 없으면 본문의 자동 생성 표식으로 대신 판단합니다(추가 API 호출이 들어갑니다).

---

## 사용법

### 사람이 하는 일

DB에 행을 추가하고 **주제만** 적습니다. 상태는 비워두거나 `요청`으로 둡니다.

| 주제 | 상태 |
|---|---|
| 일본 관광객이 겪는 교통카드 문제 | *(비어 있음)* |
| 청소년 선불카드 발급 후기 | 요청 |

### 자동화가 하는 일

```bash
toss-content notion pending          # 처리 대기 행 확인
toss-content notion fill --dry-run   # 쓰지 않고 결과만 미리보기
toss-content notion fill --limit 5   # 실제 채우기
```

각 행에 대해:
1. DB에서 관련 레퍼런스를 뽑고
2. 카드뉴스 카피를 생성한 뒤 (Claude 또는 규칙 기반)
3. 속성에 요약·카피·레퍼런스·플랫폼 등을 기입하고
4. 페이지 **본문**에 카드별 카피와 참고 링크를 적고
5. 상태를 `완료`로 바꿉니다

`toss-content daily` 에도 포함돼 있어 GitHub Actions가 매일 자동 처리합니다.

### 처리 대상 판단 규칙

| 상태 값 | 처리 |
|---|---|
| 비어 있음 | ✅ 처리 |
| `요청`, `대기`, `todo`, `not started` | ✅ 처리 |
| `완료`, `done` | ⏭ 건너뜀 |
| 그 외 (`진행중`, `보류` 등) | ⏭ 건너뜀 — 모르는 상태는 건드리지 않습니다 |

`config/sources.yaml` 의 `trigger_status` / `done_status` 로 바꿀 수 있습니다.

---

## 안전장치

- **사람이 쓴 제목을 덮어쓰지 않습니다.** 자동화가 title 속성을 건드리면 입력이 사라지므로, 아예 쓰기 대상에서 제외했습니다.
- **실패도 DB에 남깁니다.** 처리 실패 시 상태를 `실패`로 바꾸고 본문에 오류 내용을 적습니다. 조용히 사라지면 사람이 눈치채지 못합니다.
- **중복 실행 방지.** 상태 칼럼이나 본문 표식으로 이미 처리된 행을 건너뜁니다.
- **Notion 장애가 전체를 막지 않습니다.** `daily` 실행에서 Notion이 실패해도 수집과 슬랙 다이제스트는 그대로 진행됩니다.

---

## 문제 해결

| 증상 | 원인과 해결 |
|---|---|
| `NOTION_TOKEN이 없습니다` | `.env` 에 토큰 미설정 |
| `데이터베이스를 찾을 수 없습니다` | **DB에 통합 연결 누락** (2번 단계). 가장 흔한 원인입니다 |
| `notion find` 결과가 비어 있음 | 같은 원인 — 어떤 DB에도 통합이 연결되지 않음 |
| 특정 칼럼만 안 채워짐 | `notion schema` 로 매칭 확인 → `notion.properties` 에 직접 지정 |
| `validation_error` (select) | 상태 값이 DB의 옵션 목록에 없음. `done_status` 를 실제 옵션명과 맞추세요 |
| 페이지 ID를 DB ID로 착각 | `notion find` 로 진짜 database_id 확인 |
| 같은 행이 반복 처리됨 | 상태 칼럼이 없어 표식 판단 중. 상태 칼럼 추가를 권장 |
