# 2. X · Instagram · Threads 레퍼런스 자동 수집

목표: 콘텐츠 기획에 쓸 소셜 레퍼런스를 매일 자동으로 모으고, 볼 가치 있는 것만 위로 올리기.

## 먼저 알아야 할 것: 2026년 소셜 API 현실

세 플랫폼 모두 무료 수집이 사실상 막혔거나 조건이 붙습니다. **이게 이 기능의 가장 큰 제약**이라 먼저 짚습니다.

### X (구 트위터)

무료 검색 티어가 **없습니다**. 2023년 2월에 무료 API가 끝났고, 남아 있던 무료 등급도 쓰기 전용 스텁으로 축소된 뒤 2026년 2월 종량제로 흡수됐습니다. 현재 신규 개발자가 쓸 수 있는 건 종량제 아니면 Enterprise뿐입니다.

- **종량제**: 게시물 읽기 $0.005/건, 사용자 읽기 $0.010/건 (월 200만 건 상한)
- 기존 구독자만 남아 있는 레거시 등급: Basic $200/월, Pro $5,000/월
- 전문 검색(full-archive)은 Enterprise($42,000/월~) 전용

→ **권장**: 종량제 토큰을 쓰거나, 예산이 없으면 아래 폴백을 쓰세요.

### Instagram

Basic Display API 폐지 후 남은 건 **Instagram Graph API**뿐이고, **비즈니스/크리에이터 계정 + 연결된 Facebook 페이지**가 전제입니다. 개인 계정 데이터는 접근 불가입니다.

- 해시태그 검색: **계정당 주 30개 고유 해시태그** 제한 (엄격합니다)
- Business Discovery: 상대 비즈니스 계정의 공개 정보를 동의 없이 조회 가능
- 2026년에 단일 게시물 조회에서 조회수 필드가 빠졌습니다

### Threads

Meta가 2025년에 키워드 검색을 열었습니다. 다만 두 가지가 큽니다.

- `threads_keyword_search` 권한이 **앱 리뷰를 통과하기 전에는 본인 계정 게시물만** 검색됩니다
- 레이트리밋이 **7일 롤링 500쿼리**로 빡빡합니다
- **공개 검색 결과에는 지표(좋아요/댓글)가 붙지 않습니다.** 인사이트는 자기 소유 게시물에만 열립니다

---

## 이 툴킷의 대응: 프로바이더 폴백 체인

플랫폼마다 프로바이더를 여러 개 두고 **앞에서부터 시도 → 실패하면 다음으로** 넘어갑니다. 토큰이 없으면 조용히 건너뛰므로, 일부만 설정해도 나머지는 정상 동작합니다.

| 플랫폼 | 1순위 | 2순위 | 3순위 |
|---|---|---|---|
| X | `official` (X API v2) | `apify` (액터) | `rss` (RSSHub/Nitter, 계정만) |
| Instagram | `official` (Graph API) | `apify` | — |
| Threads | `official` (keyword_search) | `apify` | — |

순서는 `config/sources.yaml` 의 `collect.providers` 에서 바꿀 수 있습니다.

```yaml
collect:
  providers:
    x: [official, apify, rss]
```

**아무 토큰도 없어도** `toss-content collect` 는 0건을 반환하고 정상 종료합니다. 파이프라인이 죽지 않습니다.

---

## 설정

### 수집 규칙 (`automation/config/sources.yaml`)

```yaml
sources:
  - kind: account          # account | keyword | hashtag
    value: tossteam
    label: 토스 공식         # 슬랙 표시용 이름
    platforms: [x, instagram, threads]   # 비우면 전체 적용
```

> ⚠️ Instagram 해시태그는 **계정당 주 30개** 제한이 있습니다. `platforms: [instagram]` 인 hashtag 규칙 수 × 실행 횟수가 이 안에 들어오는지 확인하세요.
> ⚠️ Threads는 **7일 500쿼리** 제한이 있습니다. 규칙 5개 × 하루 1회 = 주 35쿼리로 안전합니다.

### 토큰 (`automation/.env`)

`.env.example` 을 복사해 채우세요. 전부 채울 필요 없습니다.

```bash
X_BEARER_TOKEN=              # X API v2 (종량제)
X_RSS_BASE=                  # 예: https://rsshub.app (무료 폴백, 계정 타임라인만)
IG_ACCESS_TOKEN=             # Instagram Graph API
IG_BUSINESS_USER_ID=         # 비즈니스 계정 ID
THREADS_ACCESS_TOKEN=        # Threads API
APIFY_TOKEN=                 # 폴백 수집 (셋 다 커버)
```

---

## 랭킹: 왜 "좋아요 많은 글"이 위가 아닌가

목적이 *인기 글 나열*이 아니라 **지금 참고할 가치가 큰 글 찾기**라서, 다음을 조합합니다.

| 요소 | 의미 | 기본 가중치 |
|---|---|---|
| 참여량 | `log(좋아요+댓글+공유)` — 10만이 1만보다 10배 좋은 레퍼런스는 아니므로 로그 스케일 | 1.0 |
| **속도** | 시간당 참여수 — 갓 올라온 급상승 글을 잡는다 | **1.4** |
| 키워드 | `boost_keywords` 매칭 수 | 0.6 |
| 미디어 | 이미지/영상 있으면 가산 (카드뉴스 레퍼런스라서) | 0.3 |
| 신선도 | 36시간 반감기 감쇠 | 곱셈 |

**플랫폼 간 지표 불균형 보정**: Threads 공개 검색은 지표가 아예 없어 0으로 들어옵니다. 그대로 두면 항상 바닥에 깔리므로 중립 프록시 값(30)을 넣습니다. "지표 없음"이 "가치 없음"이 되지 않게 하기 위한 것이지, 실제 인기도를 추정하는 값이 아닙니다.

**다변화**: 상위 목록이 한 플랫폼/한 계정으로 도배되지 않도록 같은 작성자는 최대 2건, 플랫폼별 상한도 겁니다.

가중치는 `config/sources.yaml` 의 `ranking` 에서 조정하세요.

---

## 사용법

```bash
toss-content collect                      # 전체 수집
toss-content collect --platform x,threads # 일부만
toss-content digest --limit 10            # 슬랙 전송
toss-content daily                        # collect + digest (CI용)
```

수집 결과는 `automation/data/references.db` (SQLite)에 쌓입니다. 같은 게시물은 중복 저장되지 않고 지표만 갱신되며, 슬랙에 이미 보낸 건 `notified_at` 으로 표시돼 다시 보내지 않습니다.

## 문제 해결

| 증상 | 원인과 해결 |
|---|---|
| 전 플랫폼 0건 | 토큰 미설정. `toss-content doctor` 로 확인 |
| X만 0건 | 무료 티어로는 검색 불가. 종량제 토큰이나 `X_RSS_BASE` 설정 |
| Instagram 해시태그 실패 | 주 30개 한도 소진, 또는 비즈니스 계정 미연결 |
| Threads가 본인 글만 나옴 | `threads_keyword_search` 권한 앱 리뷰 미통과 |
| Threads 지표가 전부 0 | 정상입니다. 공개 검색은 지표를 제공하지 않습니다 |
| 429 오류 반복 | `collect.per_query_limit` 을 낮추거나 실행 주기를 늘리세요 |
