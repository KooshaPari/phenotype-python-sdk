# request_id specification

Zero-dependency (stdlib-only) request-ID propagation via `contextvars`,
with optional FastAPI/Starlette ASGI middleware and optional structlog
binding.

## 1. Public API

```python
from phenotype_py_extras.request_id import (
    request_id_var,                # contextvars.ContextVar[str | None]
    new_request_id,                # () -> str  (UUID4 hex, no dashes)
    get_request_id,                # () -> str | None
    set_request_id,                # (rid: str) -> Token
    reset_request_id,              # (token: Token) -> None
    clear_request_id,              # () -> None
    RequestIDMiddleware,           # ASGI middleware class
    bind_request_id_to_logger,     # (logger) -> BoundLogger | logger
)
```

## 2. Behavior

### Without middleware

`get_request_id()` returns `None`. Set it manually with `set_request_id(rid)`,
clear it with `clear_request_id()`. The Token-based reset is preferred in
middleware (`finally: reset_request_id(token)`).

### With `RequestIDMiddleware`

- The middleware inspects the inbound `X-Request-ID` header (configurable
  via `header_name` kwarg). If present, it's reused; otherwise a new UUID4
  hex is generated.
- The ID is set into the `request_id_var` ContextVar before the downstream
  app runs.
- The response `X-Request-ID` header echoes the ID for client correlation.
- The contextvar is reset in a `finally` block to prevent leakage across
  requests served on the same asyncio task.

### With `bind_request_id_to_logger`

- If `structlog` is importable, calls `logger.bind(request_id=...)` and
  returns the bound logger (chainable).
- If `structlog` is not installed, returns the original logger untouched.
- Falls back to `os.environ["PHENOTYPE_REQUEST_ID"]` if the contextvar is
  unset (allows end-to-end correlation in non-async contexts).

## 3. Installation

```bash
pip install phenotype-py-extras           # core (stdlib only)
pip install "phenotype-py-extras[web]"    # adds fastapi (for middleware)
pip install "phenotype-py-extras[observability]"  # adds structlog
```

## 4. See also

- `phenotype-request-id` (deleted 2026-06-20) — original source repo.
- `findings/2026-06-19-L5-114-phenotype-request-id-absorption.md` — L5-114 audit.