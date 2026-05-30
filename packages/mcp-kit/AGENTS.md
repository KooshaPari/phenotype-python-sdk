# AGENTS.md — McpKit

Polyglot MCP (Model Context Protocol) framework SDK — single registry-driven source of truth with bindings in Go, Rust, TypeScript, and Python.

## Repository identity

- Multi-language workspace: `go/`, `rust/`, `typescript/`, `python/`.
- Canonical contract: `registry.yaml` (root).
- Submodules: `python/pheno-mcp` -> upstream `KooshaPari/PhenoMCP` (see `.gitmodules`).
- Owner: `team-agents`.

## Binding maturity (verified from README)

| Binding    | State    |
|------------|----------|
| Python     | Real (in `python/pheno-mcp` submodule) |
| Rust       | Real (`rust/` cargo workspace) |
| Go         | Scaffold only (`go/go.work`, no modules wired) |
| TypeScript | Scaffold only (placeholder directory) |

## Build & test (verified from README)

```bash
# Clone with submodules first
git submodule update --init --recursive

# Rust binding
cd rust && cargo build --workspace && cargo test --workspace

# Python binding (work inside the submodule)
cd python/pheno-mcp
pip install -e '.[dev]'   # or: uv sync
pytest

# Workspace dev tooling (lint/format only — does NOT install pheno-mcp)
pip install -e '.[dev]' .
```

Root `pyproject.toml` is dev-tooling only (pytest/black/ruff). Real Python packaging lives in the submodule.

## Governance

- Dual license: Apache-2.0 + MIT (`LICENSE-APACHE`, `LICENSE-MIT`).
- Conduct: `CODE_OF_CONDUCT.md`. Contributing: `CONTRIBUTING.md`. Security: `SECURITY.md`.

## Commit & branch convention

- Conventional Commits.
- Branch: `<type>/<topic>`.

## Agent guardrails

- Do not depend on the Go or TypeScript surfaces — they are scaffolds.
- Generated typed surfaces must be re-derived from `registry.yaml`; never hand-edit generated bindings.
