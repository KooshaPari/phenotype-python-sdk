# ResilienceKit

Multi-language resilience and fault-tolerance toolkit for distributed systems. Provides production-grade retry policies, circuit breakers, bulkheads, timeouts, and chaos engineering capabilities across Rust, Go, and Python.

## Overview

**ResilienceKit** is the canonical resilience framework for building fault-tolerant distributed systems in the Phenotype ecosystem. It provides battle-tested patterns (retry strategies, circuit breakers, bulkheads, timeout policies) with language-idiomatic implementations while maintaining consistent semantics across all platforms.

**Core Mission**: Enable developers to build resilient systems with minimal complexity through well-designed, proven patterns and battle-tested implementations.

## Technology Stack

- **Languages**: Rust (primary), Go, Python (with unified semantics)
- **Core Patterns**:
  - **Retry Policies**: Exponential backoff, jitter, max retries, deadline tracking
  - **Circuit Breakers**: Threshold-based state machine with half-open recovery
  - **Bulkheads**: Isolation between independent workloads (semaphore-based)
  - **Timeouts**: Deadline-aware execution with cancellation
  - **Rate Limiting**: Token bucket, sliding window implementations
  - **Fallbacks**: Graceful degradation and default values
- **Rust Crates**:
  - `phenotype-retry` — Retry policy engines
  - `phenotype-async-traits` — Async resilience traits
  - `phenotype-port-traits` — Port/adapter patterns
  - `phenotype-state-machine` — Finite state machines (for circuit breakers)
- **Observability**: Metrics (counters, histograms), structured logging, trace integration

## Key Features

- **Production-Ready**: Battle-tested in high-reliability systems
- **Language-Idiomatic**: Native APIs for Rust, Go, Python with consistent semantics
- **Composable**: Stack patterns (retry + circuit breaker + timeout together)
- **Observable**: Built-in metrics and logging at every integration point
- **Type-Safe**: Strong type safety in Rust and Python (via type hints)
- **Performance**: Zero-copy architectures, minimal allocations
- **Flexible**: Customizable policies and hooks for advanced use cases
- **Testable**: Built-in chaos/fault injection for testing resilience

## Quick Start

```bash
# Clone and explore
git clone <repo-url>
cd ResilienceKit

# Review governance and architecture
cat CLAUDE.md          # Workspace organization
cat PRD.md             # Product requirements
cat SPEC.md            # Technical specification
cat AGENTS.md          # Agent operating contract

# Explore implementations
ls -la rust/           # Rust crates
ls -la go/             # Go packages
ls -la python/         # Python modules

# Build and test (Rust)
cd rust && cargo build --release && cargo test --workspace
cargo clippy --workspace -- -D warnings
```

## Project Structure

```
ResilienceKit/
├── rust/              # Rust implementation
│   ├── core/
│   │   └── phenotype-retry/
│   ├── phenotype-async-traits/
│   ├── phenotype-port-traits/
│   ├── phenotype-state-machine/
│   └── Cargo.toml
├── go/                # Go packages
│   ├── resilience/    # Core patterns
│   ├── chaos/         # Chaos injection
│   └── go.mod
├── python/            # Python modules
│   ├── resilience/    # Core patterns
│   ├── chaos/         # Chaos injection
│   └── pyproject.toml
├── docs/              # Shared documentation
├── SPEC.md            # Technical specification
├── PLAN.md            # Implementation plan
├── PRD.md             # Product requirements
└── CLAUDE.md, AGENTS.md
```

## Resilience Patterns

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Retry** | Transient failure recovery | Network timeouts, rate limits |
| **Circuit Breaker** | Prevent cascading failures | Downstream service down |
| **Bulkhead** | Workload isolation | Prevent one task exhausting resources |
| **Timeout** | Bounded execution | Prevent infinite waits |
| **Rate Limiting** | Control flow | Respect service rate limits |
| **Fallback** | Graceful degradation | Default values when service unavailable |
| **Chaos** | Resilience testing | Inject failures to verify recovery |

## Quality Requirements

- **Rust**: `cargo clippy -- -D warnings` (zero warnings), `cargo test --workspace`
- **Go**: `go vet ./...`, `go test ./...`, `gofumpt`
- **Python**: `ruff check`, `mypy`, `pytest`
- **Coverage**: ≥90% for critical paths
- **Documentation**: Comprehensive examples, guides, API docs

## Related Phenotype Projects

- **[PhenoLibs](../PhenoLibs)** — Uses resilience patterns in shared logic
- **[cloud](../cloud)** — Multi-tenant service resilience
- **[PhenoProc](../PhenoProc)** — Process-level resilience patterns
- **[ValidationKit](../ValidationKit)** — Validation with resilience integration

## License

MIT — see [LICENSE](./LICENSE).
