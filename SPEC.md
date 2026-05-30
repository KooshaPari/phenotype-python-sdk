# ResilienceKit Comprehensive Specification

**Document ID:** PHENOTYPE_RESILIENCEKIT_SPEC  
**Status:** Active  
**Last Updated:** 2026-04-03  
**Author:** Phenotype Architecture Team  
**Version:** 2.0

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Functionality Specification](#3-functionality-specification)
4. [Technical Architecture](#4-technical-architecture)
5. [API Reference](#5-api-reference)
6. [Error Handling](#6-error-handling)
7. [Security](#7-security)
8. [Testing Strategy](#8-testing-strategy)
9. [Deployment](#9-deployment)
10. [Observability](#10-observability)
11. [Configuration](#11-configuration)
12. [Performance Requirements](#12-performance-requirements)
13. [Compatibility](#13-compatibility)
14. [Migration Guide](#14-migration-guide)
15. [Glossary](#15-glossary)

---

## 1. Project Overview

### 1.1 Purpose

ResilienceKit is a multi-language resilience toolkit for the Phenotype ecosystem. It provides
fault-tolerance patterns — including retry logic, circuit breakers, bulkheads, rate limiting,
timeouts, fallbacks, error classification, and health checking — implemented consistently
across Python, Rust, and Go.

### 1.2 Scope

ResilienceKit covers the following resilience patterns:

| Pattern | Description | Status |
|---------|-------------|--------|
| Circuit Breaker | Prevents cascading failures by detecting and isolating failing services | Implemented (Python) |
| Retry with Backoff | Automatically retries failed operations with configurable strategies | Implemented (Python, Rust) |
| Bulkhead | Isolates resources to prevent cascading failures | Implemented (Python) |
| Rate Limiting | Controls request rates to prevent overload | Partial (Rust) |
| Timeout | Prevents operations from hanging indefinitely | Implemented (Python) |
| Fallback | Provides alternative behavior when primary operations fail | Implemented (Python) |
| Error Classification | Categorizes and tracks errors for intelligent handling | Implemented (Python) |
| Health Checking | Monitors system health and component status | Implemented (Python) |
| State Machine | Hierarchical state machines for complex workflows | Implemented (Rust) |
| Async Traits | Async-first trait utilities for Rust | Implemented (Rust) |
| Port Traits | Hexagonal architecture port abstractions | Implemented (Rust) |

### 1.3 Design Principles

1. **Async-First**: All patterns support asynchronous execution natively
2. **Type Safety**: Strong typing across all implementations
3. **Composability**: Patterns can be composed for layered defense
4. **Observability**: Built-in monitoring, statistics, and health checking
5. **Multi-Language**: Consistent API surface across Go, Python, and Rust
6. **Configurable**: Fine-grained configuration for every parameter
7. **Zero Dependencies (Core)**: Core patterns have minimal external dependencies
8. **Testable**: Comprehensive test coverage with deterministic behavior

### 1.4 Project Structure

```
ResilienceKit/
├── docs/
│   ├── SPEC.md                          # This document
│   ├── adr/
│   │   ├── ADR-001-circuit-breaker.md   # Circuit Breaker ADR
│   │   ├── ADR-002-retry-strategy.md    # Retry Strategy ADR
│   │   └── ADR-003-rate-limiting.md     # Rate Limiting ADR
│   └── research/
│       └── RESILIENCE_PATTERNS_SOTA.md  # State of the Art Research
├── go/
│   ├── go.work
│   ├── pheno-retry/                     # Go retry (planned)
│   ├── pheno-circuitbreaker/            # Go circuit breaker (planned)
│   ├── pheno-bulkhead/                  # Go bulkhead (planned)
│   └── pheno-timeout/                   # Go timeout (planned)
├── python/
│   ├── pheno-resilience/                # Main Python package
│   │   ├── pyproject.toml
│   │   └── src/pheno_resilience/
│   │       ├── __init__.py
│   │       ├── circuit_breaker.py       # Circuit breaker implementation
│   │       ├── retry.py                 # Retry strategies
│   │       ├── bulkhead.py              # Bulkhead pattern
│   │       ├── timeout.py               # Timeout handling
│   │       ├── fallback.py              # Fallback mechanisms
│   │       ├── error_handling.py        # Error classification
│   │       ├── error_handler.py         # Generic error handler
│   │       └── health.py                # Health checking
│   ├── deploy-kit/                      # Deployment utilities
│   └── ci-cd-kit/                       # CI/CD workflows
└── rust/
    ├── Cargo.toml                       # Workspace definition
    ├── phenotype-retry/                 # Rust retry library
    │   └── src/lib.rs
    ├── phenotype-state-machine/         # Hierarchical state machines
    │   └── src/
    │       ├── lib.rs
    │       └── models.rs
    ├── phenotype-async-traits/          # Async trait utilities
    │   └── src/lib.rs
    └── phenotype-port-traits/           # Hexagonal port abstractions
        └── src/lib.rs
```

### 1.5 Dependencies

#### Python Dependencies

```toml
# pheno-resilience/pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"
pheno-core = { path = "../../../PhenoKit/python/pheno-core", develop = true }

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-asyncio = "^0.23"
pytest-cov = "^5.0"
black = "^24.0"
ruff = "^0.4"
mypy = "^1.9"
```

#### Rust Dependencies

```toml
# rust/Cargo.toml
[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
async-trait = "0.1"
thiserror = "1.0"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
futures = "0.3"
pin-project = "1"
rand = "0.8"
```

#### Go Dependencies (Planned)

```
go 1.22

Modules:
- pheno-retry
- pheno-circuitbreaker
- pheno-bulkhead
- pheno-timeout
```

### 1.6 Versioning

ResilienceKit follows semantic versioning (SemVer):

- **MAJOR**: Breaking API changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Current version: `0.1.0` (pre-release)

---

## 2. Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ResilienceKit Architecture                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Application Layer                              │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │  Service A  │  │  Service B  │  │  Service C  │  │  Service D  │  │  │
│  │  │  (Python)   │  │  (Rust)     │  │  (Go)       │  │  (Python)   │  │  │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │  │
│  └─────────┼────────────────┼────────────────┼────────────────┼─────────┘  │
│            │                │                │                │            │
│  ┌─────────┼────────────────┼────────────────┼────────────────┼─────────┐  │
│  │         ▼                ▼                ▼                ▼         │  │
│  │  ┌──────────────────────────────────────────────────────────────┐   │  │
│  │  │                    ResilienceKit Core                        │   │  │
│  │  │                                                              │   │  │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐  │   │  │
│  │  │  │  Circuit   │ │   Retry    │ │  Bulkhead  │ │  Rate    │  │   │  │
│  │  │  │  Breaker   │ │  Strategy  │ │  Pattern   │ │  Limiter │  │   │  │
│  │  │  └────────────┘ └────────────┘ └────────────┘ └──────────┘  │   │  │
│  │  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐  │   │  │
│  │  │  │  Timeout   │ │  Fallback  │ │   Error    │ │  Health  │  │   │  │
│  │  │  │  Handler   │ │  Mechanism │ │ Classifier │ │  Check   │  │   │  │
│  │  │  └────────────┘ └────────────┘ └────────────┘ └──────────┘  │   │  │
│  │  │  ┌────────────┐ ┌────────────┐                              │   │  │
│  │  │  │   State    │ │   Async    │                              │   │  │
│  │  │  │  Machine   │ │  Traits    │                              │   │  │
│  │  │  └────────────┘ └────────────┘                              │   │  │
│  │  └──────────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Cross-Cutting Concerns                             │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────────────────┐  │  │
│  │  │ Logging  │ │ Metrics  │ │ Tracing  │ │ Configuration Management│  │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └─────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Language-Specific Architecture

#### Python Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Python Package Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  pheno_resilience/                                              │
│  ├── __init__.py          # Public API exports                  │
│  ├── circuit_breaker.py   # CircuitBreaker, Manager, Config     │
│  ├── retry.py             # RetryStrategy, Manager, Decorators  │
│  ├── bulkhead.py          # Bulkhead, ResourcePool, Manager     │
│  ├── timeout.py           # TimeoutHandler, Config              │
│  ├── fallback.py          # FallbackHandler, Strategy           │
│  ├── error_handling.py    # ErrorCategorizer, Tracker, Analyzer │
│  ├── error_handler.py     # Generic ErrorHandler, Metrics       │
│  └── health.py            # HealthMonitor, Checker              │
│                                                                 │
│  Dependencies:                                                  │
│  ├── pheno-core (logging)                                       │
│  └── Python stdlib (asyncio, threading, dataclasses)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Rust Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Rust Workspace Architecture                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  phenotype-retry/                                               │
│  ├── RetryError<E>          # Generic error type                │
│  ├── BackoffStrategy        # Fixed, Linear, Exponential, Custom│
│  ├── RetryPolicy            # Configuration                     │
│  ├── RetryContext           # Context for retry-aware ops       │
│  ├── retry()                # Basic retry function              │
│  └── retry_with_context()   # Context-aware retry               │
│                                                                 │
│  phenotype-state-machine/                                       │
│  ├── State trait            # Core state interface              │
│  ├── Handler trait          # Event handler interface           │
│  ├── Event                  # Event type                        │
│  ├── HandlerResult          # Stay, Transition, Exit            │
│  ├── HierarchicalStateMachine  # HSM implementation             │
│  ├── StateMachine           # Simple state machine              │
│  ├── AsyncStateMachine      # Async wrapper                     │
│  └── StateHistory           # History tracking                  │
│                                                                 │
│  phenotype-async-traits/                                        │
│  ├── AsyncInit trait        # Async initialization              │
│  ├── AsyncResource trait    # Resource management               │
│  ├── TimeoutStream          # Stream timeout wrapper            │
│  ├── PrioritySemaphore      # Semaphore with priority           │
│  ├── BackgroundTask         # Task management                   │
│  ├── JitteredInterval       # Interval with jitter              │
│  ├── AsyncRateLimiter       # Rate limiting                     │
│  ├── FutureExt trait        # Future extensions                 │
│  └── StreamExt2 trait       # Stream extensions                 │
│                                                                 │
│  phenotype-port-traits/                                         │
│  ├── Repository trait       # Data access                       │
│  ├── Cache trait            # Key-value operations              │
│  ├── EventBus trait         # Pub/sub messaging                 │
│  ├── Storage trait          # File/blob operations              │
│  ├── UnitOfWork trait       # Transactional operations          │
│  ├── Entity trait           # Domain objects                    │
│  ├── AggregateRoot trait    # Event sourcing                    │
│  ├── InMemoryRepository     # In-memory implementation          │
│  ├── Pagination             # Pagination parameters             │
│  ├── Filter                 # Query filters                     │
│  └── QuerySpec              # Query specification               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Pattern Composition

Resilience patterns are designed to compose together:

```
┌─────────────────────────────────────────────────────────────────┐
│              Pattern Composition Flow                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Incoming Request                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────┐                                           │
│  │  Rate Limiter   │ ──► Reject if over limit (429)            │
│  └────────┬────────┘                                           │
│           │ Allowed                                            │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │    Bulkhead     │ ──► Reject if pool full                   │
│  └────────┬────────┘                                           │
│           │ Acquired resource                                  │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Circuit Breaker │ ──► Fail fast if open                     │
│  └────────┬────────┘                                           │
│           │ Closed or Half-Open                                │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │     Timeout     │ ──► Cancel if exceeds timeout             │
│  └────────┬────────┘                                           │
│           │ Within timeout                                     │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │     Retry       │ ──► Retry on transient failure            │
│  └────────┬────────┘                                           │
│           │ All retries exhausted                              │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │    Fallback     │ ──► Use alternative behavior              │
│  └────────┬────────┘                                           │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │    Response     │                                           │
│  └─────────────────┘                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.4 Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Error Classification Flow                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Exception Occurs                                               │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────┐                                           │
│  │ ErrorCategorizer│                                           │
│  │                 │                                           │
│  │ 1. Custom       │                                           │
│  │    categorizers │ ──► Return category if matched            │
│  └────────┬────────┘                                           │
│           │ Not matched                                        │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Exception type  │                                           │
│  │ mapping         │ ──► Return category if type matches       │
│  └────────┬────────┘                                           │
│           │ Not matched                                        │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Pattern matching│                                           │
│  │ on error message│ ──► Return category if pattern matches    │
│  └────────┬────────┘                                           │
│           │ Not matched                                        │
│           ▼                                                    │
│  ┌─────────────────┐                                           │
│  │ Return UNKNOWN  │                                           │
│  └────────┬────────┘                                           │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────┐    ┌─────────────────┐                   │
│  │ Determine       │───►│ Create ErrorInfo│                   │
│  │ Severity        │    │ with context    │                   │
│  └─────────────────┘    └────────┬────────┘                   │
│                                  │                            │
│                                  ▼                            │
│                         ┌─────────────────┐                   │
│                         │ Track in        │                   │
│                         │ ErrorTracker    │                   │
│                         └────────┬────────┘                   │
│                                  │                            │
│                                  ▼                            │
│                         ┌─────────────────┐                   │
│                         │ Call registered │                   │
│                         │ handler         │                   │
│                         └─────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Functionality Specification

### 3.1 Circuit Breaker System

#### 3.1.1 Overview

The Circuit Breaker pattern prevents cascading failures by detecting when a downstream
service is failing and temporarily blocking requests to it.

#### 3.1.2 States

```
┌─────────────────────────────────────────────────────────────────┐
│              Circuit Breaker States                             │
├──────────────┬──────────────────────────────────────────────────┤
│  State       │  Description                                     │
├──────────────┼──────────────────────────────────────────────────┤
│  CLOSED      │  Normal operation. Requests pass through.        │
│              │  Failures are counted.                           │
├──────────────┼──────────────────────────────────────────────────┤
│  OPEN        │  Circuit is tripped. All requests fail fast.     │
│              │  Recovery timer is running.                      │
├──────────────┼──────────────────────────────────────────────────┤
│  HALF_OPEN   │  Recovery timer elapsed. Probe requests allowed. │
│              │  Successes count toward closing.                 │
│              │  Any failure re-opens the circuit.               │
└──────────────┴──────────────────────────────────────────────────┘
```

#### 3.1.3 State Transitions

| From | To | Trigger | Action |
|------|-----|---------|--------|
| CLOSED | OPEN | `failure_count >= failure_threshold` within `failure_window` | Block all requests, start recovery timer |
| OPEN | HALF_OPEN | `now - last_failure_time >= recovery_timeout` | Allow probe requests |
| HALF_OPEN | CLOSED | `success_count >= success_threshold` | Resume normal operation, reset counters |
| HALF_OPEN | OPEN | Any failure during probe | Block requests, reset recovery timer |

#### 3.1.4 Configuration

```python
@dataclass(slots=True)
class CircuitBreakerConfig:
    failure_threshold: int = 5           # Failures before opening
    failure_window: float = 60.0         # Window for failure counting (seconds)
    recovery_timeout: float = 30.0       # Time before half-open (seconds)
    success_threshold: int = 3           # Successes needed to close from half-open
    enable_monitoring: bool = True       # Background monitoring
    monitoring_interval: float = 10.0    # Monitoring check interval
    exception_types: tuple = (Exception,) # Exceptions to count as failures
    ignore_exceptions: tuple = ()        # Exceptions to ignore
    on_state_change: Callable | None = None  # State change callback
    on_failure: Callable | None = None       # Failure callback
    on_success: Callable | None = None       # Success callback
```

#### 3.1.5 API

```python
class CircuitBreaker:
    def __init__(self, name: str, config: CircuitBreakerConfig | None = None)

    # Properties
    @property
    def state(self) -> CircuitBreakerState
    @property
    def failure_count(self) -> int
    @property
    def success_count(self) -> int
    @property
    def is_open(self) -> bool
    @property
    def is_closed(self) -> bool
    @property
    def is_half_open(self) -> bool

    # Execution
    def call(self, func: Callable, *args, **kwargs) -> Any
    async def call_async(self, func: Callable, *args, **kwargs) -> Any

    # Management
    def reset(self) -> None
    def get_stats(self) -> dict[str, Any]

    # Monitoring
    async def start_monitoring(self) -> None
    async def stop_monitoring(self) -> None

class CircuitBreakerManager:
    def create_circuit(self, name: str, config: CircuitBreakerConfig | None = None) -> CircuitBreaker
    def get_circuit(self, name: str) -> CircuitBreaker | None
    def remove_circuit(self, name: str) -> bool
    def list_circuits(self) -> list[str]
    def get_all_stats(self) -> dict[str, dict[str, Any]]
    async def start_monitoring(self) -> None
    async def stop_monitoring(self) -> None
```

#### 3.1.6 Exceptions

```python
class CircuitBreakerError(Exception):
    """Base exception for circuit breaker errors."""

class CircuitBreakerOpenError(CircuitBreakerError):
    """Raised when circuit breaker is open."""
    def __init__(self, circuit_name: str, state: CircuitBreakerState)
```

### 3.2 Retry System

#### 3.2.1 Overview

The Retry system automatically retries failed operations with configurable backoff
strategies and jitter to prevent thundering herd.

#### 3.2.2 Backoff Strategies

```
┌──────────────────┬──────────────────────────────────────────────┐
│  Strategy        │  Formula                                     │
├──────────────────┼──────────────────────────────────────────────┤
│  Exponential     │  delay = base * (multiplier ^ (attempt-1))   │
│  Linear          │  delay = base + (increment * (attempt-1))    │
│  Constant        │  delay = base                                │
│  Fibonacci       │  delay = base * fibonacci(attempt)           │
│  Adaptive        │  delay = base * 2^consecutive_failures       │
│  Custom (Rust)   │  user-defined function                       │
└──────────────────┴──────────────────────────────────────────────┘
```

#### 3.2.3 Jitter

All strategies support jitter (±25% by default):

```python
def apply_jitter(self, delay: float) -> float:
    jitter_factor = random.uniform(0.75, 1.25)
    return delay * jitter_factor
```

#### 3.2.4 Configuration

```python
@dataclass(slots=True)
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0          # seconds
    max_delay: float = 60.0          # seconds
    jitter: bool = True
    retryable_exceptions: tuple = (Exception,)
    non_retryable_exceptions: tuple = ()
    on_retry: Callable[[int, Exception], None] | None = None
    on_failure: Callable[[Exception], None] | None = None
    on_success: Callable[[Any], None] | None = None
    timeout: float | None = None     # seconds
```

#### 3.2.5 Rust Retry Types

```rust
pub enum RetryError<E> {
    Exceeded { attempts: u32, last_error: E },
    Cancelled,
}

pub enum BackoffStrategy {
    Fixed { delay: Duration },
    Linear { base: Duration },
    Exponential { base: Duration, max: Duration },
    Custom { func: Arc<dyn Fn(u32) -> Duration + Send + Sync> },
}

pub struct RetryPolicy {
    pub max_attempts: u32,
    pub backoff: BackoffStrategy,
}

pub struct RetryContext {
    pub attempt: u32,
    pub max_attempts: u32,
    pub elapsed: Duration,
    pub last_error: Option<String>,
}
```

#### 3.2.6 API

```python
class RetryStrategy(ABC):
    def __init__(self, config: RetryConfig)
    def calculate_delay(self, attempt: int) -> float
    def should_retry(self, attempt: int, exception: Exception) -> bool
    def apply_jitter(self, delay: float) -> float
    def execute(self, func: Callable, *args, **kwargs) -> Any
    async def execute_async(self, func: Callable, *args, **kwargs) -> Any

class ExponentialBackoffRetry(RetryStrategy):
    def __init__(self, config: RetryConfig, multiplier: float = 2.0)

class LinearBackoffRetry(RetryStrategy):
    def __init__(self, config: RetryConfig, increment: float = 1.0)

class ConstantDelayRetry(RetryStrategy):
    pass

class FibonacciBackoffRetry(RetryStrategy):
    def __init__(self, config: RetryConfig)

class AdaptiveRetry(RetryStrategy):
    def __init__(self, config: RetryConfig)

class RetryManager:
    def add_strategy(self, name: str, strategy: RetryStrategy) -> None
    def get_strategy(self, name: str) -> RetryStrategy | None
    def set_default_strategy(self, strategy: RetryStrategy) -> None
    def execute_with_strategy(self, strategy_name: str, func: Callable, *args, **kwargs) -> Any
    async def execute_async_with_strategy(self, strategy_name: str, func: Callable, *args, **kwargs) -> Any
    def execute(self, func: Callable, *args, **kwargs) -> Any
    async def execute_async(self, func: Callable, *args, **kwargs) -> Any
    def list_strategies(self) -> list[str]

# Decorators
def with_retry(config: RetryConfig, strategy_type: str = "exponential"):
    """Decorator for adding retry logic to functions."""

def retry_on_exception(exception_types: tuple = (Exception,), max_attempts: int = 3):
    """Simple retry decorator for specific exceptions."""
```

#### 3.2.7 Rust API

```rust
pub async fn retry<F, Fut, T, E>(
    operation: F,
    policy: &RetryPolicy,
) -> Result<T, RetryError<E>>
where
    F: FnMut() -> Fut,
    Fut: Future<Output = Result<T, E>>,
    E: std::error::Error + Send + Sync + 'static;

pub async fn retry_with_context<F, Fut, T, E>(
    operation: F,
    policy: &RetryPolicy,
) -> Result<T, RetryError<E>>
where
    F: FnMut(RetryContext) -> Fut,
    Fut: Future<Output = Result<T, E>>,
    E: std::error::Error + Send + Sync + 'static;
```

### 3.3 Bulkhead System

#### 3.3.1 Overview

The Bulkhead pattern isolates resources to prevent cascading failures by limiting
concurrent access to shared resources.

#### 3.3.2 Configuration

```python
@dataclass(slots=True)
class BulkheadConfig:
    max_concurrent_calls: int = 10
    max_wait_time: float = 5.0    # seconds to wait for resource
    timeout: float | None = None  # operation timeout
    enable_monitoring: bool = True
```

#### 3.3.3 API

```python
class Bulkhead:
    def __init__(self, name: str, config: BulkheadConfig | None = None)
    async def execute(self, func: Callable, *args, **kwargs) -> Any
    async def execute_async(self, func: Callable, *args, **kwargs) -> Any
    async def acquire_resource(self) -> AsyncContextManager
    def get_stats(self) -> dict[str, Any]
    async def start_monitoring(self) -> None
    async def stop_monitoring(self) -> None

class BulkheadManager:
    def create_bulkhead(self, name: str, config: BulkheadConfig | None = None) -> Bulkhead
    def get_bulkhead(self, name: str) -> Bulkhead | None
    def remove_bulkhead(self, name: str) -> bool
    def list_bulkheads(self) -> list[str]
    def get_all_stats(self) -> dict[str, dict[str, Any]]
    async def start_monitoring(self) -> None
    async def stop_monitoring(self) -> None
```

#### 3.3.4 Exceptions

```python
class BulkheadFullError(Exception):
    """Raised when bulkhead is full and cannot accept more calls."""
    def __init__(self, bulkhead_name: str, max_concurrent: int, current_calls: int)
```

### 3.4 Timeout System

#### 3.4.1 Overview

Timeout handling prevents operations from hanging indefinitely by enforcing
maximum execution times.

#### 3.4.2 Configuration

```python
@dataclass(slots=True)
class TimeoutConfig:
    default_timeout: float = 30.0
    enable_signal_timeout: bool = True
    timeout_handler: Callable[[], None] | None = None
```

#### 3.4.3 API

```python
class TimeoutHandler:
    def __init__(self, config: TimeoutConfig | None = None)
    def set_timeout(self, operation: str, timeout: float) -> None
    def get_timeout(self, operation: str) -> float
    async def execute_with_timeout(self, operation: str, func: Callable, *args, **kwargs) -> Any
    def execute_with_timeout_sync(self, operation: str, func: Callable, *args, **kwargs) -> Any
    async def timeout_context(self, operation: str, timeout: float | None = None) -> AsyncContextManager
    def timeout_context_sync(self, operation: str, timeout: float | None = None) -> ContextManager
```

#### 3.4.4 Exceptions

```python
class TimeoutError(Exception):
    """Base timeout error."""

class OperationTimeoutError(TimeoutError):
    """Raised when an operation times out."""
    def __init__(self, operation_name: str, timeout: float)
```

### 3.5 Fallback System

#### 3.5.1 Overview

Fallback mechanisms provide alternative behavior when primary operations fail,
ensuring graceful degradation.

#### 3.5.2 Configuration

```python
@dataclass(slots=True)
class FallbackConfig:
    enable_fallback: bool = True
    fallback_timeout: float | None = None
    max_fallback_attempts: int = 1
    fallback_on_exceptions: tuple = (Exception,)
```

#### 3.5.3 API

```python
class FallbackStrategy(ABC):
    @abstractmethod
    async def execute_fallback(self, original_error: Exception, context: dict[str, Any]) -> Any

class FallbackHandler:
    def __init__(self, config: FallbackConfig | None = None)
    def add_fallback(self, operation: str, strategy: FallbackStrategy) -> None
    def set_default_fallback(self, strategy: FallbackStrategy) -> None
    async def execute_with_fallback(self, operation: str, func: Callable, *args, **kwargs) -> Any
```

#### 3.5.4 Exceptions

```python
class FallbackError(Exception):
    """Raised when fallback operations fail."""
```

### 3.6 Error Classification System

#### 3.6.1 Overview

Error classification categorizes errors for intelligent retry decisions,
appropriate alerting, and meaningful metrics.

#### 3.6.2 Error Categories

```python
class ErrorCategory(Enum):
    NETWORK = "network"
    TIMEOUT = "timeout"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    CONFIGURATION = "configuration"
    RESOURCE = "resource"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"
    SERIALIZATION = "serialization"
    UNKNOWN = "unknown"
```

#### 3.6.3 Severity Levels

```python
class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

#### 3.6.4 Severity Mapping

| Category | Default Severity | Retryable |
|----------|-----------------|-----------|
| NETWORK | MEDIUM | Yes |
| TIMEOUT | MEDIUM | Yes |
| AUTHENTICATION | CRITICAL | No |
| AUTHORIZATION | CRITICAL | No |
| VALIDATION | LOW | No |
| CONFIGURATION | LOW | No |
| RESOURCE | HIGH | Yes |
| BUSINESS_LOGIC | MEDIUM | No |
| EXTERNAL_SERVICE | MEDIUM | Yes |
| DATABASE | HIGH | Yes |
| FILE_SYSTEM | MEDIUM | No |
| SERIALIZATION | MEDIUM | No |
| UNKNOWN | MEDIUM | No |

#### 3.6.5 API

```python
class ErrorCategorizer:
    def __init__(self)
    def add_pattern(self, category: ErrorCategory, pattern: str | re.Pattern) -> None
    def add_exception_mapping(self, exception_type: type[Exception], category: ErrorCategory) -> None
    def add_custom_categorizer(self, categorizer: Callable[[Exception], ErrorCategory | None]) -> None
    def categorize(self, exception: Exception) -> ErrorCategory
    def get_retryable_categories(self) -> set[ErrorCategory]
    def is_retryable(self, exception: Exception) -> bool

class ErrorHandler:
    def __init__(self, categorizer: ErrorCategorizer | None = None)
    def set_handler(self, category: ErrorCategory, handler: Callable[[ErrorInfo], Any]) -> None
    def set_default_handler(self, handler: Callable[[ErrorInfo], Any]) -> None
    def set_error_tracker(self, tracker: ErrorTracker) -> None
    def handle_error(self, exception: Exception, context: dict[str, Any] | None = None) -> Any

class ErrorTracker:
    def __init__(self, max_errors: int = 1000)
    def track_error(self, error_info: ErrorInfo) -> None
    def get_error_count(self) -> int
    def get_errors_by_category(self, category: ErrorCategory) -> list[ErrorInfo]
    def get_errors_by_severity(self, severity: ErrorSeverity) -> list[ErrorInfo]
    def get_recent_errors(self, count: int = 10) -> list[ErrorInfo]
    def get_error_rate(self, hours: int = 1) -> float
    def get_top_error_categories(self, limit: int = 5) -> list[tuple]
    def get_top_error_patterns(self, limit: int = 5) -> list[tuple]
    def get_error_distribution_by_hour(self) -> dict[int, int]
    def clear_errors(self) -> None

class ErrorAnalyzer:
    def __init__(self, error_tracker: ErrorTracker)
    def analyze_errors(self, hours: int = 24) -> ErrorMetrics
    def detect_error_spikes(self, threshold: float = 2.0) -> list[dict[str, Any]]
```

### 3.7 Health Checking System

#### 3.7.1 Overview

Health checking monitors the health of system components and provides
visibility into system state.

#### 3.7.2 Health Status Levels

```python
class HealthStatus(Enum):
    HEALTHY = "healthy"       # All dependencies responding normally
    DEGRADED = "degraded"     # Some dependencies slow or partially failing
    UNHEALTHY = "unhealthy"   # Critical dependencies failing
    UNKNOWN = "unknown"       # Health check hasn't run yet
```

#### 3.7.3 Configuration

```python
@dataclass(slots=True)
class HealthConfig:
    check_interval: float = 30.0  # seconds
    timeout: float = 5.0          # seconds
    retry_count: int = 3
    enable_monitoring: bool = True
```

#### 3.7.4 API

```python
class HealthCheck:
    name: str
    status: HealthStatus
    message: str = ""
    details: dict[str, Any] = {}
    timestamp: datetime = None
    response_time: float = 0.0

class HealthChecker(ABC):
    @abstractmethod
    async def check_health(self) -> HealthCheck

class HealthMonitor:
    def __init__(self, config: HealthConfig | None = None)
    def add_checker(self, name: str, checker: HealthChecker) -> None
    def remove_checker(self, name: str) -> bool
    async def check_all(self) -> dict[str, HealthCheck]
    async def get_overall_health(self) -> HealthStatus
    async def start_monitoring(self) -> None
    async def stop_monitoring(self) -> None
```

### 3.8 State Machine System (Rust)

#### 3.8.1 Overview

Hierarchical state machines provide a formal way to model system behavior
and transitions for complex workflows.

#### 3.8.2 Core Traits

```rust
pub trait State: Debug + Clone + Send + Sync + 'static {
    type Id: Debug + Clone + Eq + Hash + Send + Sync;
    fn state_id(&self) -> Self::Id;
    fn parent(&self) -> Option<Self::Id>;
    fn is_active(&self, current: &Self::Id) -> bool;
}

pub trait Handler<S: State>: Send + Sync {
    fn on_enter(&self, state: &S);
    fn on_exit(&self, state: &S);
    fn handle(&self, event: Event, state: &S) -> HandlerResult<S>;
}
```

#### 3.8.3 Types

```rust
pub struct Event {
    pub event_type: String,
    pub payload: Option<serde_json::Value>,
}

pub enum HandlerResult<S: State> {
    Stay,
    Transition(S),
    Exit,
}

pub struct StateMachine<S: State> {
    current: S,
    history: Vec<S>,
    transitions: Vec<(S::Id, S::Id)>,
}

pub struct AsyncStateMachine<S: State> {
    inner: StateMachine<S>,
    handler: Option<Box<dyn Handler<S>>>,
}

pub struct StateHistory<S: State> {
    entries: Vec<HistoryEntry<S>>,
    max_size: usize,
}
```

### 3.9 Async Traits (Rust)

#### 3.9.1 Overview

Async trait utilities provide reusable async trait definitions and stream
utilities for the Phenotype ecosystem.

#### 3.9.2 Traits

```rust
#[async_trait]
pub trait AsyncInit: Send + Sync {
    async fn init(&mut self) -> Result<(), Box<dyn std::error::Error + Send + Sync>>;
    async fn shutdown(&mut self) -> Result<(), Box<dyn std::error::Error + Send + Sync>>;
}

#[async_trait]
pub trait AsyncResource<T>: Send + Sync {
    async fn acquire(&self) -> Result<T, Box<dyn std::error::Error + Send + Sync>>;
    async fn release(&self, resource: T) -> Result<(), Box<dyn std::error::Error + Send + Sync>>;
}

pub trait FutureExt: Future + Sized {
    fn with_timeout(self, duration: Duration) -> tokio::time::Timeout<Self>;
}

pub trait StreamExt2: Stream + Sized
where
    Self::Item: Future,
{
    fn buffered_unordered(self, n: usize) -> futures::stream::BufferUnordered<Self>;
}
```

#### 3.9.3 Utilities

```rust
pub struct TimeoutStream<S> {
    inner: S,
    timeout: Duration,
}

pub struct PrioritySemaphore {
    permits: tokio::sync::Semaphore,
}

pub struct BackgroundTask<T> {
    handle: tokio::task::JoinHandle<T>,
    abort_handle: tokio::task::AbortHandle,
}

pub struct JitteredInterval {
    interval: tokio::time::Interval,
    jitter_ms: u64,
}

pub struct AsyncRateLimiter {
    semaphore: PrioritySemaphore,
    max_per_second: u32,
}
```

### 3.10 Port Traits (Rust)

#### 3.10.1 Overview

Port traits provide hexagonal architecture abstractions for data access,
caching, event bus, and storage operations.

#### 3.10.2 Traits

```rust
#[async_trait]
pub trait Repository<T, ID>: Send + Sync
where
    T: Send + Sync + Serialize + for<'de> Deserialize<'de>,
    ID: Send + Sync,
{
    async fn find_by_id(&self, id: ID) -> Result<Option<T>, PortError>;
    async fn find_all(&self) -> Result<Vec<T>, PortError>;
    async fn save(&self, entity: T) -> Result<T, PortError>;
    async fn delete(&self, id: ID) -> Result<(), PortError>;
}

#[async_trait]
pub trait Cache<K, V>: Send + Sync {
    async fn get(&self, key: &K) -> Result<Option<V>, PortError>;
    async fn set(&self, key: K, value: V, ttl_secs: Option<u64>) -> Result<(), PortError>;
    async fn delete(&self, key: &K) -> Result<(), PortError>;
    async fn clear(&self) -> Result<(), PortError>;
}

#[async_trait]
pub trait EventBus: Send + Sync {
    async fn publish(&self, topic: &str, payload: Vec<u8>) -> Result<(), PortError>;
    async fn subscribe(&self, topic: &str) -> Result<Box<dyn EventStream>, PortError>;
}

#[async_trait]
pub trait Storage: Send + Sync {
    async fn put(&self, key: &str, data: Vec<u8>) -> Result<(), PortError>;
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>, PortError>;
    async fn delete(&self, key: &str) -> Result<(), PortError>;
    async fn list(&self, prefix: &str) -> Result<Vec<String>, PortError>;
}

#[async_trait]
pub trait UnitOfWork: Send + Sync {
    async fn begin(&self) -> Result<(), PortError>;
    async fn commit(&self) -> Result<(), PortError>;
    async fn rollback(&self) -> Result<(), PortError>;
}
```

---

## 4. Technical Architecture

### 4.1 Threading Model

#### Python

- **Thread Safety**: `threading.RLock` for circuit breaker state
- **Async**: `asyncio` for all async operations
- **Concurrency**: `asyncio.Semaphore` for bulkhead resource pools
- **Monitoring**: Background `asyncio.Task` for each component

#### Rust

- **Thread Safety**: `Arc<RwLock<>>` for shared mutable state
- **Async**: `tokio` runtime for async operations
- **Concurrency**: `tokio::sync::Semaphore` for resource limiting
- **Tasks**: `tokio::spawn` for background tasks with `AbortHandle`

#### Go (Planned)

- **Thread Safety**: `sync.RWMutex` for shared state
- **Concurrency**: Goroutines and channels
- **Context**: `context.Context` for cancellation and timeouts

### 4.2 Memory Model

#### Python

- `@dataclass(slots=True)` for memory-efficient data classes
- `deque(maxlen=N)` for bounded error tracking
- Weak references for callback cleanup

#### Rust

- Zero-cost abstractions with no runtime overhead
- `Arc` for shared ownership
- `Box<dyn Trait>` for trait objects
- Stack allocation where possible

### 4.3 Error Propagation

```
┌─────────────────────────────────────────────────────────────────┐
│              Error Propagation Strategy                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Python:                                                        │
│  ├── Custom exception hierarchy per pattern                     │
│  ├── Exception chaining (raise ... from ...)                    │
│  └── Context preservation in ErrorInfo                          │
│                                                                 │
│  Rust:                                                          │
│  ├── Generic error types (RetryError<E>)                        │
│  ├── thiserror for derive macros                                │
│  └── Result<T, E> throughout                                    │
│                                                                 │
│  Go (Planned):                                                  │
│  ├── Sentinel errors (ErrCircuitOpen, ErrBulkheadFull)          │
│  ├── Error wrapping (fmt.Errorf("%w", err))                     │
│  └── errors.Is / errors.As for type checking                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 Configuration Management

All patterns support configuration through:

1. **Default Values**: Sensible defaults for common use cases
2. **Programmatic Configuration**: Constructor/config object
3. **Dynamic Updates**: Some parameters can be changed at runtime
4. **Validation**: Configuration validation on construction

### 4.5 Lifecycle Management

```
┌─────────────────────────────────────────────────────────────────┐
│              Component Lifecycle                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Construction                                                │
│     ├── Create with configuration                               │
│     ├── Validate configuration                                  │
│     └── Initialize internal state                               │
│                                                                 │
│  2. Operation                                                   │
│     ├── Process requests                                        │
│     ├── Update statistics                                       │
│     ├── Trigger callbacks                                       │
│     └── Monitor health (if enabled)                             │
│                                                                 │
│  3. Shutdown                                                    │
│     ├── Stop monitoring tasks                                   │
│     ├── Cancel pending operations                               │
│     ├── Flush statistics                                        │
│     └── Release resources                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. API Reference

### 5.1 Python Public API

```python
# pheno_resilience/__init__.py

# Circuit Breaker
from .circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerError,
    CircuitBreakerManager,
    CircuitBreakerState,
)

# Retry
from .retry import (
    ConstantDelayRetry,
    ExponentialBackoffRetry,
    LinearBackoffRetry,
    MaxRetriesExceededError,
    RetryConfig,
    RetryStrategy,
    retry_on_exception,
    with_retry,
)

# Error Handling
from .error_handler import (
    ErrorCategory,
    ErrorContext,
    ErrorHandler,
    ErrorInfo,
    ErrorMetrics,
    ErrorSeverity,
)
```

### 5.2 Rust Public API

```rust
// phenotype-retry
pub use {
    RetryError,
    BackoffStrategy,
    RetryPolicy,
    RetryContext,
    retry,
    retry_with_context,
};

// phenotype-state-machine
pub use {
    State,
    Handler,
    Event,
    HandlerResult,
    HierarchicalStateMachine,
    StateMachine,
    AsyncStateMachine,
    StateHistory,
    HistoryEntry,
};

// phenotype-async-traits
pub use {
    AsyncInit,
    AsyncResource,
    TimeoutStream,
    PrioritySemaphore,
    BackgroundTask,
    JitteredInterval,
    AsyncRateLimiter,
    FutureExt,
    StreamExt2,
};

// phenotype-port-traits
pub use {
    Repository,
    Cache,
    EventBus,
    EventStream,
    Storage,
    PortError,
    Pagination,
    SortDirection,
    Filter,
    FilterOperator,
    QuerySpec,
    UnitOfWork,
    Entity,
    AggregateRoot,
    InMemoryRepository,
};
```

### 5.3 Go Public API (Planned)

```go
// pheno-retry
package pheno_retry

type BackoffStrategy interface {
    NextDelay(attempt int) time.Duration
}

type RetryConfig struct {
    MaxAttempts   int
    Backoff       BackoffStrategy
    Retryable     func(error) bool
    OnRetry       func(attempt int, err error)
}

func Retry(ctx context.Context, config RetryConfig, fn func(ctx context.Context) error) error

// pheno-circuitbreaker
package pheno_circuitbreaker

type CircuitState int

const (
    StateClosed CircuitState = iota
    StateOpen
    StateHalfOpen
)

type CircuitBreaker struct { ... }
func New(name string, config Config) *CircuitBreaker
func (cb *CircuitBreaker) Execute(ctx context.Context, fn func(ctx context.Context) (interface{}, error)) (interface{}, error)
```

---

## 6. Error Handling

### 6.1 Error Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│              Python Exception Hierarchy                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Exception                                                      │
│  ├── CircuitBreakerError                                        │
│  │   └── CircuitBreakerOpenError                               │
│  ├── RetryError                                                 │
│  │   └── MaxRetriesExceededError                               │
│  ├── BulkheadFullError                                         │
│  ├── TimeoutError                                               │
│  │   └── OperationTimeoutError                                 │
│  └── FallbackError                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Error Context

Every error in ResilienceKit includes context information:

```python
@dataclass(slots=True)
class ErrorInfo:
    error_id: str                    # Unique identifier
    exception: Exception             # Original exception
    category: ErrorCategory          # Categorized type
    severity: ErrorSeverity          # Severity level
    timestamp: datetime              # When it occurred
    context: dict[str, Any]          # Operation context
    stack_trace: str                 # Full stack trace
    retryable: bool                  # Whether to retry
    tags: set[str]                   # Classification tags
    metadata: dict[str, Any]         # Additional metadata
```

### 6.3 Error Recovery Strategies

| Error Type | Recovery Strategy |
|------------|------------------|
| Transient network error | Retry with exponential backoff |
| Service temporarily unavailable | Circuit breaker + retry |
| Resource exhaustion | Bulkhead + timeout |
| Rate limit exceeded | Retry after Retry-After header |
| Permanent failure | Fallback to alternative |
| Configuration error | Fail fast, alert immediately |

### 6.4 Error Reporting

Errors are reported through multiple channels:

1. **Logging**: Structured logging with error context
2. **Metrics**: Error counts by category, severity, pattern
3. **Callbacks**: Custom error handlers per category
4. **Tracking**: ErrorTracker for historical analysis
5. **Alerting**: Integration with external alerting systems

---

## 7. Security

### 7.1 Thread Safety

All shared state is protected:

- **Python**: `threading.RLock` for reentrant locking
- **Rust**: `Arc<RwLock<>>` for read-write locking
- **Go (Planned)**: `sync.RWMutex` for read-write locking

### 7.2 Resource Limits

All patterns enforce resource limits to prevent exhaustion:

- **Circuit Breaker**: Limits failed request propagation
- **Bulkhead**: Limits concurrent resource usage
- **Rate Limiter**: Limits request throughput
- **Timeout**: Limits operation duration
- **Retry**: Limits retry attempts with max_delay cap

### 7.3 Input Validation

- Configuration validation on construction
- Type checking for all parameters
- Bounds checking for numeric values
- Sanitization of error messages (no sensitive data leakage)

### 7.4 Denial of Service Protection

- Rate limiting prevents abuse
- Bulkhead isolation prevents resource monopolization
- Circuit breaker prevents cascading failures
- Timeout prevents resource hoarding

### 7.5 Audit Trail

- All state changes are logged
- Error tracking provides historical analysis
- Statistics expose operational metrics
- Monitoring tasks provide continuous visibility

---

## 8. Testing Strategy

### 8.1 Unit Testing

Each pattern is tested in isolation:

```
┌─────────────────────────────────────────────────────────────────┐
│              Unit Test Coverage                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Circuit Breaker:                                               │
│  ├── State transitions (CLOSED → OPEN → HALF_OPEN → CLOSED)    │
│  ├── Failure threshold triggering                              │
│  ├── Recovery timeout behavior                                 │
│  ├── Success threshold in half-open                            │
│  ├── Exception filtering                                       │
│  ├── Callback invocation                                       │
│  └── Statistics accuracy                                       │
│                                                                 │
│  Retry:                                                         │
│  ├── All backoff strategies                                    │
│  ├── Jitter application                                        │
│  ├── Max attempts enforcement                                  │
│  ├── Exception filtering                                       │
│  ├── Callback invocation                                       │
│  ├── Context awareness                                         │
│  └── Timeout handling                                          │
│                                                                 │
│  Bulkhead:                                                      │
│  ├── Concurrency limiting                                      │
│  ├── Resource acquisition/release                              │
│  ├── Timeout on acquisition                                    │
│  ├── Statistics accuracy                                       │
│  └── Monitoring behavior                                       │
│                                                                 │
│  Error Classification:                                          │
│  ├── Pattern matching                                          │
│  ├── Exception type mapping                                    │
│  ├── Custom categorizers                                       │
│  ├── Severity determination                                    │
│  ├── Retryable detection                                       │
│  └── Error tracking                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Integration Testing

- Pattern composition (retry + circuit breaker)
- Concurrent access patterns
- Async/sync interoperability
- Cross-language API consistency

### 8.3 Chaos Testing

- Inject network failures
- Simulate service degradation
- Test circuit breaker opening/closing
- Verify retry doesn't amplify failures
- Test bulkhead under load

### 8.4 Performance Testing

- Measure overhead of each pattern
- Test under high concurrency
- Verify memory usage stays bounded
- Benchmark different backoff strategies

### 8.5 Test Configuration

```toml
# Python
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short"

[tool.coverage.run]
source = ["src/pheno_resilience"]
branch = true

[tool.coverage.report]
fail_under = 80
```

---

## 9. Deployment

### 9.1 Python Package

```bash
# Build
cd python/pheno-resilience
poetry build

# Install
pip install dist/pheno_resilience-*.whl

# Development
poetry install --with dev
```

### 9.2 Rust Crates

```bash
# Build
cd rust
cargo build --release

# Test
cargo test

# Publish
cargo publish -p phenotype-retry
cargo publish -p phenotype-state-machine
cargo publish -p phenotype-async-traits
cargo publish -p phenotype-port-traits
```

### 9.3 Go Modules (Planned)

```bash
# Build
cd go
go build ./...

# Test
go test ./...

# Tidy
go mod tidy
```

### 9.4 CI/CD Pipeline

```yaml
# python/ci-cd-kit/workflows/coverage_python.yml
name: Python Coverage
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install uv
      - run: uv sync --dev
      - run: uv run pytest --cov=pheno_resilience
      - run: uv run ruff check src/
      - run: uv run mypy src/
```

---

## 10. Observability

### 10.1 Metrics

Each pattern exposes metrics:

| Pattern | Metrics |
|---------|---------|
| Circuit Breaker | State, failure count, success count, total calls, rejections, failure rate |
| Retry | Attempts, successes, failures, total delay, strategy used |
| Bulkhead | Active calls, available calls, utilization, rejections |
| Rate Limiter | Allowed, rejected, current tokens, refill rate |
| Timeout | Timeouts, average duration, p99 duration |
| Error Classification | Errors by category, severity, pattern, hourly distribution |
| Health Check | Component status, response time, overall health |

### 10.2 Logging

All patterns use structured logging:

```python
logger = get_logger("pheno.resilience.circuit_breaker")
logger.info(f"Circuit breaker '{self.name}' transitioned to OPEN")
logger.debug(f"Circuit breaker '{self.name}' recorded failure (count: {self._failure_count})")
logger.warning(f"Circuit breaker '{self.name}' ignoring exception: {type(exception).__name__}")
```

### 10.3 Health Endpoints

Health monitors can be exposed via HTTP:

```json
{
  "status": "healthy",
  "checks": {
    "database": {
      "status": "healthy",
      "response_time": 0.012,
      "timestamp": "2026-04-03T10:00:00Z"
    },
    "external_api": {
      "status": "degraded",
      "response_time": 2.5,
      "message": "High latency detected",
      "timestamp": "2026-04-03T10:00:00Z"
    }
  }
}
```

---

## 11. Configuration

### 11.1 Default Configuration

```python
# Sensible defaults for production use
DEFAULTS = {
    "circuit_breaker": {
        "failure_threshold": 5,
        "failure_window": 60.0,
        "recovery_timeout": 30.0,
        "success_threshold": 3,
    },
    "retry": {
        "max_attempts": 3,
        "base_delay": 1.0,
        "max_delay": 60.0,
        "jitter": True,
    },
    "bulkhead": {
        "max_concurrent_calls": 10,
        "max_wait_time": 5.0,
    },
    "timeout": {
        "default_timeout": 30.0,
    },
    "health": {
        "check_interval": 30.0,
        "timeout": 5.0,
    },
}
```

### 11.2 Environment-Based Configuration

```python
import os

def get_config():
    return {
        "circuit_breaker": {
            "failure_threshold": int(os.getenv("CB_FAILURE_THRESHOLD", 5)),
            "recovery_timeout": float(os.getenv("CB_RECOVERY_TIMEOUT", 30.0)),
        },
        "retry": {
            "max_attempts": int(os.getenv("RETRY_MAX_ATTEMPTS", 3)),
            "base_delay": float(os.getenv("RETRY_BASE_DELAY", 1.0)),
        },
    }
```

### 11.3 Dynamic Configuration

Some parameters can be changed at runtime:

- Circuit breaker: `reset()` to manually reset state
- Timeout: `set_timeout()` to change per-operation timeout
- Rate limiter: Adjust token count and refill rate
- Health check: Add/remove checkers dynamically

---

## 12. Performance Requirements

### 12.1 Overhead Targets

| Pattern | Target Overhead | Notes |
|---------|----------------|-------|
| Circuit Breaker state check | < 1μs | Must be negligible |
| Retry delay calculation | < 100ns | Simple math operation |
| Bulkhead acquire | < 10μs | Semaphore operation |
| Rate limiter check | < 1μs | Token bucket math |
| Error categorization | < 100μs | Pattern matching |
| Health check | < 5ms | Per-component check |

### 12.2 Memory Targets

| Component | Target | Notes |
|-----------|--------|-------|
| Circuit Breaker instance | < 1KB | Important for thousands of breakers |
| Retry context | < 256 bytes | Stack-allocated where possible |
| Error tracker (1000 errors) | < 1MB | Bounded deque |
| Bulkhead instance | < 512 bytes | Semaphore + counters |

### 12.3 Concurrency Targets

| Component | Target | Notes |
|-----------|--------|-------|
| Circuit Breaker | Thread-safe | RLock-protected |
| Retry | Thread-safe | No shared state |
| Bulkhead | Concurrent | Semaphore-based |
| Rate Limiter | Thread-safe | Mutex-protected |

---

## 13. Compatibility

### 13.1 Language Versions

| Language | Minimum Version | Target Version |
|----------|----------------|----------------|
| Python | 3.11 | 3.14 |
| Rust | 1.75 | Latest stable |
| Go | 1.22 | 1.24+ |

### 13.2 Runtime Compatibility

| Runtime | Support | Notes |
|---------|---------|-------|
| Python asyncio | Full | Native support |
| Rust tokio | Full | Primary async runtime |
| Rust async-std | Partial | Via compatibility layer |
| Go goroutines | Full (planned) | Native support |

### 13.3 Platform Compatibility

| Platform | Support |
|----------|---------|
| Linux | Full |
| macOS | Full |
| Windows | Full |
| Docker | Full |
| Kubernetes | Full |

---

## 14. Migration Guide

### 14.1 From Manual Error Handling

**Before:**
```python
try:
    result = api.call()
except Exception:
    result = None
```

**After:**
```python
from pheno_resilience import CircuitBreaker, RetryConfig, with_retry

cb = CircuitBreaker("api")

@with_retry(RetryConfig(max_attempts=3))
def call_api():
    return cb.call(api.call)

result = call_api()
```

### 14.2 From Simple Retry to ResilienceKit

**Before:**
```python
for i in range(3):
    try:
        return api.call()
    except Exception:
        time.sleep(1)
raise Exception("Failed")
```

**After:**
```python
from pheno_resilience import RetryConfig, ExponentialBackoffRetry

config = RetryConfig(
    max_attempts=3,
    base_delay=1.0,
    jitter=True,
)
strategy = ExponentialBackoffRetry(config)
result = strategy.execute(api.call)
```

### 14.3 Rust Migration

**Before:**
```rust
for attempt in 1..=3 {
    match operation().await {
        Ok(v) => return Ok(v),
        Err(e) => {
            if attempt == 3 { return Err(e); }
            tokio::time::sleep(Duration::from_secs(1)).await;
        }
    }
}
```

**After:**
```rust
use phenotype_retry::{retry, RetryPolicy, BackoffStrategy};

let policy = RetryPolicy::default_exponential(3);
let result = retry(|| async { operation().await }, &policy).await;
```

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **Circuit Breaker** | Pattern that detects failures and prevents further requests to failing services |
| **Retry** | Pattern that automatically re-attempts failed operations |
| **Backoff** | Strategy for increasing delay between retry attempts |
| **Jitter** | Random variation added to retry delays to prevent thundering herd |
| **Thundering Herd** | Problem where many clients retry simultaneously, overwhelming a recovering service |
| **Bulkhead** | Pattern that isolates resources to prevent cascading failures |
| **Rate Limiter** | Component that controls the rate of requests to prevent overload |
| **Token Bucket** | Rate limiting algorithm that allows bursts up to bucket capacity |
| **Timeout** | Maximum allowed duration for an operation |
| **Fallback** | Alternative behavior when primary operation fails |
| **Error Classification** | Process of categorizing errors for intelligent handling |
| **Health Check** | Mechanism for monitoring component health |
| **State Machine** | Formal model for system behavior and transitions |
| **Async-First** | Design principle prioritizing asynchronous execution |
| **Composability** | Ability to combine patterns for layered defense |
| **Observability** | Ability to understand system state through metrics, logs, and traces |
| **Retry Budget** | Limit on total retry traffic as percentage of original traffic |
| **Half-Open** | Circuit breaker state that allows probe requests to test recovery |
| **Recovery Timeout** | Duration a circuit breaker stays open before transitioning to half-open |
| **Failure Threshold** | Number of failures required to trip a circuit breaker |
| **Success Threshold** | Number of successes required to close a circuit breaker from half-open |
| **Sliding Window** | Rate limiting technique that uses a moving time window |
| **Leaky Bucket** | Rate limiting algorithm that processes requests at a constant rate |
| **Fixed Window** | Rate limiting technique that counts requests per fixed time period |
| **Semaphore** | Synchronization primitive that limits concurrent access |
| **Resource Pool** | Collection of reusable resources with concurrency limits |
| **Adaptive Retry** | Retry strategy that adjusts based on failure patterns |
| **Fibonacci Backoff** | Retry strategy using Fibonacci sequence for delays |
| **Decorrelated Jitter** | Jitter algorithm that randomizes between base and 3x previous delay |
| **Error Spike** | Sudden increase in error rate above normal baseline |
| **Degraded Mode** | Operating state where some functionality is reduced but system remains available |
| **Graceful Degradation** | Design principle where system reduces functionality rather than failing completely |
| **Cascading Failure** | Failure that propagates from one component to dependent components |
| **Fail Fast** | Pattern that immediately rejects requests when system is known to be failing |
| **Probe Request** | Test request sent during half-open state to check service recovery |
| **Retryable Error** | Error that may resolve itself if the operation is retried |
| **Non-Retryable Error** | Error that will not resolve itself and should not be retried |
| **Error Budget** | Maximum acceptable error rate before triggering alerts or circuit breakers |
| **Service Level Objective (SLO)** | Target reliability level for a service |
| **Error Rate** | Percentage of requests that result in errors |
| **P99 Latency** | 99th percentile response time |
| **Mean Time to Recovery (MTTR)** | Average time to recover from a failure |
| **Mean Time Between Failures (MTBF)** | Average time between system failures |

---

## 16. Appendix: Complete Usage Examples

### 16.1 Full Python Example: Resilient API Client

```python
from pheno_resilience import (
    CircuitBreaker, CircuitBreakerConfig,
    RetryConfig, ExponentialBackoffRetry, with_retry,
    Bulkhead, BulkheadConfig,
    ErrorCategory, ErrorHandler,
)

class ResilientAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

        # Circuit breaker for the API
        self.cb = CircuitBreaker("api", CircuitBreakerConfig(
            failure_threshold=5,
            recovery_timeout=30.0,
            success_threshold=3,
        ))

        # Retry strategy
        retry_config = RetryConfig(
            max_attempts=3,
            base_delay=1.0,
            max_delay=30.0,
            jitter=True,
            retryable_exceptions=(ConnectionError, TimeoutError),
        )
        self.retry_strategy = ExponentialBackoffRetry(retry_config)

        # Bulkhead for connection isolation
        self.bulkhead = Bulkhead("api_connections", BulkheadConfig(
            max_concurrent_calls=20,
            max_wait_time=5.0,
        ))

        # Error handler
        self.error_handler = ErrorHandler()

    async def get(self, path: str) -> dict:
        """Make a resilient GET request."""
        async def _request():
            return await self.bulkhead.execute_async(
                lambda: self.cb.call_async(
                    self._http_get, f"{self.base_url}{path}"
                )
            )

        try:
            return await self.retry_strategy.execute_async(_request)
        except Exception as e:
            return self.error_handler.handle_error(e, {"path": path})

    async def _http_get(self, url: str) -> dict:
        """Actual HTTP request."""
        # Implementation depends on HTTP client
        pass
```

### 16.2 Full Rust Example: Resilient Database Client

```rust
use phenotype_retry::{retry, RetryPolicy, BackoffStrategy};
use std::time::Duration;

struct ResilientDbClient {
    pool: ConnectionPool,
    retry_policy: RetryPolicy,
}

impl ResilientDbClient {
    fn new(pool: ConnectionPool) -> Self {
        Self {
            pool,
            retry_policy: RetryPolicy::new(
                3,
                BackoffStrategy::exponential(
                    Duration::from_millis(100),
                    Duration::from_secs(5),
                ),
            ),
        }
    }

    async fn query(&self, sql: &str) -> Result<Vec<Row>, Box<dyn std::error::Error>> {
        let sql = sql.to_string();
        let pool = self.pool.clone();

        retry(
            || {
                let sql = sql.clone();
                let pool = pool.clone();
                async move {
                    let conn = pool.get().await?;
                    conn.query(&sql).await
                }
            },
            &self.retry_policy,
        )
        .await
        .map_err(|e| Box::new(e) as Box<dyn std::error::Error>)
    }
}
```

### 16.3 Pattern Composition Examples

```
┌─────────────────────────────────────────────────────────────────┐
│              Common Pattern Compositions                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. API Gateway:                                                │
│     Rate Limiter → Bulkhead → Circuit Breaker → Retry           │
│                                                                 │
│  2. Database Client:                                            │
│     Circuit Breaker → Retry → Timeout                           │
│                                                                 │
│  3. Message Queue Consumer:                                     │
│     Bulkhead → Retry → Fallback → Error Handler                 │
│                                                                 │
│  4. Health Check Endpoint:                                      │
│     Timeout → Health Monitor → Error Handler                    │
│                                                                 │
│  5. Background Job Processor:                                   │
│     Retry → Bulkhead → Circuit Breaker → Fallback               │
│                                                                 │
│  6. Real-time Data Pipeline:                                    │
│     Rate Limiter → Timeout → Retry → Error Handler              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

*Specification Version: 2.0*  
*Next Review: 2026-07-03*  
*Contributors: Phenotype Architecture Team*
