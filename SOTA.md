# SOTA — phenotype-python-sdk

> **Last researched:** 2026-06-16  
> **Methods:** ADR-011 Python absorption audit, phenotype-registry DOMAIN_ROLES, uv workspace evaluation, internal dogfood

## Executive summary

| Dimension | Our choice | Confidence | Deep dive |
|-----------|------------|------------|-----------|
| Technical | uv workspace monorepo for Python SDK kits | high | [docs/sota/technical.md](docs/sota/technical.md) |
| DX | `uv sync` + per-kit README | med | [docs/sota/dx.md](docs/sota/dx.md) |
| UX | N/A (library/SDK repo) | n/a | [docs/sota/ux.md](docs/sota/ux.md) |
| AX | Genesis doc set + charter scope for Python packages | high | [docs/sota/ax.md](docs/sota/ax.md) |
| Security | Kilo Code Stand + secret scan in CI | med | [docs/sota/security.md](docs/sota/security.md) |
| Ops | Targeted `uv` / pytest per changed package | med | [docs/sota/ops.md](docs/sota/ops.md) |
| Cost | One Python SDK workspace vs N Kit repos | high | [docs/sota/cost.md](docs/sota/cost.md) |

## Why this is optimal (for our constraints)

Python is the **Tier 2 SDK edge** for `py-sdk-index`: absorbed kit repos already ship Python surfaces, uv gives fast cross-kit dependency resolution, and consolidating under one charter prevents duplicate package names and gives agents a single boundary for observe/connect/resilience/test Python extras.

## Fork status

- **Is fork:** no

## Evolution triggers

Re-open research when:

- Rust core crates reach parity for a kit edge — re-evaluate Python necessity
- uv workspace exceeds ~40 members — evaluate feature-group publishing
- Fleet role model adds new Python-only boundary

## Linkage

- Charter scope: [charter.md](charter.md)
- Review enforcement: [review.md](review.md)
- Intent goals: [intent.md](intent.md)
