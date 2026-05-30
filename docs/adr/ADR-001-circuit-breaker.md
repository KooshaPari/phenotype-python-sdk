# ADR-001: Circuit Breaker Pattern Design

**Document ID:** PHENOTYPE_RESILIENCEKIT_ADR_001  
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

Circuit Breaker Pattern Design for ResilienceKit

## Status

**Accepted** — Implemented in Python, planned for Go and Rust.

---

## Context

### Problem Statement

In the Phenotype ecosystem, services communicate with each other over networks that are
inherently unreliable. When a downstream service becomes slow or unresponsive, upstream
services can accumulate pending requests, exhaust thread pools, and eventually fail
themselves — a phenomenon known as cascading failure.

Without a circuit breaker, every request to a failing service:
- Consumes resources (threads, connections, memory)
- Increases latency for all users
- Potentially amplifies the failure through retry storms
- Delays recovery by keeping the failing service under load

### Requirements

1. **Fail Fast**: When a service is known to be failing, reject requests immediately
2. **Automatic Recovery**: Detect when the service recovers and resume normal operation
3. **Configurable**: Allow tuning thresholds per service dependency
4. **Observable**: Expose state, metrics, and state change events
5. **Thread-Safe**: Support concurrent access from multiple goroutines/threads
6. **Async-Compatible**: Work with async/await patterns in all target languages

### Existing Solutions Evaluated

| Solution | Pros | Cons |
|----------|------|------|
| **pybreaker** | Mature, well-tested | Single language, limited async support |
| **Hystrix** | Battle-tested at Netflix | Deprecated, Java-only, heavy |
| **Resilience4j** | Modern, lightweight | Java-only |
| **gobreaker** | Simple Go implementation | Limited features, single language |
| **Custom implementation** | Full control, multi-language | Development cost |

### Decision Drivers

- Multi-language support (Python, Rust, Go) is a hard requirement
- Async-first design is mandatory for the Phenotype ecosystem
- Need for centralized circuit breaker management across services
- Observability and monitoring are first-class requirements

---

## Decision

We will implement a Circuit Breaker pattern with the following design:

### State Machine

The circuit breaker implements a three-state machine:

```
                    ┌─────────────────────────────────────────────┐
                    │              State Transitions               │
                    ├─────────────────────────────────────────────┤
                    │                                             │
                    │    ┌──────────┐    Recovery Timeout          │
                    │    │          │    Elapsed                   │
                    │    │  CLOSED  │──────────────────┐          │
                    │    │          │                  │          │
                    │    └────┬─────┘                  ▼          │
                    │         │                    ┌──────────┐  │
                    │         │ Failure Threshold  │          │  │
                    │         │ Exceeded           │ HALF_OPEN│  │
                    │         ▼                    │          │  │
                    │    ┌──────────┐              └────┬─────┘  │
                    │    │          │                   │        │
                    │    │   OPEN   │◄──────────────────┘        │
                    │    │          │  Failure in Half-Open      │
                    │    └──────────┘                            │
                    │         │                                  │
                    │         │ Success Threshold Met            │
                    │         ▼                                  │
                    │    ┌──────────┐                            │
                    │    │  CLOSED  │                            │
                    │    │          │                            │
                    │    └──────────┘                            │
                    │                                             │
                    └─────────────────────────────────────────────┘
```

### Configuration Parameters

```
┌─────────────────────────────────────────────────────────────────┐
│              Circuit Breaker Configuration                      │
├──────────────────────────┬──────────────┬───────────────────────┤
│  Parameter               │  Default     │  Description          │
├──────────────────────────┼──────────────┼───────────────────────┤
│  failure_threshold       │  5           │  Failures before open │
│  failure_window          │  60s         │  Window for counting  │
│  recovery_timeout        │  30s         │  Open → Half-Open     │
│  success_threshold       │  3           │  Successes to close   │
│  enable_monitoring       │  true        │  Background monitor   │
│  monitoring_interval     │  10s         │  Monitor frequency    │
│  exception_types         │  (Exception) │  Exceptions to count  │
│  ignore_exceptions       │  ()          │  Exceptions to skip   │
└──────────────────────────┴──────────────┴───────────────────────┘
```

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Circuit Breaker Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                  CircuitBreakerManager                     │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │CircuitBreaker│ │CircuitBreaker│ │CircuitBreaker│  ...  │ │
│  │  │  (Service A) │ │  (Service B) │ │  (Service C) │       │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │ │
│  │         │                │                │               │ │
│  │  ┌──────┴──────┐  ┌──────┴──────┐  ┌──────┴──────┐       │ │
│  │  │ Monitoring  │  │ Monitoring  │  │ Monitoring  │       │ │
│  │  │   Task      │  │   Task      │  │   Task      │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │              Shared Monitoring Loop                  │  │ │
│  │  │  - Aggregate stats                                   │  │ │
│  │  │  - Health reporting                                  │  │ │
│  │  │  - Graceful shutdown                                 │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Callback System

