"""pheno_resilience: resilience primitives for Pheno services.

Exposes the circuit breaker, retry strategies, health monitoring, and
error handling APIs documented in ``packages/resilience-kit/SPEC.md``.
"""

from pheno_resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitBreakerOpenError,
    CircuitBreakerState,
)
from pheno_resilience.error_handler import (
    ErrorCategory,
    ErrorContext,
    ErrorHandler,
    ErrorInfo,
    ErrorMetrics,
    ErrorSeverity,
)
from pheno_resilience.health import (
    HealthCheck,
    HealthChecker,
    HealthConfig,
    HealthMonitor,
    HealthStatus,
)
from pheno_resilience.retry import (
    ConstantDelayRetry,
    ExponentialBackoffRetry,
    FibonacciBackoffRetry,
    LinearBackoffRetry,
    MaxRetriesExceededError,
    RetryConfig,
    RetryStrategy,
)

__version__ = "0.1.0"

__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerError",
    "CircuitBreakerOpenError",
    "CircuitBreakerState",
    "ConstantDelayRetry",
    "ErrorCategory",
    "ErrorContext",
    "ErrorHandler",
    "ErrorInfo",
    "ErrorMetrics",
    "ErrorSeverity",
    "ExponentialBackoffRetry",
    "FibonacciBackoffRetry",
    "HealthCheck",
    "HealthChecker",
    "HealthConfig",
    "HealthMonitor",
    "HealthStatus",
    "LinearBackoffRetry",
    "MaxRetriesExceededError",
    "RetryConfig",
    "RetryStrategy",
]
