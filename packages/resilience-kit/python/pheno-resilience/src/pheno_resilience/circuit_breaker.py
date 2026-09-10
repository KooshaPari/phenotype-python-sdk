"""Circuit breaker pattern for fault tolerance.

Provides the :class:`CircuitBreaker` primitive with CLOSED/OPEN/HALF_OPEN
states, a configurable failure threshold and recovery timeout, and call
statistics exposed through :meth:`CircuitBreaker.get_stats`.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeVar

T = TypeVar("T")


class CircuitBreakerError(Exception):
    """Base exception for circuit breaker errors."""


class CircuitBreakerState(str, Enum):
    """States of a circuit breaker."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(CircuitBreakerError):
    """Raised when a call is attempted through an open circuit."""

    def __init__(self, circuit_name: str, state: CircuitBreakerState) -> None:
        self.circuit_name = circuit_name
        self.state = state
        super().__init__(
            f"Circuit breaker '{circuit_name}' is {state.value}; call rejected"
        )


@dataclass
class CircuitBreakerConfig:
    """Configuration for :class:`CircuitBreaker` behaviour."""

    failure_threshold: int = 5
    failure_window: float = 60.0
    recovery_timeout: float = 30.0
    success_threshold: int = 3
    enable_monitoring: bool = True


class CircuitBreaker:
    """Fails fast once consecutive failures exceed a configured threshold."""

    def __init__(self, name: str, config: CircuitBreakerConfig | None = None) -> None:
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitBreakerState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._total_calls = 0
        self._total_successes = 0
        self._total_failures = 0
        self._opened_at: float | None = None

    @property
    def state(self) -> CircuitBreakerState:
        """Current state; OPEN transitions to HALF_OPEN after the recovery timeout."""
        if (
            self._state is CircuitBreakerState.OPEN
            and self._opened_at is not None
            and time.monotonic() - self._opened_at >= self.config.recovery_timeout
        ):
            self._state = CircuitBreakerState.HALF_OPEN
        return self._state

    @property
    def failure_count(self) -> int:
        """Consecutive failures since the last success or reset."""
        return self._failure_count

    @property
    def success_count(self) -> int:
        """Consecutive successes since the last failure or reset."""
        return self._success_count

    @property
    def is_closed(self) -> bool:
        """True when the circuit is closed and calls flow normally."""
        return self.state is CircuitBreakerState.CLOSED

    @property
    def is_open(self) -> bool:
        """True when the circuit is open and calls are rejected."""
        return self.state is CircuitBreakerState.OPEN

    @property
    def is_half_open(self) -> bool:
        """True when the circuit is probing for recovery."""
        return self.state is CircuitBreakerState.HALF_OPEN

    def call(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """Execute ``func`` through the circuit, recording the outcome."""
        state = self.state
        if state is CircuitBreakerState.OPEN:
            raise CircuitBreakerOpenError(self.name, state)

        self._total_calls += 1
        try:
            result = func(*args, **kwargs)
        except Exception:
            self._record_failure()
            raise
        self._record_success()
        return result

    def reset(self) -> None:
        """Reset the circuit to CLOSED and clear the consecutive counters."""
        self._state = CircuitBreakerState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._opened_at = None

    def get_stats(self) -> dict[str, Any]:
        """Return a snapshot of circuit statistics."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self._failure_count,
            "success_count": self._success_count,
            "total_calls": self._total_calls,
            "total_successes": self._total_successes,
            "total_failures": self._total_failures,
        }

    def _record_success(self) -> None:
        self._success_count += 1
        self._total_successes += 1
        if (
            self._state is CircuitBreakerState.HALF_OPEN
            and self._success_count >= self.config.success_threshold
        ):
            self.reset()

    def _record_failure(self) -> None:
        self._failure_count += 1
        self._total_failures += 1
        self._success_count = 0
        if (
            self._state is CircuitBreakerState.HALF_OPEN
            or self._failure_count >= self.config.failure_threshold
        ):
            self._state = CircuitBreakerState.OPEN
            self._opened_at = time.monotonic()
