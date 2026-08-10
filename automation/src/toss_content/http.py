"""공통 HTTP 클라이언트 — 재시도, 레이트리밋 백오프, 타임아웃.

X/Meta API 모두 429를 자주 뱉기 때문에 `Retry-After`를 존중하는 얇은 래퍼를 둔다.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

log = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 20
MAX_RETRIES = 4
RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class HttpError(RuntimeError):
    def __init__(self, status: int, body: str, url: str):
        super().__init__(f"HTTP {status} for {url}: {body[:400]}")
        self.status = status
        self.body = body
        self.url = url


def request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    json_body: Any = None,
    timeout: int = DEFAULT_TIMEOUT,
    max_retries: int = MAX_RETRIES,
    session: requests.Session | None = None,
) -> Any:
    sess = session or requests
    delay = 2.0
    last_error: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            resp = sess.request(
                method,
                url,
                headers=headers,
                params=params,
                json=json_body,
                timeout=timeout,
            )
        except requests.RequestException as exc:  # 네트워크 레벨 실패
            last_error = exc
            if attempt == max_retries:
                break
            log.warning("네트워크 오류 (%s/%s) %s: %s", attempt, max_retries, url, exc)
            time.sleep(delay)
            delay *= 2
            continue

        if resp.status_code in RETRYABLE_STATUS and attempt < max_retries:
            wait = delay
            retry_after = resp.headers.get("Retry-After")
            if retry_after:
                try:
                    wait = max(wait, float(retry_after))
                except ValueError:
                    pass
            # X API v2는 x-rate-limit-reset(epoch)로 알려준다.
            reset = resp.headers.get("x-rate-limit-reset")
            if resp.status_code == 429 and reset:
                try:
                    wait = max(wait, min(float(reset) - time.time(), 120.0))
                except ValueError:
                    pass
            log.warning(
                "재시도 가능한 응답 %s (%s/%s) — %.1fs 대기 후 재시도: %s",
                resp.status_code, attempt, max_retries, wait, url,
            )
            time.sleep(max(wait, 1.0))
            delay *= 2
            continue

        if resp.status_code >= 400:
            raise HttpError(resp.status_code, resp.text, url)

        if not resp.content:
            return None
        return resp.json()

    raise HttpError(0, f"재시도 소진: {last_error}", url)


def get_json(url: str, **kwargs: Any) -> Any:
    return request_json("GET", url, **kwargs)


def post_json(url: str, **kwargs: Any) -> Any:
    return request_json("POST", url, **kwargs)
