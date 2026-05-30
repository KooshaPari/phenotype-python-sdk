# ADR-002: Retry Strategy Design

**Document ID:** PHENOTYPE_RESILIENCEKIT_ADR_002  
**Status:** Accepted  
**Last Updated:** 2026-04-03  
**Author:** Phenotype Architecture Team

---

## Table of Contents

1. [Title](#title)
2. [Status](#status)
3. [Context](#context)
4. [Decision](#decision)
5. [Consequences](#consequences)
6. [Implementation Details](#implementation-details)
7. [Code Examples](#code-examples)
8. [Cross-References](#cross-references)

---

## Title

Retry Strategy Design for ResilienceKit

## Status

**Accepted** — Implemented in Python and Rust, planned for Go.

---

## Context

### Problem Statement

Transient failures are inevitable in distributed systems. Network timeouts, temporary
service unavailability, and resource contention cause operations to fail intermittently.
Without retry logic, every transient failure becomes a permanent user-facing error.

However, naive retry strategies can make problems worse:
- **Thundering herd**: Synchronized retries from many clients overwhelm recovering services
- **Retry amplification**: Each retry multiplies the load on an already struggling service
- **Resource exhaustion**: Retrying operations consume threads, connections, and memory
- **Cascading failures**: Retries to a failing service can cause the caller to fail too

### Requirements

1. **Multiple Strategies**: Support different backoff strategies for different failure modes
2. **Jitter**: Add randomness to retry delays to prevent thundering herd
3. **Configurable**: Allow per-operation tuning of retry parameters
4. **Exception Filtering**: Distinguish retryable from non-retryable errors
5. **Async-Native**: Support async/await without blocking threads
6. **Context-Aware**: Provide retry context (attempt number, elapsed time) to operations
7. **Observable**: Track retry attempts, success rates, and timing
8. **Composable**: Work with circuit breakers, bulkheads, and timeouts

### Existing Solutions Evaluated

| Solution | Pros | Cons |
|----------|------|------|
| **tenacity** (Python) | Mature, feature-rich | Python-only, complex API |
| **Polly** (.NET) | Comprehensive, well-documented | .NET-only |
| **backoff** (Python) | Simple, decorator-based | Limited strategies |
| **tokio-retry** (Rust) | Async-native, simple | Limited to Rust |
| **Custom implementation** | Multi-language, ecosystem fit | Development cost |

### Decision Drivers

- Multi-language consistency is critical for the Phenotype ecosystem
- Async-first design is mandatory
- Need for multiple backoff strategies with jitter
- Integration with other resilience patterns (circuit breaker, bulkhead)

---

## Decision

We will implement a Retry system with the following design:

### Supported Backoff Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│              Retry Strategy Comparison                          │
├──────────────────┬──────────────────────────────────────────────┤
│  Strategy        │  Delay Formula                               │
├──────────────────┼──────────────────────────────────────────────┤
│  Exponential     │  delay = base * (multiplier ^ (attempt-1))   │
│  Linear          │  delay = base + (increment * (attempt-1))    │
│  Constant        │  delay = base (fixed)                        │
│  Fibonacci       │  delay = base * fibonacci(attempt)           │
│  Adaptive        │  delay = base * 2^consecutive_failures       │
│  Custom          │  User-defined function                       │
└──────────────────┴──────────────────────────────────────────────┘
```

### Strategy Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│              When to Use Each Strategy                          │
├──────────────────┬──────────────────────────────────────────────┤
│  Strategy        │  Best For                                    │
├──────────────────┼──────────────────────────────────────────────┤
│  Exponential     │  General purpose, external APIs              │
│  Linear          │  Predictable recovery patterns               │
│  Constant        │  Quick retries for very transient errors     │
│  Fibonacci       │  Balanced growth, moderate failures          │
│  Adaptive        │  Dynamic environments, varying failure rates │
│  Custom          │  Specialized requirements                    │
└──────────────────┴──────────────────────────────────────────────┘
```

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Retry System Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    RetryManager                            │ │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │ │
│  │  │ Exponential   │  │ Linear        │  │ Adaptive      │ │ │
│  │  │ BackoffRetry  │  │ BackoffRetry  │  │ Retry         │ │ │
│  │  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘ │ │
│  │          │                  │                  │         │ │
│  │          └──────────────────┼──────────────────┘         │ │
│  │                             ▼                            │ │
│  │              ┌─────────────────────────┐                 │ │
│  │              │    RetryConfig          │                 │ │
│  │              │  - max_attempts         │                 │ │
│  │              │  - base_delay           │                 │ │
│  │              │  - max_delay            │                 │ │
│  │              │  - jitter               │                 │ │
│  │              │  - retryable_exceptions │                 │ │
│  │              │  - callbacks            │                 │ │
│  │              └─────────────────────────┘                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Execution Flow:                                               │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌───────────┐ │
│  │  Call   │───►│  Try     │───►│  Success │───►│  Return   │ │
│  │  Func   │    │  Op      │    │  ?       │    │  Result   │ │
│  └─────────┘    └────┬─────┘    └────┬─────┘    └───────────┘ │
│                      │  No            │ Yes                    │
│                      ▼                │                        │
│               ┌──────────────┐       │                        │
│               │  Retryable?  │       │                        │
│               └──────┬───────┘       │                        │
│                  Yes │  No           │                        │
│                      ▼    ▼          │                        │
│               ┌────────┐ ┌────────┐  │                        │
│               │Backoff │ │Raise   │  │                        │
│               │+ Jitter│ │Error   │  │                        │
│               └───┬────┘ └────────┘  │                        │
│                   │                  │                        │
│                   └──────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Jitter Implementation

ResilienceKit uses ±25% jitter to prevent thundering herd:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Jitter Application                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Without Jitter:                  With Jitter (±25%):          │
│                                                                 │
│  Client A:  ──1s───2s───4s───8s   Client A:  ──0.9s──1.8s──3.2s│
│  Client B:  ──1s───2s───4s───8s   Client B:  ──1.1s──2.4s──5.0s│
│  Client C:  ──1s───2s───4s───8s   Client C:  ──0.8s──1.6s──3.6s│
│                                                                 │
│  All clients retry simultaneously    Retries are spread out     │
│  causing thundering herd             preventing overload        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Retry Decision Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│              Retry Decision Flow                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Operation Failed                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────┐                                       │
│  │ Max attempts reached?│──Yes──► Raise MaxRetriesExceededError│
│  └─────────┬───────────┘                                       │
│            │ No                                                │
│            ▼                                                   │
│  ┌─────────────────────┐                                       │
│  │ Exception in         │──Yes──► Raise immediately (no retry) │
│  │ non_retryable list?  │                                       │
│  └─────────┬───────────┘                                       │
│            │ No                                                │
│            ▼                                                   │
│  ┌─────────────────────┐                                       │
│  │ Exception in         │──No───► Raise immediately (no retry) │
│  │ retryable list?      │                                       │
│  └─────────┬───────────┘                                       │
│            │ Yes                                               │
│            ▼                                                   │
│  ┌─────────────────────┐                                       │
│  │ Calculate delay      │                                       │
│  │ (strategy + jitter)  │                                       │
│  └─────────┬───────────┘                                       │
│            │                                                   │
│            ▼                                                   │
│  ┌─────────────────────┐                                       │
│  │ Call on_retry        │                                       │
│  │ callback             │                                       │
│  └─────────┬───────────┘                                       │
│            │                                                   │
│            ▼                                                   │
│  ┌─────────────────────┐                                       │
│  │ Wait (async/sync)    │                                       │
│  └─────────┬───────────┘                                       │
│            │                                                   │
│            ▼                                                   │
│  ┌─────────────────────┐                                       │
│  │ Retry operation      │                                       │
│  └─────────────────────┘                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Consequences

### Positive Consequences

1. **Transient Failure Recovery**: Operations that fail due to temporary issues (network
   blips, service restarts, resource contention) are automatically retried, significantly
   improving success rates without manual intervention.

2. **Thundering Herd Prevention**: Jitter (±25%) randomizes retry timing across clients,
   preventing synchronized retry storms that could overwhelm recovering services.

3. **Strategy Flexibility**: Five built-in strategies (exponential, linear, constant,
   Fibonacci, adaptive) plus custom strategy support allow optimal retry behavior for
   each failure mode and service dependency.

4. **Exception Filtering**: Distinguishing between retryable and non-retryable exceptions
   prevents wasted retries on errors that won't resolve themselves (validation errors,
   authentication failures).

5. **Async-Native Design**: Non-blocking retry waits using `asyncio.sleep` (Python) and
   `tokio::time::sleep` (Rust) ensure threads are not blocked during backoff periods,
   enabling high-concurrency retry operations.

6. **Context Awareness**: The retry context provides attempt number, max attempts,
   elapsed time, and last error to the operation, enabling intelligent behavior
   (e.g., reducing request scope on later attempts, logging context).

7. **Callback System**: `on_retry`, `on_success`, and `on_failure` callbacks enable
   integration with metrics, logging, alerting, and external monitoring systems.

8. **Decorator Support**: The `@with_retry` decorator provides a simple way to add retry
   logic to any function without modifying its implementation, supporting both sync and
   async functions.

### Negative Consequences

1. **Increased Latency**: Retries add latency to operations that eventually succeed.
   With exponential backoff, the total wait time can be significant (e.g., 31 seconds
   for 5 attempts with base=1s, multiplier=2).

2. **Resource Consumption**: Each retry attempt consumes resources (CPU, memory, network
   connections). Under heavy failure conditions, retry traffic can become a significant
   portion of total traffic.

3. **Complexity**: Multiple strategies, jitter, exception filtering, and callbacks
   increase the cognitive load for developers configuring retry behavior.

4. **Testing Difficulty**: Testing retry behavior requires mocking time, simulating
   failures, and verifying retry counts and delays, which adds complexity to test suites.

5. **No Retry Budget**: The current implementation does not limit total retry traffic
   as a percentage of original traffic, which could lead to retry amplification under
   sustained failure conditions.

6. **No Distributed Coordination**: Each process independently decides whether to retry,
   which can lead to amplified load on a recovering service when many instances retry
   simultaneously (mitigated by jitter but not eliminated).

### Mitigation Strategies

| Negative Consequence | Mitigation |
|---------------------|------------|
| Increased latency | Configure max_delay, use adaptive strategies |
| Resource consumption | Implement retry budgets (Phase 3 roadmap) |
| Complexity | Provide sensible defaults, strategy selection guide |
| Testing difficulty | Provide test utilities, mock time functions |
| No retry budget | Add retry budget limiter (Phase 3 roadmap) |
| No distributed coordination | Use circuit breaker to coordinate (composability) |

---

## Implementation Details

### Python Implementation

Located at: `python/pheno-resilience/src/pheno_resilience/retry.py`

Key classes:
- `RetryConfig` — Dataclass with all configuration parameters
- `RetryStrategy` — Abstract base class for all strategies
- `ExponentialBackoffRetry` — Exponential backoff with configurable multiplier
- `LinearBackoffRetry` — Linear backoff with configurable increment
- `ConstantDelayRetry` — Fixed delay between retries
- `FibonacciBackoffRetry` — Fibonacci-based backoff
- `AdaptiveRetry` — Dynamically adjusts based on failure patterns
- `RetryManager` — Registry for managing multiple retry strategies
- `MaxRetriesExceededError` — Exception raised when all retries fail

Key functions:
- `with_retry(config, strategy_type)` — Decorator for adding retry to functions
- `retry_on_exception(exception_types, max_attempts)` — Simple retry decorator

### Rust Implementation

Located at: `rust/phenotype-retry/src/lib.rs`

Key types:
- `RetryError<E>` — Generic error enum (Exceeded, Cancelled)
- `BackoffStrategy` — Enum with Fixed, Linear, Exponential, Custom variants
- `RetryPolicy` — Configuration struct (max_attempts, backoff)
- `RetryContext` — Context passed to retry-aware operations

Key functions:
- `retry(operation, policy)` — Basic retry function
- `retry_with_context(operation, policy)` — Retry with context

### Go Implementation (Planned)

Proposed design:
- `BackoffStrategy` interface with `NextDelay(attempt int) time.Duration`
- `RetryConfig` struct with all parameters
- `Retry(ctx, config, fn)` function with context support
- Channel-based cancellation support

---

## Code Examples

### Python: Basic Retry

```python
from pheno_resilience import RetryConfig, ExponentialBackoffRetry

config = RetryConfig(
    max_attempts=5,
    base_delay=1.0,
    max_delay=60.0,
    jitter=True,
)

strategy = ExponentialBackoffRetry(config)

# Execute with retry
result = strategy.execute(
    http_client.get,
    "https://api.example.com/data"
)
```

### Python: Async Retry

```python
from pheno_resilience import RetryConfig, ExponentialBackoffRetry

config = RetryConfig(
    max_attempts=3,
    base_delay=0.5,
    max_delay=10.0,
    jitter=True,
    retryable_exceptions=(ConnectionError, TimeoutError),
)

strategy = ExponentialBackoffRetry(config)

# Execute async function with retry
result = await strategy.execute_async(
    async_http_client.get,
    "https://api.example.com/data"
)
```

### Python: Decorator Usage

```python
from pheno_resilience import RetryConfig, with_retry

config = RetryConfig(
    max_attempts=3,
    base_delay=1.0,
    jitter=True,
)

@with_retry(config, strategy_type="exponential")
async def fetch_user(user_id: str) -> dict:
    return await http_client.get(f"/users/{user_id}")

# Automatically retries on failure
user = await fetch_user("123")
```

### Python: With Callbacks

```python
from pheno_resilience import RetryConfig, ExponentialBackoffRetry

def on_retry(attempt: int, exception: Exception):
    logger.warning(f"Retry attempt {attempt}: {exception}")
    metrics.retry_attempt(exception_type=type(exception).__name__)

def on_success(result):
    metrics.retry_success()

def on_failure(exception):
    logger.error(f"All retries failed: {exception}")
    metrics.retry_failure(exception_type=type(exception).__name__)

config = RetryConfig(
    max_attempts=5,
    base_delay=1.0,
    on_retry=on_retry,
    on_success=on_success,
    on_failure=on_failure,
)

strategy = ExponentialBackoffRetry(config)
result = strategy.execute(fetch_data)
```

### Rust: Basic Retry

```rust
use phenotype_retry::{retry, RetryPolicy, BackoffStrategy};
use std::time::Duration;

let policy = RetryPolicy::new(
    5,
    BackoffStrategy::exponential(
        Duration::from_millis(100),
        Duration::from_secs(5),
    ),
);

let result = retry(
    || async {
        // Async operation that might fail
        fetch_data().await
    },
    &policy,
).await;

match result {
    Ok(value) => println!("Success: {:?}", value),
    Err(RetryError::Exceeded { attempts, last_error }) => {
        eprintln!("Failed after {} attempts: {}", attempts, last_error);
    }
    Err(RetryError::Cancelled) => {
        eprintln!("Retry was cancelled");
    }
}
```

### Rust: Retry with Context

```rust
use phenotype_retry::{retry_with_context, RetryPolicy, BackoffStrategy, RetryContext};
use std::time::Duration;

let policy = RetryPolicy::default_exponential(5);

let result = retry_with_context(
    |ctx: RetryContext| {
        async move {
            // Use context for intelligent retry behavior
            if ctx.is_last_attempt() {
                // On last attempt, use fallback endpoint
                fetch_from_fallback().await
            } else {
                fetch_primary().await
            }
        }
    },
    &policy,
).await;
```

### Rust: Custom Backoff

```rust
use phenotype_retry::{retry, RetryPolicy, BackoffStrategy};
use std::time::Duration;

// Custom backoff: 100ms, 200ms, 500ms, 1000ms, 2000ms
let policy = RetryPolicy::new(
    5,
    BackoffStrategy::custom(|attempt| {
        let delays = [100, 200, 500, 1000, 2000];
        let idx = (attempt - 1) as usize;
        Duration::from_millis(delays[idx.min(delays.len() - 1)])
    }),
);

let result = retry(|| async { operation().await }, &policy).await;
```

### Go: Proposed Usage

```go
package main

import (
    "context"
    "time"
    "github.com/phenotype/resiliencekit/go/pheno-retry"
)

func main() {
    config := pheno_retry.RetryConfig{
        MaxAttempts: 5,
        Backoff: &pheno_retry.ExponentialBackoff{
            Base:   100 * time.Millisecond,
            Max:    5 * time.Second,
            Jitter: true,
        },
        Retryable: func(err error) bool {
            // Only retry on network errors
            return isNetworkError(err)
        },
        OnRetry: func(attempt int, err error) {
            log.Printf("Retry %d: %v", attempt, err)
        },
    }

    result, err := pheno_retry.Retry(context.Background(), config, func(ctx context.Context) error {
        return fetchData(ctx)
    })
}
```

### Python: RetryManager

```python
from pheno_resilience.retry import (
    RetryManager, RetryConfig,
    ExponentialBackoffRetry, LinearBackoffRetry, AdaptiveRetry,
)

manager = RetryManager()

# Add strategies
manager.add_strategy("api_calls", ExponentialBackoffRetry(RetryConfig(
    max_attempts=5,
    base_delay=1.0,
    max_delay=30.0,
)))

manager.add_strategy("db_queries", LinearBackoffRetry(RetryConfig(
    max_attempts=3,
    base_delay=0.5,
    max_delay=5.0,
)))

manager.add_strategy("adaptive", AdaptiveRetry(RetryConfig(
    max_attempts=10,
    base_delay=0.1,
    max_delay=60.0,
)))

# Set default
manager.set_default_strategy(ExponentialBackoffRetry(RetryConfig()))

# Execute with specific strategy
result = manager.execute_with_strategy("api_calls", fetch_data)

# Execute with default
result = manager.execute(fetch_data)
```

---

## Cross-References

### Related ADRs

- **ADR-001**: [Circuit Breaker Pattern](./ADR-001-circuit-breaker.md) — Circuit breaker prevents retry storms to failing services
- **ADR-003**: [Rate Limiting Algorithm](./ADR-003-rate-limiting.md) — Rate limiting controls retry traffic volume

### Related Documentation

- **SOTA Research**: [RESILIENCE_PATTERNS_SOTA.md](../research/RESILIENCE_PATTERNS_SOTA.md) — Section 4: Retry Strategies
- **Specification**: [SPEC.md](../SPEC.md) — Section 3: Retry System

### External References

- AWS Architecture Blog: "Exponential Backoff and Jitter" — https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- tenacity Python library — https://github.com/jd/tenacity
- tokio-retry Rust library — https://github.com/srijs/rust-tokio-retry
- Polly Retry — https://github.com/App-vNext/Polly

### Implementation Files

- Python: `python/pheno-resilience/src/pheno_resilience/retry.py`
- Rust: `rust/phenotype-retry/src/lib.rs`
- Go: `go/pheno-retry/` (planned)

---

*ADR Version: 1.0*  
*Review Date: 2026-07-03*
