# ADR-003: Rate Limiting Algorithm

**Document ID:** PHENOTYPE_RESILIENCEKIT_ADR_003  
**Status:** Proposed  
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

Rate Limiting Algorithm Selection for ResilienceKit

## Status

**Proposed** — Under review. Implementation planned for all three languages.

---

## Context

### Problem Statement

Rate limiting is essential for protecting services from overload, ensuring fair resource
allocation, and preventing abuse. Without rate limiting:

- A single client can monopolize all available resources
- Traffic spikes can overwhelm services, causing cascading failures
- Abuse (intentional or accidental) can degrade service quality for all users
- No mechanism exists to gracefully shed load during peak demand

Rate limiting differs from circuit breaking in that it is **proactive** (prevents overload
before it happens) rather than **reactive** (responds to failures after they occur).

### Requirements

1. **Multiple Algorithms**: Support different rate limiting algorithms for different use cases
2. **Distributed Support**: Coordinate rate limits across multiple service instances
3. **Async-Native**: Non-blocking rate limit checks that work with async/await
4. **Configurable**: Per-endpoint, per-client, and global rate limits
5. **Observable**: Expose metrics on allowed/rejected requests, current rates
6. **Graceful Degradation**: Provide meaningful error responses when rate limited
7. **Composable**: Work with circuit breakers, retries, and bulkheads

### Rate Limiting Algorithms Evaluated

| Algorithm | Description | Burst Support | Precision | Memory |
|-----------|-------------|---------------|-----------|--------|
| **Fixed Window** | Count requests per fixed time window | No (burst at boundaries) | Low | O(1) |
| **Sliding Window Log** | Store timestamp of each request | Yes | High | O(N) |
| **Sliding Window Counter** | Approximate sliding window with weighted counters | Partial | Medium | O(1) |
| **Token Bucket** | Tokens added at fixed rate, consumed per request | Yes | High | O(1) |
| **Leaky Bucket** | Requests processed at fixed rate, queue excess | No | High | O(N) |

### Algorithm Deep Dive

