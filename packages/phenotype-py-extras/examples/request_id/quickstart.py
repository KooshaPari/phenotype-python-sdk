"""Quickstart: contextvars request-ID + FastAPI middleware.

Run: python examples/request_id/quickstart.py
"""

from __future__ import annotations

from phenotype_py_extras.request_id import (
    RequestIDMiddleware,
    get_request_id,
    new_request_id,
    set_request_id,
    reset_request_id,
)


def contextvar_demo() -> None:
    """Pure contextvars usage — no FastAPI required."""
    rid = new_request_id()
    token = set_request_id(rid)
    try:
        assert get_request_id() == rid
        print(f"Current request_id: {get_request_id()}")
    finally:
        reset_request_id(token)
    assert get_request_id() is None
    print("Context reset OK.")


def middleware_demo(app) -> None:
    """Wrap a FastAPI/Starlette app with RequestIDMiddleware."""
    app.add_middleware(RequestIDMiddleware)
    print(f"Wrapped {app!r} with RequestIDMiddleware")


if __name__ == "__main__":
    contextvar_demo()

    try:
        from fastapi import FastAPI  # type: ignore

        app = FastAPI()
        middleware_demo(app)
    except ImportError:
        print("FastAPI not installed; skip middleware_demo (pip install 'phenotype-py-extras[web]').")