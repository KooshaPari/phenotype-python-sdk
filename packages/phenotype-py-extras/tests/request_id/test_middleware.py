"""Tests for RequestIDMiddleware (FastAPI/Starlette ASGI)."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from phenotype_py_extras.request_id.context import get_request_id
from phenotype_py_extras.request_id.middleware import RequestIDMiddleware


HEADER = b"x-request-id"


def _make_scope(headers: list[tuple[bytes, bytes]] | None = None) -> dict[str, Any]:
    return {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": headers or [],
    }


async def _noop_receive():
    return {"type": "http.request", "body": b"", "more_body": False}


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro) if False else asyncio.run(coro)


class _CaptureApp:
    def __init__(self):
        self.received_rid: str | None = None
        self.response_headers: list[tuple[bytes, bytes]] = []

    async def __call__(self, scope, receive, send):
        self.received_rid = get_request_id()
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b"ok"})


def test_middleware_generates_rid_when_missing():
    app = _CaptureApp()
    middleware = RequestIDMiddleware(app)

    sent_messages: list[dict] = []

    async def send(msg):
        sent_messages.append(msg)

    async def run():
        await middleware(_make_scope(), _noop_receive, send)

    _run(run())
    assert app.received_rid is not None
    assert len(app.received_rid) == 32
    start = next(m for m in sent_messages if m["type"] == "http.response.start")
    echoed = dict(start["headers"]).get(HEADER)
    assert echoed is not None
    assert echoed.decode("latin-1") == app.received_rid


def test_middleware_reuses_inbound_rid():
    app = _CaptureApp()
    middleware = RequestIDMiddleware(app)
    rid = "upstream-trace-abc"

    sent: list[dict] = []

    async def send(msg):
        sent.append(msg)

    async def run():
        await middleware(_make_scope([(HEADER, rid.encode())]), _noop_receive, send)

    _run(run())
    assert app.received_rid == "upstream-trace-abc"
    start = next(m for m in sent if m["type"] == "http.response.start")
    assert dict(start["headers"]).get(HEADER) == b"upstream-trace-abc"


def test_middleware_resets_context_after_request():
    app = _CaptureApp()
    middleware = RequestIDMiddleware(app)

    async def run():
        await middleware(_make_scope(), _noop_receive, _noop_send := _make_send())

    def _make_send():
        async def send(msg):
            pass

        return send

    _run(run())
    assert get_request_id() is None


def test_middleware_passes_through_non_http_scope():
    app = _CaptureApp()
    middleware = RequestIDMiddleware(app)

    async def run():
        scope = {"type": "lifespan"}
        await middleware(scope, _noop_receive, _no_op_send := _make_send())

    def _make_send():
        async def send(msg):
            pass

        return send

    _run(run())
    assert app.received_rid is None


def test_middleware_handles_uppercase_header_name():
    app = _CaptureApp()
    middleware = RequestIDMiddleware(app, header_name="X-Request-ID")
    sent = []

    async def send(msg):
        sent.append(msg)

    async def run():
        await middleware(_make_scope([(b"X-Request-ID", b"hello-upper")]), _noop_receive, send)

    _run(run())
    assert app.received_rid == "hello-upper"