```
┌─────────────────────────────────────────────────────────────────┐
│              Fixed Window Counter                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Window: [00:00 - 00:01]  [00:01 - 00:02]  [00:02 - 00:03]   │
│  Limit:  100 requests per minute                               │
│                                                                 │
│  00:00:59 ──► 100 requests (all within limit)                 │
│  00:01:00 ──► Counter resets to 0                              │
│  00:01:01 ──► 100 requests (all within limit)                 │
│                                                                 │
│  Problem: 200 requests in 2 seconds (00:00:59-00:01:01)       │
│  This is 2x the intended rate!                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              Token Bucket                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Bucket Capacity: 100 tokens                                    │
│  Refill Rate: 10 tokens/second                                  │
│                                                                 │
│  ┌─────────────────────────────┐                               │
│  │  ┌───┬───┬───┬───┬───┐     │                               │
│  │  │ ● │ ● │ ● │ ● │ ● │ ... │  ← 100 tokens                 │
│  │  └───┴───┴───┴───┴───┘     │                               │
│  │         ▲                   │                               │
│  │         │ +10/sec           │                               │
│  └─────────┼───────────────────┘                               │
│            │                                                   │
│  Request ──┤──► Take 1 token                                    │
│            │    Available? Yes → Process                       │
│            │    Available? No → Reject/Wait                    │
│                                                                 │
│  Advantages:                                                    │
│  - Allows bursts up to bucket capacity                         │
│  - Smooth long-term rate (refill rate)                         │
│  - Simple O(1) implementation                                  │
│  - No per-request storage                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              Sliding Window Log                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Window: 60 seconds                                             │
│  Limit: 100 requests                                            │
│                                                                 │
│  Log: [t=1, t=5, t=10, t=15, ..., t=55]                       │
│       ↑                                    ↑                    │
│       Oldest (will be pruned)             Newest                │
│                                                                 │
│  On request:                                                   │
│  1. Remove entries older than (now - 60s)                      │
│  2. Count remaining entries                                    │
│  3. If count < limit, allow and add timestamp                  │
│  4. If count >= limit, reject                                  │
│                                                                 │
│  Advantages:                                                    │
│  - Precise rate limiting                                       │
│  - No boundary burst problem                                   │
│  - Accurate at any point in time                               │
│                                                                 │
│  Disadvantages:                                                 │
│  - O(N) memory (stores all timestamps)                        │
│  - O(N) computation per request (pruning)                      │
│  - Not suitable for high-throughput systems                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              Leaky Bucket                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Bucket Capacity: 100 requests                                  │
│  Leak Rate: 10 requests/second                                  │
│                                                                 │
│  ┌─────────────────────────────┐                               │
│  │  ┌─────────────────────┐    │                               │
│  │  │  ~~~ Water Level ~~~ │    │                               │
│  │  │  ~~~ (requests)  ~~~ │    │                               │
│  │  │                     │    │                               │
│  │  └──────────┬──────────┘    │                               │
│  │             │ Drip          │                               │
│  │             │ 10/sec        │                               │
│  └─────────────┼───────────────┘                               │
│                ▼                                               │
│           Processed                                            │
│                                                                 │
│  Incoming requests fill the bucket.                            │
│  Requests are processed at a constant rate (leak).             │
│  If bucket is full, new requests are rejected.                 │
│                                                                 │
│  Advantages:                                                    │
│  - Smooth, constant output rate                                │
│  - Good for traffic shaping                                    │
│                                                                 │
│  Disadvantages:                                                 │
│  - No burst allowance                                          │
│  - Queue management complexity                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Decision Drivers

- Token Bucket is the industry standard for API rate limiting
- Sliding Window Log provides the most accurate limiting
- Need for both local and distributed rate limiting
- Async-native implementation is mandatory

---

## Decision

We will implement **Token Bucket** as the primary rate limiting algorithm, with
**Sliding Window Counter** as a secondary option for scenarios requiring higher accuracy.

### Rationale

Token Bucket is selected as the primary algorithm because:

1. **Burst Support**: Allows short bursts (up to bucket capacity) while maintaining
   a smooth long-term rate, which matches real-world API usage patterns.

2. **Efficiency**: O(1) time and space complexity — requires only two values
   (current tokens, last refill time) regardless of request volume.

3. **Simplicity**: Easy to implement, understand, and debug. The algorithm is
   well-understood and has been battle-tested in production systems.

4. **Flexibility**: Can be configured for strict limiting (capacity = refill rate)
   or burst-friendly limiting (capacity >> refill rate).

5. **Distributed-Friendly**: The token count and refill time can be stored in a
   shared data store (Redis) for distributed rate limiting.

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│              Rate Limiter Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                  RateLimiterManager                        │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │ TokenBucket │  │ TokenBucket │  │ TokenBucket │  ...  │ │
│  │  │ (Global)    │  │ (Per-Client)│  │ (Per-Endpoint)│      │ │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │ │
│  │         │                │                │               │ │
│  │         └────────────────┼────────────────┘               │ │
│  │                          ▼                                │ │
│  │              ┌─────────────────────────┐                 │ │
│  │              │   RateLimiterConfig     │                 │ │
│  │              │  - max_tokens           │                 │ │
│  │              │  - refill_rate          │                 │ │
│  │              │  - refill_interval      │                 │ │
│  │              │  - strategy             │                 │ │
│  │              └─────────────────────────┘                 │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  Request Flow:                                                 │
│  ┌─────────┐    ┌──────────────┐    ┌──────────┐              │
│  │ Request │───►│ Check Rate   │───►│ Allowed? │              │
│  │         │    │ Limiter      │    └────┬─────┘              │
│  └─────────┘    └──────────────┘     Yes │ No                 │
│                                         ▼   ▼                  │
│                                   ┌──────┐ ┌──────────────┐   │
│                                   │Process│ │ Reject with  │   │
│                                   │       │ │ 429 + Retry- │   │
│                                   └───────┘ │ After header │   │
│                                             └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Configuration Parameters

```
┌─────────────────────────────────────────────────────────────────┐
│              Rate Limiter Configuration                         │
├──────────────────────────┬──────────────┬───────────────────────┤
│  Parameter               │  Default     │  Description          │
├──────────────────────────┼──────────────┼───────────────────────┤
│  max_tokens              │  100         │  Bucket capacity      │
│  refill_rate             │  10/sec      │  Tokens per second    │
│  refill_interval         │  100ms       │  Refill check freq    │
│  strategy                │  token_bucket│  Algorithm to use     │
│  key_function            │  client_ip   │  How to identify src  │
│  response_headers        │  true        │  Add rate limit hdrs  │
│  enable_monitoring       │  true        │  Background monitor   │
└──────────────────────────┴──────────────┴───────────────────────┘
```

### Response Headers

When rate limiting is active, responses include standard headers:

```
X-RateLimit-Limit: 100          # Maximum requests per window
X-RateLimit-Remaining: 42       # Requests remaining in current window
X-RateLimit-Reset: 1712160000   # Unix timestamp when the limit resets
Retry-After: 30                 # Seconds to wait before retrying (when limited)
```

---

## Consequences

### Positive Consequences

1. **Overload Protection**: Rate limiting prevents any single client or endpoint from
   consuming all available resources, ensuring fair access and preventing service
   degradation under heavy load.

2. **Burst Handling**: The Token Bucket algorithm allows short bursts of traffic
   (up to bucket capacity) while maintaining a smooth long-term average rate,
   which matches real-world usage patterns where traffic is naturally bursty.

3. **Resource Efficiency**: O(1) time and space complexity means rate limiting adds
   negligible overhead to request processing, even at high throughput.

4. **Graceful Degradation**: Rate-limited requests receive clear error responses
   (HTTP 429) with `Retry-After` headers, enabling clients to back off appropriately
   rather than failing with ambiguous errors.

5. **Multi-Level Limiting**: Support for global, per-client, and per-endpoint rate
   limits enables fine-grained traffic control — for example, limiting a specific
   API endpoint more strictly than others, or limiting abusive clients while allowing
   normal clients full access.

6. **Observability**: Built-in metrics (allowed/rejected counts, current token levels,
   refill rates) provide visibility into traffic patterns and enable alerting on
   unusual activity.

7. **Composability**: Rate limiting works naturally with other resilience patterns —
   requests that pass the rate limiter can then go through bulkhead isolation,
   circuit breaker checks, and retry logic.

### Negative Consequences

1. **False Rejections**: Legitimate traffic may be rejected during burst periods,
   especially if the bucket capacity is set too low. This can impact user experience
   during traffic spikes.

2. **Configuration Complexity**: Tuning rate limits requires understanding of traffic
   patterns. Incorrect configuration can either allow too much traffic (insufficient
   protection) or reject too much (poor user experience).

3. **Distributed State**: For distributed rate limiting, a shared state store (Redis,
   etcd) is required, adding infrastructure complexity and a potential single point
   of failure.

4. **Clock Drift**: Token refill calculations depend on accurate time. Clock drift
   between nodes in a distributed system can cause inconsistent rate limiting behavior.

5. **No Priority Support**: The current design does not support priority-based rate
   limiting (e.g., allowing premium clients higher limits). This would require
   additional complexity.

6. **Memory for Sliding Window**: If Sliding Window Log is used as a secondary
   algorithm, it requires O(N) memory to store timestamps, which can be significant
   for high-throughput endpoints.

### Mitigation Strategies

| Negative Consequence | Mitigation |
|---------------------|------------|
| False rejections | Tune bucket capacity based on p99 traffic, monitor rejection rate |
| Configuration complexity | Provide sensible defaults, auto-tuning based on traffic analysis |
| Distributed state | Use Redis Cluster for high availability, fallback to local limiting |
| Clock drift | Use monotonic clocks, periodic synchronization, tolerance windows |
| No priority support | Add priority levels to bucket configuration (Phase 3 roadmap) |
| Memory for sliding window | Use Sliding Window Counter approximation instead of full log |

---

## Implementation Details

### Rust Implementation (Current)

Located at: `rust/phenotype-async-traits/src/lib.rs`

The current implementation provides a basic rate limiter:

```rust
pub struct AsyncRateLimiter {
    semaphore: PrioritySemaphore,
    max_per_second: u32,
}
```

This is a simple semaphore-based approach that limits concurrent requests but does
not implement a true token bucket algorithm. The planned enhancement will add:

- Token bucket with configurable capacity and refill rate
- Sliding window counter as an alternative algorithm
- Per-key rate limiting (for per-client limits)
- Metrics and monitoring

### Python Implementation (Planned)

Proposed design:
- `TokenBucket` class with `allow()` and `wait()` methods
- `SlidingWindowCounter` class for accurate limiting
- `RateLimiterManager` for managing multiple limiters
- `@rate_limit` decorator for easy usage
- Async context manager support

### Go Implementation (Planned)

Proposed design:
- `TokenBucket` struct with mutex-protected state
- `Allow()` method for non-blocking check
- `Wait(ctx)` method for blocking wait with context cancellation
- `RateLimiter` interface for algorithm abstraction
- Distributed rate limiting via Redis adapter

---

## Code Examples

### Rust: Token Bucket (Proposed)

```rust
use std::sync::Mutex;
use std::time::{Duration, Instant};

