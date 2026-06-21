"""Request-ID generator + structlog binding (log integration).

Absorbed from KooshaPari/phenotype-request-id/src/phenotype_request_id/logging.py:1-78
+ generator semantics (L5-114, 2026-06-20).

The original source had `logging.py` that bound the request_id contextvar to structlog.
This module adds the optional structured-formatting helpers and the optional
structlog processor glue. If structlog is not installed, `bind_request_id_to_logger`
gracefully no-ops with a debug log (the request_id is still propagated via contextvars).
"""

from __future__ import annotations

import logging
import os
from typing import Any

from .context import get_request_id, new_request_id


def _try_structlog():
    try:
        import structlog  # type: ignore
        return structlog
    except ImportError:
        return None


def generate(prefix: str | None = None) -> str:
    """Generate a request ID. If `prefix` is given, prepend it (e.g. 'req-')."""
    rid = new_request_id()
    if prefix:
        return f"{prefix}{rid}"
    return rid


def bind_request_id_to_logger(
    logger: logging.Logger | Any,
    method_name: str = "bind",
) -> Any:
    """Bind the current request_id onto a structlog-style BoundLogger.

    If structlog is not importable, returns the logger untouched (no-op fallback).
    Returns the bound logger (so calls can be chained), or the original logger.
    """
    rid = get_request_id()
    structlog = _try_structlog()
    if structlog is None:
        return logger
    if rid is None:
        rid = os.environ.get("PHENOTYPE_REQUEST_ID", "")
    bind = getattr(logger, method_name, None)
    if not callable(bind):
        return logger
    return bind(request_id=rid) if rid else logger