The circuit breaker supports three callback types:

1. **on_state_change**: Called when the circuit transitions between states
2. **on_failure**: Called when a call fails (before state transition check)
3. **on_success**: Called when a call succeeds

Callbacks enable integration with logging, metrics, alerting, and external systems.

---

## Consequences

### Positive Consequences

1. **Cascading Failure Prevention**: When a downstream service fails, the circuit breaker
   opens and prevents further requests, protecting both the failing service and the caller
   from resource exhaustion.

2. **Automatic Recovery**: The half-open state allows the circuit breaker to probe the
   downstream service and automatically resume normal operation when the service recovers,
   without manual intervention.

3. **Resource Efficiency**: Failed-fast requests consume minimal resources compared to
   requests that wait for timeouts, significantly improving system throughput during
   degradation periods.

4. **Observability**: Built-in statistics tracking (total calls, failures, successes,
   rejections, failure rate, success rate) provides visibility into service health
   and enables alerting on circuit state changes.

5. **Fine-Grained Control**: Per-service configuration allows tuning circuit breaker
   parameters based on each dependency's characteristics (criticality, typical latency,
   failure patterns).

6. **Exception Filtering**: The ability to specify which exception types count toward
   the failure threshold and which to ignore prevents non-transient errors (like
   validation errors) from tripping the circuit.

7. **Thread Safety**: The use of `threading.RLock` in Python ensures safe concurrent
   access, preventing race conditions in state transitions and counter updates.

8. **Composability**: Circuit breakers can be composed with other resilience patterns
   (retry, bulkhead, timeout) for layered defense against failures.

### Negative Consequences

1. **Configuration Complexity**: Each circuit breaker requires careful tuning of
   thresholds. Incorrect configuration can lead to premature circuit opening (false
   positives) or delayed opening (insufficient protection).

2. **Monitoring Overhead**: Background monitoring tasks consume resources (one async
   task per circuit breaker plus a manager-level task). With hundreds of circuit
   breakers, this overhead becomes non-trivial.

3. **State Management Complexity**: The three-state machine with sliding windows
   and multiple counters increases the cognitive load for developers understanding
   and debugging circuit breaker behavior.

4. **Testing Difficulty**: Testing circuit breaker behavior requires simulating
   failure conditions and verifying state transitions, which adds complexity to
   test suites.

5. **Recovery Delay**: The recovery timeout introduces a delay between service
   recovery and resumption of normal operation. During this window, requests are
   unnecessarily rejected.

6. **No Distributed Coordination**: The current implementation is local to each
   process. In a multi-instance deployment, each instance maintains its own circuit
   state, which can lead to inconsistent behavior across instances.

### Mitigation Strategies

| Negative Consequence | Mitigation |
|---------------------|------------|
| Configuration complexity | Provide sensible defaults, document tuning guidelines |
| Monitoring overhead | Make monitoring optional, use shared monitoring loop |
| State management complexity | Clear documentation, state transition diagrams |
| Testing difficulty | Provide test utilities, mock time functions |
| Recovery delay | Configurable recovery timeout, adaptive recovery |
| No distributed coordination | Future: Redis-backed shared state (Phase 3 roadmap) |

---

## Implementation Details

### Python Implementation

Located at: `python/pheno-resilience/src/pheno_resilience/circuit_breaker.py`

Key classes:
- `CircuitBreakerState` — Enum with CLOSED, OPEN, HALF_OPEN states
- `CircuitBreakerConfig` — Dataclass with all configuration parameters
- `CircuitBreakerError` — Base exception class
- `CircuitBreakerOpenError` — Raised when circuit is open
- `CircuitBreaker` — Main implementation with thread-safe state management
- `CircuitBreakerManager` — Registry for managing multiple circuit breakers

Thread safety approach:
- `threading.RLock` protects all state mutations
- Properties use lock for consistent reads
- State transitions are atomic within the lock

### Rust Implementation (Planned)

Proposed design:
- Use `std::sync::Arc<RwLock<>>` for thread-safe shared state
- Leverage `tokio::time` for async timeout handling
- Generic over error type `E` for type-safe error filtering
- Implement `Debug`, `Clone` for usability
- Use `thiserror` for error derivation

### Go Implementation (Planned)

Proposed design:
- Use `sync.RWMutex` for concurrency safety
- Use `context.Context` for cancellation support
- Channels for state change notifications
- `time.Ticker` for monitoring loops

---

## Code Examples

### Python: Basic Usage

