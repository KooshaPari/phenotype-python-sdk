"""contextvars-based request-ID storage.

Absorbed from KooshaPari/phenotype-request-id/src/phenotype_request_id/context.py:1-46 (L5-114, 2026-06-20).
Zero external deps (stdlib only).
"""

from __future__ import annotations

import contextvars
import uuid


request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)


def new_request_id() -> str:
    """Generate a new opaque request ID (UUID4 hex, no dashes)."""
    return uuid.uuid4().hex


def get_request_id() -> str | None:
    """Return the current request ID (set by middleware), or None if unset."""
    return request_id_var.get()


def set_request_id(rid: str) -> contextvars.Token:
    """Set the request ID for the current context. Returns a Token for reset."""
    return request_id_var.set(rid)


def reset_request_id(token: contextvars.Token) -> None:
    """Reset the request ID using a Token returned by set_request_id."""
    request_id_var.reset(token)


def clear_request_id() -> None:
    """Unconditionally clear the request ID in the current context."""
    request_id_var.set(None)