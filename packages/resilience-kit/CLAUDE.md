# ResilienceKit — Workspace Operating Notes

## Project

Multi-language resilience and fault-tolerance toolkit for distributed systems. Includes retry policies, circuit breakers, bulkheads, and chaos engineering capabilities.

## Workspace Structure

```
ResilienceKit/
├── rust/                    # Rust resilience crates
│   ├── core/               # Core resilience patterns
│   │   └── phenotype-retry/
│   ├── phenotype-async-traits/
│   ├── phenotype-port-traits/
│   └── phenotype-state-machine/
├── go/                      # Go resilience packages
├── python/                  # Python resilience modules
├── chaos/                   # Chaos engineering tooling (future)
├── docs/
├── ADR.md
├── PLAN.md
├── PRD.md
└── SPEC.md
```

## Stack

### Rust
- **Language**: Rust Edition 2021
- **Edition**: 2021+
- **MSRV**: 1.70+
- **Workspace**: Monorepo with 4 crates
- **Test**: `cargo test --workspace`
- **Lint**: `cargo clippy --workspace -- -D warnings`
- **Format**: `cargo fmt --check`
- **Resolver**: v2

### Go
- **Version**: 1.24+
- **Test**: `go test ./...`
- **Lint**: `go vet ./...`
- **Format**: `gofumpt`

### Python
- **Version**: 3.11+
- **Test**: `pytest`
- **Lint**: `ruff check`, `mypy`
- **Format**: `ruff format`

## Crates Overview

| Crate | Purpose | Status |
|-------|---------|--------|
| **phenotype-retry** | Exponential backoff, jitter, deadline retry strategies | Active |
| **phenotype-async-traits** | Async trait helpers and utilities | Active |
| **phenotype-state-machine** | State machine for resilience patterns | Active |
| **phenotype-port-traits** | Port interfaces (Hexagonal) | Active |

## Design Principles

This repository follows **Hexagonal Architecture** with **SOLID**, **GRASP**, and **Law of Demeter**.

### Core Patterns
- **Retry**: Exponential backoff, jitter, deadline-aware
- **Circuit Breaker** (future): State-based failure isolation
- **Bulkhead** (future): Resource isolation and confinement
- **Chaos Engineering** (future): Fault injection and resilience testing

## Worktree Discipline

- Feature work goes in `.worktrees/<topic>/`
- Canonical repository remains on `main` for final integration and verification.
- Use `git status --short --branch` to verify main branch.

## Dependencies

- Cross-project: `phenotype-port-interfaces` from PhenoContracts
- Workspace: Internal crate dependencies managed via workspace.dependencies

## Quality Gates

All pushes must pass:
1. `cargo check --workspace`
2. `cargo test --workspace`
3. `cargo clippy --workspace -- -D warnings`
4. `cargo fmt --check`

For Python/Go, run respective lint/test suites.

## Governance Protocols

- Shared governance blocks: reference `Phenotype/repos/CLAUDE.md` for cross-project reuse protocol
- AgilePlus tracking: all work via `/repos/AgilePlus`
- Worktree standard: use `.worktrees/` for feature development, not legacy roots

## Related Repositories

- **PhenoContracts**: Port interface definitions
- **PhenoKits/HexaKit**: Hexagonal architecture templates
- **PhenoDevOps/chaos**: Chaos engineering tools (complementary)
- **Phenotype-infrakit**: Infrastructure patterns and integration

---

*Last updated: 2026-04-07 — Workspace structure initialization*
