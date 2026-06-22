"""FastAPI/Starlette middleware that propagates the X-Request-ID header.

Absorbed from KooshaPari/phenotype-request-id/src/phenotype_request_id/fastapi.py:1-104
(L5-114, 2026-06-20). Import rewritten to phenotype_py_extras.request_id.

Behaviour:
- If the inbound request has `X-Request-ID`, reuse it (preserves upstream trace IDs).
- Otherwise, generate a new one via `new_request_id()`.
- Set it into `request_id_var` contextvar before the downstream app runs.
- Echo it back as a response header so the client can correlate logs.
- Always reset the contextvar in a `finally` to prevent leakage across requests
  served on the same asyncio task.
"""

from __future__ import annotations

import contextvars
from .context import new_request_id, reset_request_id, set_request_id


HEADER_NAME = "X-Request-ID"


class RequestIDMiddleware:
    """ASGI middleware (works with FastAPI, Starlette, Quart).

    Wrap your app:
        app.add_middleware(RequestIDMiddleware)

    Or for raw ASGI:
        app = RequestIDMiddleware(app)
    """

    def __init__(self, app, header_name: str = HEADER_NAME) -> None:
        self.app = app
        self.header_name = header_name
        self._encoded_header = header_name.lower().encode("latin-1")

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        rid = _extract_header(scope.get("headers") or [], self._encoded_header)
        if not rid:
            rid = new_request_id()

        token: contextvars.Token = set_request_id(rid)

        async def _send_with_header(message):
            if message.get("type") == "http.response.start":
                headers = [
                    (key, value)
                    for key, value in list(message.get("headers") or [])
                    if key.lower() != self._encoded_header
                ]
                headers.append(
                    (self._encoded_header, rid.encode("latin-1"))
                )
                message = {**message, "headers": headers}
            await send(message)

        try:
            await self.app(scope, receive, _send_with_header)
        finally:
            reset_request_id(token)


def _extract_header(headers: list[tuple[bytes, bytes]], name_b: bytes) -> str | None:
    for k, v in headers:
        if k.lower() == name_b:
            try:
                return v.decode("latin-1")
            except UnicodeDecodeError:
                return None
    return None
