"""Error handling: categorization, severity, metrics, and error records."""

from __future__ import annotations

import traceback
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

Handler = Callable[["ErrorInfo"], None]


class ErrorSeverity(str, Enum):
    """Severity levels for errors."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(str, Enum):
    """Functional categories for errors."""

    NETWORK = "network"
    TIMEOUT = "timeout"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    RATE_LIMIT = "rate_limit"
    NOT_FOUND = "not_found"
    INTERNAL = "internal"
    UNKNOWN = "unknown"


@dataclass
class ErrorContext:
    """Contextual metadata attached to an error."""

    operation_name: str
    operation_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: datetime = field(default_factory=datetime.now)
    user_context: dict[str, Any] = field(default_factory=dict)
    system_context: dict[str, Any] = field(default_factory=dict)
    previous_errors: list[ErrorInfo] = field(default_factory=list)


@dataclass
class ErrorInfo:
    """Full record of a single error occurrence."""

    exception: Exception
    category: ErrorCategory
    severity: ErrorSeverity | None = None
    context: ErrorContext | None = None
    traceback_str: str = field(default_factory=traceback.format_exc)
    metadata: dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0

    def __post_init__(self) -> None:
        if self.severity is None:
            self.severity = _SEVERITY_BY_CATEGORY.get(
                self.category, ErrorSeverity.MEDIUM
            )


@dataclass
class ErrorMetrics:
    """Aggregate error counters."""

    total_errors: int = 0
    errors_by_category: dict[str, int] = field(default_factory=dict)
    errors_by_severity: dict[str, int] = field(default_factory=dict)
    successful_operations: int = 0
    retry_attempts: int = 0
    circuit_breaker_activations: int = 0


_TYPE_NETWORK_PATTERNS = ("connection", "network", "timeout", "socket", "dns")
_MESSAGE_NETWORK_PATTERNS = ("connection", "network", "timed out", "timeout")
_MESSAGE_RATE_LIMIT_PATTERNS = ("rate limit", "too many requests", "throttl")
_MESSAGE_AUTH_PATTERNS = (
    "unauthorized",
    "authentication",
    "forbidden",
    "permission",
)
_MESSAGE_VALIDATION_PATTERNS = ("invalid", "validation", "malformed")

_SEVERITY_BY_CATEGORY = {
    ErrorCategory.AUTHENTICATION: ErrorSeverity.HIGH,
    ErrorCategory.AUTHORIZATION: ErrorSeverity.HIGH,
    ErrorCategory.INTERNAL: ErrorSeverity.HIGH,
    ErrorCategory.NETWORK: ErrorSeverity.MEDIUM,
    ErrorCategory.TIMEOUT: ErrorSeverity.MEDIUM,
    ErrorCategory.RATE_LIMIT: ErrorSeverity.MEDIUM,
    ErrorCategory.NOT_FOUND: ErrorSeverity.LOW,
    ErrorCategory.VALIDATION: ErrorSeverity.LOW,
    ErrorCategory.UNKNOWN: ErrorSeverity.CRITICAL,
}


class ErrorHandler:
    """Categorizes errors, tracks metrics, and dispatches registered handlers."""

    def __init__(self) -> None:
        self.error_handlers: dict[ErrorCategory, list[Handler]] = {}
        self.error_stats: dict[ErrorCategory, dict[str, int]] = {}
        self.metrics = ErrorMetrics()

    def register_handler(self, category: ErrorCategory, handler: Handler) -> None:
        """Register a handler callback for a category."""
        self.error_handlers.setdefault(category, []).append(handler)

    def categorize_error(self, error: Exception) -> ErrorCategory:
        """Categorize an exception by type name and message patterns."""
        type_name = type(error).__name__.lower()
        message = str(error).lower()

        if any(pattern in type_name for pattern in _TYPE_NETWORK_PATTERNS):
            return ErrorCategory.NETWORK
        if isinstance(error, ValueError):
            return ErrorCategory.VALIDATION
        if any(pattern in message for pattern in _MESSAGE_NETWORK_PATTERNS):
            return ErrorCategory.NETWORK
        if any(pattern in message for pattern in _MESSAGE_RATE_LIMIT_PATTERNS):
            return ErrorCategory.RATE_LIMIT
        if any(pattern in message for pattern in _MESSAGE_AUTH_PATTERNS):
            return ErrorCategory.AUTHENTICATION
        if any(pattern in message for pattern in _MESSAGE_VALIDATION_PATTERNS):
            return ErrorCategory.VALIDATION
        return ErrorCategory.UNKNOWN

    def determine_severity(
        self, error: Exception, category: ErrorCategory
    ) -> ErrorSeverity:
        """Determine severity from the error and its category."""
        return _SEVERITY_BY_CATEGORY.get(category, ErrorSeverity.MEDIUM)

    def create_error_info(
        self, error: Exception, context: ErrorContext | None = None
    ) -> ErrorInfo:
        """Build a full :class:`ErrorInfo` record for an exception."""
        category = self.categorize_error(error)
        severity = self.determine_severity(error, category)
        return ErrorInfo(
            exception=error,
            category=category,
            severity=severity,
            context=context,
            traceback_str="".join(
                traceback.format_exception(type(error), error, error.__traceback__)
            ),
        )

    async def handle_error(self, error_info: ErrorInfo) -> None:
        """Record an error, update metrics, and dispatch registered handlers."""
        self.metrics.total_errors += 1
        self.metrics.errors_by_category[error_info.category.value] = (
            self.metrics.errors_by_category.get(error_info.category.value, 0) + 1
        )
        self.metrics.errors_by_severity[error_info.severity.value] = (
            self.metrics.errors_by_severity.get(error_info.severity.value, 0) + 1
        )
        stats = self.error_stats.setdefault(error_info.category, {"count": 0})
        stats["count"] += 1
        for handler in self.error_handlers.get(error_info.category, []):
            handler(error_info)

    def get_metrics(self) -> ErrorMetrics:
        """Return the current aggregate metrics."""
        return self.metrics

    def reset_metrics(self) -> None:
        """Clear all accumulated error metrics and per-category stats."""
        self.metrics = ErrorMetrics()
        self.error_stats = {}
