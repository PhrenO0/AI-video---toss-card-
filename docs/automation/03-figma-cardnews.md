# 3. 카드뉴스 제작 자동화 (Figma 연동)

대상 파일: https://www.figma.com/design/ztuGJQdoVtA7u9pxvq8m4m/Untitled
(file key: `ztuGJQdoVtA7u9pxvq8m4m`)

## 먼저 알아야 할 것: Figma REST API는 쓰기를 못 합니다

이게 설계를 가르는 지점입니다.

- **REST API**: 파일 읽기, 이미지 export, 코멘트 — **노드 생성/수정 불가**
- **플러그인 API**: 노드 생성/수정 가능 — 단 **사람이 Figma를 열고 실행**해야 함

즉 "서버가 알아서 Figma에 카드뉴스를 그려 넣는" 것은 Figma가 구조적으로 허용하지 않습니다. 그래서 역할을 나눴습니다.

```
 ┌─ 자동 (서버/CI) ─────────────────┐   ┌─ 반자동 (Figma 안) ──┐   ┌─ 자동 ────────┐
   레퍼런스 → 카피 생성 → spec.json   →   플러그인이 카드 생성   →   PNG export
   슬랙 프리뷰로 승인                     (버튼 한 번)              슬랙 공유
 └──────────────────────────────────┘   └──────────────────────┘   └──────────────┘
```

사람이 하는 일은 **Figma에서 플러그인 버튼 한 번 누르는 것**뿐입니다.

---

## 준비

### 1) Figma 토큰

Figma → **Settings → Security → Personal access tokens** → *Generate new token*
스코프는 `File content: Read` 이상. 코멘트를 남기려면 `Comments: Write` 도 추가.

```bash
# automation/.env
FIGMA_TOKEN=figd_...
FIGMA_FILE_KEY=ztuGJQdoVtA7u9pxvq8m4m
```

확인:

```bash
toss-content figma inspect     # 인증 + 파일의 프레임 목록
```

### 2) 템플릿 프레임 만들기 (권장)

플러그인은 두 모드로 동작합니다.

| 모드 | 조건 | 결과 |
|---|---|---|
| **템플릿 모드** | 파일에 `template/cover`, `template/body`, `template/outro` 프레임 존재 | 디자이너가 만든 스타일 그대로 복제 |
| 기본 모드 | 템플릿 없음 | 코드가 최소 레이아웃으로 생성 |

**템플릿 모드를 쓰세요.** 브랜드 톤이 유지됩니다.

만드는 법:

1. 1080 × 1350 (인스타 4:5) 프레임 3개를 만들고 이름을 정확히 `template/cover`, `template/body`, `template/outro` 로 지정
2. 각 프레임 안의 텍스트 레이어 **이름**을 아래처럼 지정 (내용은 아무거나)

| 레이어 이름 | 채워지는 값 |
|---|---|
| `#title` | 카드 제목 |
| `#body` | 카드 본문 |
| `#badge` | 라벨 (예: `COVER`, `참여 1240`) |
| `#image` | 레퍼런스 이미지 (도형/사각형에 지정) |

값이 비면 해당 레이어는 자동으로 숨겨집니다.

### 3) 플러그인 설치

Figma 데스크톱 앱에서:

**Plugins → Development → Import plugin from manifest…**
→ `automation/figma-plugin/manifest.json` 선택

빌드 과정이 없습니다 (순수 JS). 저장소를 clone 한 사람은 바로 쓸 수 있습니다.

> `manifest.json` 의 `networkAccess.allowedDomains` 가 `["*"]` 로 열려 있습니다.
> 사내 배포 시에는 실제 쓰는 도메인만 남겨 좁히세요.

---

## 사용법

### 1단계 — 초안 생성

```bash
toss-content cardnews "일본 관광객이 겪는 교통카드 문제" --cards 6 --post
```

일어나는 일:

1. DB에서 상위 레퍼런스를 플랫폼 다변화해서 뽑음
2. 카피 생성
   - `ANTHROPIC_API_KEY` 있으면 **Claude**가 토스 톤으로 작성 (권장)
   - 없으면 규칙 기반 초안으로 폴백 (사람이 손볼 뼈대)
3. `automation/out/cardnews/<slug>.json` 에 spec 저장
4. `automation/out/preview/<slug>/*.png` 에 프리뷰 렌더
5. `--post` 를 주면 슬랙에 미리보기 + 승인 버튼 게시

슬랙에서 승인하거나 `🔄 다시 생성` 을 누를 수 있습니다.

### 2단계 — Figma에 반영

1. Figma에서 **Plugins → Development → TOSS 카드뉴스 생성기** 실행
2. `out/cardnews/<slug>.json` 내용을 붙여넣기 (또는 URL로 불러오기)
3. **템플릿 확인** 버튼으로 템플릿 인식 여부 확인
4. **카드 생성** → `카드뉴스 자동생성` 페이지에 카드 세트 생성

생성된 노드 ID가 플러그인 창에 표시됩니다.

### 3단계 — 내보내기

```bash
toss-content figma export --nodes "12:34,12:35,12:36" --slug 교통카드-캠페인
```

`automation/out/figma/<slug>/*.png` 에 2배 해상도로 저장됩니다.

리뷰 코멘트도 남길 수 있습니다:

```bash
toss-content figma comment "3번 카드 문구 확인 부탁드립니다" --node 12:36
```

---

## 카드뉴스 spec 형식

플러그인과 파이프라인이 주고받는 계약입니다. 직접 손으로 써서 플러그인에 넣어도 됩니다.

```json
{
  "version": 1,
  "slug": "교통카드-캠페인-260809-1430",
  "topic": "일본 관광객이 겪는 교통카드 문제",
  "template": "toss_default",
  "createdAt": "2026-08-09T14:30:00+00:00",
  "cards": [
    {
      "index": 1,
      "kind": "cover",
      "title": "개찰구에서 막힌 적 있나요?",
      "body": "한국 지하철, 카드 하나로 끝냅니다.",
      "badge": "COVER",
      "image_url": "",
      "source_uids": ["x:1234567890"]
    }
  ]
}
```

- `kind`: `cover` | `body` | `outro` — 어떤 템플릿을 복제할지 결정
- `source_uids`: 근거가 된 레퍼런스. 나중에 "이 카피 어디서 나왔지?" 를 추적할 때 씁니다

---

## 문제 해결

| 증상 | 원인과 해결 |
|---|---|
| `FIGMA_TOKEN이 없습니다` | `.env` 에 토큰 미설정 |
| `403 Forbidden` | 토큰에 해당 파일 접근 권한 없음. 파일 소유 계정으로 발급했는지 확인 |
| 플러그인이 템플릿을 못 찾음 | 프레임 이름이 정확히 `template/cover` 인지 확인 (대소문자 무관, 공백 주의) |
| 텍스트가 안 바뀜 | 레이어 이름이 `#title` 등과 정확히 일치하는지 확인 |
| 폰트 오류 | 템플릿에 쓴 폰트가 로컬에 없음. Figma에서 폰트를 설치하거나 다른 폰트로 교체 |
| 프리뷰 한글 깨짐 | CJK 폰트 없음 → `apt-get install fonts-noto-cjk` 또는 Noto Sans KR 설치 |
| 이미지가 안 들어감 | `#image` 이름의 도형이 있는지, 이미지 URL이 살아있는지 확인 |