pub struct TokenBucket {
    tokens: f64,
    max_tokens: f64,
    refill_rate: f64, // tokens per second
    last_refill: Instant,
}

impl TokenBucket {
    pub fn new(max_tokens: f64, refill_rate: f64) -> Self {
        Self {
            tokens: max_tokens,
            max_tokens,
            refill_rate,
            last_refill: Instant::now(),
        }
    }

    pub fn allow(&mut self) -> bool {
        self.refill();
        if self.tokens >= 1.0 {
            self.tokens -= 1.0;
            true
        } else {
            false
        }
    }

    pub async fn wait(&mut self) {
        while !self.allow() {
            let wait_time = (1.0 - self.tokens) / self.refill_rate;
            tokio::time::sleep(Duration::from_secs_f64(wait_time)).await;
        }
    }

    fn refill(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_refill).as_secs_f64();
        self.tokens = (self.max_tokens)
            .min(self.tokens + elapsed * self.refill_rate);
        self.last_refill = now;
    }
}
```

### Python: Token Bucket (Proposed)

```python
import asyncio
import time
from dataclasses import dataclass

@dataclass(slots=True)
class RateLimitConfig:
    max_tokens: float = 100.0
    refill_rate: float = 10.0  # tokens per second
    key_function: callable = None

class TokenBucket:
    def __init__(self, max_tokens: float, refill_rate: float):
        self.max_tokens = max_tokens
        self.tokens = max_tokens
        self.refill_rate = refill_rate
        self.last_refill = time.monotonic()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.max_tokens, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def allow(self) -> bool:
        self._refill()
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False

    async def wait(self):
        while not self.allow():
            wait_time = (1.0 - self.tokens) / self.refill_rate
            await asyncio.sleep(wait_time)
