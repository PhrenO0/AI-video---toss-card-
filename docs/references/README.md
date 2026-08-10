# 외부 레퍼런스 요약

외부 공개 문서 3건의 요약본. **원문 저자의 자료이며, 우리 프로젝트 문서가 아니다.**
채택 여부와 적용 방식은 [`../content-workflow.md`](../content-workflow.md)에 정리했다.

| # | 문서 | 주제 | 수집일 |
|---|---|---|---|
| 01 | [저장되는 카드뉴스 공식 프롬프트 공유](./01-카드뉴스-기획법.md) | 체류시간 중심 카드뉴스 기획법 | 2026-08-10 |
| 02 | [moongi-xiaohei-illustrations 사용 가이드](./02-손그림-일러스트-스킬.md) | 손그림 AI 일러스트 스킬 + 영상 워크플로우 | 2026-08-10 |
| 03 | [포스터 스타일 카탈로그 + 스킬](./03-포스터-스타일-스킬.md) | 포스터 디자인 스킬, 레이아웃 우선 원칙 | 2026-08-10 |

## 수집 방법

Notion 공개 페이지는 JS 렌더링이라 일반 HTTP 요청으로는 본문이 잡히지 않는다.
공개 API 엔드포인트로 받아서 파싱했다.

```bash
curl -sS -X POST "https://<subdomain>.notion.site/api/v3/loadPageChunk" \
  -H "Content-Type: application/json" \
  -d '{"pageId":"<uuid-with-dashes>","limit":200,"cursor":{"stack":[]},"chunkNumber":0,"verticalColumns":false}'
```

`pageId`는 URL 끝의 32자 hex에 UUID 하이픈(8-4-4-4-12)을 넣은 값이다.
응답 JSON의 `recordMap.block`을 순회하면 블록 순서대로 본문을 복원할 수 있다.

## 주의

- 요약본은 원문의 **핵심 논지와 규칙**만 옮긴 것이다. 이미지·첨부파일은 포함하지 않았다.
- 원문에 포함된 프롬프트·스킬은 **저자의 저작물**이다. 우리 콘텐츠에 그대로 복제해 배포하지 않는다.
- 원문 저자 본인도 "결과물을 그대로 복사해서 사용하는 것은 추천하지 않는다"고 명시했다.