```python
from pheno_resilience import CircuitBreaker, CircuitBreakerConfig

# Create circuit breaker with custom config
config = CircuitBreakerConfig(
    failure_threshold=5,
    recovery_timeout=30.0,
    success_threshold=3,
)

cb = CircuitBreaker("database", config)

# Execute through circuit breaker
try:
    result = cb.call(db.query, "SELECT * FROM users")
except CircuitBreakerOpenError:
    # Circuit is open, fail fast
    logger.warning("Database circuit breaker is open")
    return cached_result
```

### Python: Async Usage

```python
from pheno_resilience import CircuitBreaker, CircuitBreakerConfig

cb = CircuitBreaker("external_api")

# Execute async function through circuit breaker
result = await cb.call_async(
    http_client.get,
    "https://api.example.com/data"
)
```

### Python: With Callbacks

```python
def on_state_change(old_state, new_state):
    metrics.circuit_breaker_state_change(
        circuit="database",
        old=old_state.value,
        new=new_state.value,
    )

def on_failure(exception):
    logger.error(f"Circuit breaker failure: {exception}")
    alerts.notify("circuit_breaker_failure")

config = CircuitBreakerConfig(
    on_state_change=on_state_change,
    on_failure=on_failure,
)

cb = CircuitBreaker("database", config)
```

### Rust: Proposed Usage

```rust
use phenotype_circuit_breaker::{CircuitBreaker, CircuitBreakerConfig, CircuitState};

let config = CircuitBreakerConfig::builder()
    .failure_threshold(5)
    .recovery_timeout(Duration::from_secs(30))
    .success_threshold(3)
    .build();

let cb = CircuitBreaker::new("database", config);

// Execute through circuit breaker
let result = cb.execute(|| async {
    db.query("SELECT * FROM users").await
}).await;

match result {
    Ok(value) => println!("Got result: {:?}", value),
    Err(CircuitBreakerError::Open) => {
        // Circuit is open, use fallback
        use_cached_result().await
    }
    Err(CircuitBreakerError::Other(e)) => {
        // Original error
        handle_error(e).await
    }
}
```

### Go: Proposed Usage

```go
package main

import (
    "context"
    "time"
    "github.com/phenotype/resiliencekit/go/pheno-circuitbreaker"
)

func main() {
    cb := pheno_circuitbreaker.New("database", pheno_circuitbreaker.Config{
        FailureThreshold: 5,
        RecoveryTimeout:  30 * time.Second,
        SuccessThreshold: 3,
    })

    result, err := cb.Execute(context.Background(), func(ctx context.Context) (interface{}, error) {
        return db.Query(ctx, "SELECT * FROM users")
    })

    if err == pheno_circuitbreaker.ErrCircuitOpen {
        // Use fallback
        return getCachedResult()
    }
}
```

### Python: Manager Usage

```python
from pheno_resilience import CircuitBreakerManager, CircuitBreakerConfig

manager = CircuitBreakerManager()

# Create multiple circuit breakers
db_cb = manager.create_circuit("database", CircuitBreakerConfig(
    failure_threshold=3,
    recovery_timeout=60.0,
))

api_cb = manager.create_circuit("external_api", CircuitBreakerConfig(
    failure_threshold=10,
    recovery_timeout=15.0,
))

# Get all stats
stats = manager.get_all_stats()
for name, circuit_stats in stats.items():
    print(f"{name}: {circuit_stats['state']} "
          f"(failures: {circuit_stats['failure_count']}, "
          f"total: {circuit_stats['total_calls']})")

# Start monitoring
await manager.start_monitoring()
```

---

## Cross-References

### Related ADRs

- **ADR-002**: [Retry Strategy Design](./ADR-002-retry-strategy.md) — Retry works with circuit breaker for layered resilience
- **ADR-003**: [Rate Limiting Algorithm](./ADR-003-rate-limiting.md) — Rate limiting complements circuit breaker for overload protection

### Related Documentation

- **SOTA Research**: [RESILIENCE_PATTERNS_SOTA.md](../research/RESILIENCE_PATTERNS_SOTA.md) — Section 3: Circuit Breaker Pattern
- **Specification**: [SPEC.md](../SPEC.md) — Section 4: Circuit Breaker System

### External References

- Nygard, M. T. (2018). *Release It!* — Original circuit breaker pattern description
- Martin Fowler: "CircuitBreaker" — https://martinfowler.com/bliki/CircuitBreaker.html
- Resilience4j Circuit Breaker — https://resilience4j.readme.io/docs/circuitbreaker
- Polly Circuit Breaker — https://github.com/App-vNext/Polly

### Implementation Files

- Python: `python/pheno-resilience/src/pheno_resilience/circuit_breaker.py`
- Rust: `rust/phenotype-circuit-breaker/` (planned)
- Go: `go/pheno-circuitbreaker/` (planned)

---

*ADR Version: 1.0*  
*Review Date: 2026-07-03*
