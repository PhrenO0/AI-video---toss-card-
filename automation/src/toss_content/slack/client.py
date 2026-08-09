"""Slack 전송 클라이언트.

토스처럼 **Enterprise Grid**를 쓰는 조직은 앱 설치에 조직 관리자 승인이 필요하다.
승인이 떨어지기 전에도 파이프라인이 굴러가야 하므로 전송 경로를 두 개 둔다.

1. ``bot`` — Bot User OAuth Token(``xoxb-``) 기반 Web API.
   채널 조회·파일 업로드·스레드 답글까지 다 되는 정식 경로.
2. ``webhook`` — Incoming Webhook URL 하나만으로 특정 채널에 게시.
   권한이 가장 좁아 승인받기 쉬우며, 앱 승인 대기 중 임시 경로로 쓴다.

둘 다 없으면 ``dry-run``으로 표준출력에 찍는다(로컬 개발/CI 검증용).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Literal

import requests

from ..http import post_json

log = logging.getLogger(__name__)

SLACK_API = "https://slack.com/api"

Mode = Literal["bot", "webhook", "dry-run"]


class SlackError(RuntimeError):
    pass


class SlackClient:
    def __init__(self, bot_token: str = "", webhook_url: str = ""):
        self.bot_token = bot_token.strip()
        self.webhook_url = webhook_url.strip()

    @property
    def mode(self) -> Mode:
        if self.bot_token:
            return "bot"
        if self.webhook_url:
            return "webhook"
        return "dry-run"

    # ------------------------------------------------------------- messages
    def post_message(
        self,
        text: str,
        blocks: list[dict[str, Any]] | None = None,
        channel: str = "",
        thread_ts: str = "",
    ) -> dict[str, Any]:
        """메시지 전송. 반환값의 ``ts``는 스레드 답글에 쓴다(webhook 모드에선 없음)."""
        payload: dict[str, Any] = {"text": text}
        if blocks:
            payload["blocks"] = blocks

        if self.mode == "bot":
            if not channel:
                raise SlackError("bot 모드에서는 channel이 필요합니다.")
            payload["channel"] = channel
            if thread_ts:
                payload["thread_ts"] = thread_ts
            return self._web_api("chat.postMessage", payload)

        if self.mode == "webhook":
            if thread_ts:
                log.warning("webhook 모드는 스레드 답글을 지원하지 않습니다 — 새 메시지로 보냅니다.")
            resp = requests.post(self.webhook_url, json=payload, timeout=20)
            if resp.status_code >= 400 or resp.text.strip() != "ok":
                raise SlackError(f"Webhook 실패 {resp.status_code}: {resp.text[:200]}")
            return {"ok": True, "mode": "webhook"}

        print("[slack dry-run]", json.dumps(payload, ensure_ascii=False, indent=2))
        return {"ok": True, "mode": "dry-run"}

    def upload_file(
        self, path: Path, channel: str, title: str = "", initial_comment: str = ""
    ) -> dict[str, Any]:
        """파일 업로드(files.getUploadURLExternal → completeUploadExternal 2단계)."""
        if self.mode != "bot":
            log.warning("파일 업로드는 bot 토큰이 필요합니다 — 건너뜁니다: %s", path)
            return {"ok": False, "reason": "bot-token-required"}

        path = Path(path)
        length = path.stat().st_size
        step1 = self._web_api(
            "files.getUploadURLExternal",
            {"filename": path.name, "length": length},
            form=True,
        )
        upload_url, file_id = step1["upload_url"], step1["file_id"]

        with path.open("rb") as fh:
            resp = requests.post(upload_url, files={"file": (path.name, fh)}, timeout=120)
        if resp.status_code >= 400:
            raise SlackError(f"파일 업로드 실패 {resp.status_code}: {resp.text[:200]}")

        return self._web_api(
            "files.completeUploadExternal",
            {
                "files": [{"id": file_id, "title": title or path.name}],
                "channel_id": channel,
                "initial_comment": initial_comment,
            },
        )

    def resolve_channel_id(self, name: str) -> str:
        """``#채널명``을 채널 ID로 바꾼다. 이미 ID면 그대로 반환."""
        name = name.strip()
        if not name.startswith("#"):
            return name
        target = name.lstrip("#")
        cursor = ""
        while True:
            payload = self._web_api(
                "conversations.list",
                {
                    "limit": 1000,
                    "cursor": cursor,
                    "types": "public_channel,private_channel",
                    "exclude_archived": "true",
                },
                form=True,
                method="GET",
            )
            for channel in payload.get("channels", []):
                if channel.get("name") == target:
                    return channel["id"]
            cursor = (payload.get("response_metadata") or {}).get("next_cursor", "")
            if not cursor:
                raise SlackError(f"채널을 찾을 수 없습니다: {name}")

    # ------------------------------------------------------------- internal
    def _web_api(
        self,
        method_name: str,
        payload: dict[str, Any],
        form: bool = False,
        method: str = "POST",
    ) -> dict[str, Any]:
        url = f"{SLACK_API}/{method_name}"
        headers = {"Authorization": f"Bearer {self.bot_token}"}
        if form:
            # 일부 메서드는 JSON 본문을 받지 않고 폼/쿼리만 받는다.
            resp = requests.request(
                method, url, headers=headers, params=payload if method == "GET" else None,
                data=payload if method != "GET" else None, timeout=30,
            )
            data = resp.json()
        else:
            headers["Content-Type"] = "application/json; charset=utf-8"
            data = post_json(url, headers=headers, json_body=payload)

        if not data.get("ok"):
            raise SlackError(f"{method_name} 실패: {data.get('error')} ({data})")
        return data


def from_settings(settings) -> SlackClient:
    return SlackClient(settings.slack_bot_token, settings.slack_webhook_url)
