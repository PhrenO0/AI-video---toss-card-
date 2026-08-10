"""Figma REST API 클라이언트.

**중요한 제약**: Figma REST API는 파일을 *읽고* 이미지로 *내보낼* 수만 있고,
노드를 새로 만들거나 텍스트를 바꾸는 쓰기 작업은 지원하지 않는다.
카드뉴스를 실제로 "찍어내는" 일은 Figma **플러그인 API**로만 가능하므로,
이 저장소의 `figma-plugin/`이 그 역할을 맡는다.

역할 분담:
- 이 클라이언트: 템플릿 구조 읽기 / 완성본 PNG export / 리뷰 코멘트 달기
- `figma-plugin/`: 카드뉴스 spec(JSON)을 받아 실제 프레임 생성

참고: https://www.figma.com/developers/api
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Iterable

import requests

from ..http import get_json, post_json

log = logging.getLogger(__name__)

FIGMA_API = "https://api.figma.com/v1"

_FILE_KEY_RE = re.compile(r"figma\.com/(?:file|design|proto)/([A-Za-z0-9]+)")


def extract_file_key(url_or_key: str) -> str:
    """Figma URL에서 파일 키를 뽑는다. 이미 키면 그대로 반환."""
    match = _FILE_KEY_RE.search(url_or_key)
    if match:
        return match.group(1)
    return url_or_key.strip().strip("/")


def normalize_node_id(node_id: str) -> str:
    """URL의 `0-1` 형식을 API가 쓰는 `0:1` 형식으로 바꾼다."""
    node_id = node_id.strip()
    return node_id.replace("-", ":") if "-" in node_id and ":" not in node_id else node_id


class FigmaError(RuntimeError):
    pass


class FigmaClient:
    def __init__(self, token: str, file_key: str = ""):
        if not token:
            raise FigmaError(
                "FIGMA_TOKEN이 없습니다. Figma → Settings → Security → "
                "Personal access tokens 에서 발급해 .env에 넣어주세요."
            )
        self.token = token.strip()
        self.file_key = extract_file_key(file_key) if file_key else ""

    @property
    def _headers(self) -> dict[str, str]:
        return {"X-Figma-Token": self.token}

    def _key(self, file_key: str = "") -> str:
        key = extract_file_key(file_key) if file_key else self.file_key
        if not key:
            raise FigmaError("Figma file_key가 설정되지 않았습니다.")
        return key

    # ------------------------------------------------------------------ read
    def whoami(self) -> dict[str, Any]:
        """토큰 유효성 확인용."""
        return get_json(f"{FIGMA_API}/me", headers=self._headers)

    def get_file(self, file_key: str = "", depth: int | None = None) -> dict[str, Any]:
        """파일 전체 노드 트리. `depth`로 탐색 깊이를 제한하면 응답이 훨씬 가볍다."""
        params = {"depth": depth} if depth else None
        return get_json(
            f"{FIGMA_API}/files/{self._key(file_key)}", headers=self._headers, params=params
        )

    def get_nodes(self, node_ids: Iterable[str], file_key: str = "") -> dict[str, Any]:
        ids = ",".join(normalize_node_id(n) for n in node_ids)
        return get_json(
            f"{FIGMA_API}/files/{self._key(file_key)}/nodes",
            headers=self._headers,
            params={"ids": ids},
        )

    def list_frames(self, file_key: str = "", page_name: str = "") -> list[dict[str, Any]]:
        """페이지별 최상위 프레임 목록 — 템플릿 노드 ID를 찾을 때 쓴다."""
        document = self.get_file(file_key, depth=2).get("document", {})
        frames: list[dict[str, Any]] = []
        for page in document.get("children", []):
            if page_name and page.get("name") != page_name:
                continue
            for node in page.get("children", []):
                if node.get("type") in {"FRAME", "COMPONENT", "COMPONENT_SET"}:
                    frames.append(
                        {
                            "id": node["id"],
                            "name": node.get("name", ""),
                            "type": node["type"],
                            "page": page.get("name", ""),
                        }
                    )
        return frames

    # ---------------------------------------------------------------- export
    def export_images(
        self,
        node_ids: Iterable[str],
        file_key: str = "",
        fmt: str = "png",
        scale: float = 2.0,
    ) -> dict[str, str]:
        """노드를 렌더링해서 {node_id: 이미지 URL} 반환. URL은 유효기간이 짧다."""
        ids = [normalize_node_id(n) for n in node_ids]
        payload = get_json(
            f"{FIGMA_API}/images/{self._key(file_key)}",
            headers=self._headers,
            params={"ids": ",".join(ids), "format": fmt, "scale": scale},
        ) or {}
        if payload.get("err"):
            raise FigmaError(f"이미지 export 실패: {payload['err']}")
        return {k: v for k, v in (payload.get("images") or {}).items() if v}

    def download_images(
        self,
        node_ids: Iterable[str],
        out_dir: Path,
        file_key: str = "",
        fmt: str = "png",
        scale: float = 2.0,
        name_map: dict[str, str] | None = None,
    ) -> list[Path]:
        """export 후 로컬에 저장. `name_map`으로 파일명을 지정할 수 있다."""
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        urls = self.export_images(node_ids, file_key, fmt, scale)

        saved: list[Path] = []
        for node_id, url in urls.items():
            stem = (name_map or {}).get(node_id) or node_id.replace(":", "-")
            path = out_dir / f"{stem}.{fmt}"
            resp = requests.get(url, timeout=120)
            resp.raise_for_status()
            path.write_bytes(resp.content)
            saved.append(path)
            log.info("Figma 이미지 저장: %s", path)
        return saved

    # --------------------------------------------------------------- comment
    def post_comment(self, message: str, file_key: str = "", node_id: str = "") -> dict[str, Any]:
        """리뷰 코멘트. 노드를 지정하면 해당 프레임에 핀으로 붙는다."""
        body: dict[str, Any] = {"message": message}
        if node_id:
            body["client_meta"] = {
                "node_id": normalize_node_id(node_id),
                "node_offset": {"x": 0, "y": 0},
            }
        return post_json(
            f"{FIGMA_API}/files/{self._key(file_key)}/comments",
            headers={**self._headers, "Content-Type": "application/json"},
            json_body=body,
        )


def from_settings(settings) -> FigmaClient:
    return FigmaClient(settings.figma_token, settings.figma.file_key)