```

### Go: Token Bucket (Proposed)

```go
package pheno_ratelimit

import (
    "context"
    "sync"
    "time"
)

type TokenBucket struct {
    mu         sync.Mutex
    tokens     float64
    maxTokens  float64
    refillRate float64
    lastRefill time.Time
}

func NewTokenBucket(maxTokens, refillRate float64) *TokenBucket {
    return &TokenBucket{
        tokens:     maxTokens,
        maxTokens:  maxTokens,
        refillRate: refillRate,
        lastRefill: time.Now(),
    }
}

func (tb *TokenBucket) Allow() bool {
    tb.mu.Lock()
    defer tb.mu.Unlock()

    now := time.Now()
    elapsed := now.Sub(tb.lastRefill).Seconds()
    tb.tokens = min(tb.maxTokens, tb.tokens+elapsed*tb.refillRate)
    tb.lastRefill = now

    if tb.tokens >= 1 {
        tb.tokens--
        return true
    }
    return false
}

func (tb *TokenBucket) Wait(ctx context.Context) error {
    for {
        if tb.Allow() {
            return nil
        }
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-time.After(10 * time.Millisecond):
        }
    }
}
```

### Python: Decorator Usage (Proposed)

```python
from pheno_resilience import rate_limit, TokenBucket

# Simple decorator
@rate_limit(max_tokens=100, refill_rate=10.0)
async def api_endpoint(request):
    return {"status": "ok"}

# With custom bucket
bucket = TokenBucket(max_tokens=50, refill_rate=5.0)

@rate_limit(bucket=bucket)
async def expensive_operation():
    return await process_data()
```

### Python: Per-Client Rate Limiting (Proposed)

```python
from pheno_resilience import RateLimiterManager, RateLimitConfig

manager = RateLimiterManager()

# Global rate limit
manager.add_limiter("global", TokenBucket(
    max_tokens=1000,
    refill_rate=100.0,
))

# Per-client rate limit
def get_client_key(request):
    return request.headers.get("X-Client-ID", request.client.host)

manager.add_limiter("per_client", TokenBucket(
    max_tokens=100,
    refill_rate=10.0,
), key_function=get_client_key)

# Per-endpoint rate limit
manager.add_limiter("search_endpoint", TokenBucket(
    max_tokens=30,
    refill_rate=3.0,
))
```

---

## Cross-References

### Related ADRs

- **ADR-001**: [Circuit Breaker Pattern](./ADR-001-circuit-breaker.md) — Circuit breaker handles sustained failures; rate limiter handles overload
- **ADR-002**: [Retry Strategy Design](./ADR-002-retry-strategy.md) — Rate limiting controls retry traffic volume

### Related Documentation

- **SOTA Research**: [RESILIENCE_PATTERNS_SOTA.md](../research/RESILIENCE_PATTERNS_SOTA.md) — Section 6: Rate Limiting Algorithms
- **Specification**: [SPEC.md](../SPEC.md) — Section 6: Rate Limiting System

### External References

- Token Bucket Algorithm — Wikipedia: https://en.wikipedia.org/wiki/Token_bucket
- Redis Rate Limiting — https://redis.io/docs/data-types/sorted-sets/#rate-limiting
- Nginx Rate Limiting — https://nginx.org/en/docs/http/ngx_http_limit_req_module.html
- AWS WAF Rate-Based Rules — https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html

### Implementation Files

- Rust: `rust/phenotype-async-traits/src/lib.rs` (basic, planned enhancement)
- Python: `python/pheno-resilience/src/pheno_resilience/` (planned)
- Go: `go/pheno-ratelimit/` (planned)

---

*ADR Version: 1.0*  
*Review Date: 2026-07-03*
