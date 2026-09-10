"""Retry strategies with configurable backoff policies.

Provides :class:`RetryConfig` plus exponential, linear, constant, and
Fibonacci backoff strategies, all sharing :meth:`RetryStrategy.execute`
and :meth:`RetryStrategy.should_retry` semantics.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


class MaxRetriesExceededError(Exception):
    """Raised when all retry attempts have been exhausted."""

    def __init__(self, max_attempts: int, last_exception: Exception) -> None:
        self.max_attempts = max_attempts
        self.last_exception = last_exception
        super().__init__(
            f"Maximum retries ({max_attempts}) exceeded; last error: {last_exception}"
        )


@dataclass
class RetryConfig:
    """Configuration for retry behaviour."""

    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    jitter: bool = True
    retryable_exceptions: tuple[type[Exception], ...] = ()
    non_retryable_exceptions: tuple[type[Exception], ...] = ()


class RetryStrategy:
    """Base class for retry strategies."""

    def __init__(self, config: RetryConfig) -> None:
        self.config = config

    def calculate_delay(self, attempt: int) -> float:
        """Return the delay in seconds before the given 1-based attempt."""
        raise NotImplementedError

    def should_retry(self, attempt: int, exception: Exception) -> bool:
        """Return True when ``exception`` should be retried on this attempt."""
        if isinstance(exception, self.config.non_retryable_exceptions):
            return False
        if self.config.retryable_exceptions and not isinstance(
            exception, self.config.retryable_exceptions
        ):
            return False
        return attempt < self.config.max_attempts

    def execute(self, func: Callable[..., T], *args: object, **kwargs: object) -> T:
        """Execute ``func``, retrying failures until attempts are exhausted."""
        last_exception: Exception | None = None
        for attempt in range(1, self.config.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 - retries any caller error
                last_exception = exc
                if not self.should_retry(attempt, exc):
                    break
                time.sleep(self.calculate_delay(attempt))
        assert last_exception is not None, "execute requires max_attempts >= 1"
        raise MaxRetriesExceededError(self.config.max_attempts, last_exception)

    def _jitter(self, delay: float) -> float:
        """Apply +/- randomness to avoid synchronized retries."""
        if not self.config.jitter:
            return delay
        return delay * (0.5 + random.random())


class ExponentialBackoffRetry(RetryStrategy):
    """Delay grows exponentially: ``base_delay * multiplier ** (attempt - 1)``."""

    def __init__(self, config: RetryConfig, multiplier: float = 2.0) -> None:
        super().__init__(config)
        self.multiplier = multiplier

    def calculate_delay(self, attempt: int) -> float:
        delay = self._jitter(self.config.base_delay * (self.multiplier ** (attempt - 1)))
        return min(delay, self.config.max_delay)


class LinearBackoffRetry(RetryStrategy):
    """Delay grows linearly: ``base_delay + increment * (attempt - 1)``."""

    def __init__(self, config: RetryConfig, increment: float = 1.0) -> None:
        super().__init__(config)
        self.increment = increment

    def calculate_delay(self, attempt: int) -> float:
        delay = self._jitter(self.config.base_delay + self.increment * (attempt - 1))
        return min(delay, self.config.max_delay)


class ConstantDelayRetry(RetryStrategy):
    """Delay is always ``base_delay``."""

    def calculate_delay(self, attempt: int) -> float:
        return self._jitter(self.config.base_delay)


class FibonacciBackoffRetry(RetryStrategy):
    """Delay follows the Fibonacci sequence scaled by ``base_delay``."""

    def calculate_delay(self, attempt: int) -> float:
        delay = self._jitter(self.config.base_delay * self._fibonacci(attempt))
        return min(delay, self.config.max_delay)

    @staticmethod
    def _fibonacci(n: int) -> int:
        previous, current = 0, 1
        for _ in range(n - 1):
            previous, current = current, previous + current
        return current
