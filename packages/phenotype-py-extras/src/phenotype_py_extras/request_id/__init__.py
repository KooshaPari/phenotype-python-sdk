"""request_id: contextvars-based request-ID propagation + FastAPI middleware + structlog binding.

Absorbed from KooshaPari/phenotype-request-id (L5-114, 2026-06-20).
Public API: request_id_var, get_request_id, set_request_id, reset_request_id,
            clear_request_id, new_request_id, RequestIDMiddleware,
            bind_request_id_to_logger
"""

from .context import (
    request_id_var,
    get_request_id,
    set_request_id,
    reset_request_id,
    clear_request_id,
    new_request_id,
)
from .middleware import RequestIDMiddleware
from .generator import bind_request_id_to_logger

__all__ = [
    "request_id_var",
    "get_request_id",
    "set_request_id",
    "reset_request_id",
    "clear_request_id",
    "new_request_id",
    "RequestIDMiddleware",
    "bind_request_id_to_logger",
]