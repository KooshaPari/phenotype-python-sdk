# McpKit

[![Build](https://img.shields.io/github/actions/workflow/status/KooshaPari/McpKit/ci.yml?branch=main&label=build)](https://github.com/KooshaPari/McpKit/actions)
[![Release](https://img.shields.io/github/v/release/KooshaPari/McpKit?include_prereleases&sort=semver)](https://github.com/KooshaPari/McpKit/releases)
[![License](https://img.shields.io/github/license/KooshaPari/McpKit)](LICENSE)
[![Phenotype](https://img.shields.io/badge/Phenotype-org-blueviolet)](https://github.com/KooshaPari)

Polyglot MCP (Model Context Protocol) framework SDK for the Phenotype ecosystem. Provides idiomatic client and server primitives in Go, Rust, TypeScript, and Python from a single registry-driven source of truth.

**Part of the [Phenotype org](https://github.com/KooshaPari) ecosystem.** Shares CI reusables and conventions with [phenoShared](https://github.com/KooshaPari/phenoShared). Follows org conventions: conventional commits, `<type>/<topic>` branching, Apache-2.0 + MIT dual license.

## What it does

McpKit gives Phenotype services a uniform way to build and consume MCP servers/clients regardless of host language. A shared [`registry.yaml`](./registry.yaml) declares the canonical tool, resource, and prompt catalog; each language binding generates typed surfaces from it so Go services, Rust daemons, TypeScript IDE extensions, and Python notebooks all speak the same MCP contract.

Downstream consumers include agent frameworks, the [PhenoRuntime](https://github.com/KooshaPari/PhenoRuntime) MCP server, and external-intake pipelines.

## Status (Phase 1)

This repository is in **early scaffolding**. Binding maturity differs by language — choose accordingly:

| Binding     | State           | Notes |
|-------------|-----------------|-------|
| Python      | **Real**        | Lives in the `python/pheno-mcp` submodule (upstream: [`KooshaPari/PhenoMCP`](https://github.com/KooshaPari/PhenoMCP)). Build/test from there directly. |
| Rust        | **Real**        | `rust/` cargo workspace builds. Includes vendored `mcp-forge` codegen tooling. |
| Go          | **Scaffold**    | `go/go.work` only; no modules wired yet. Do not depend on this surface. |
| TypeScript  | **Scaffold**    | Directory placeholder; no package published yet. |

Owner: `team-agents`.

## Requirements

- **Go** binding (when implemented): Go 1.22+
- **Rust** binding: Rust stable, edition 2021
- **TypeScript** binding (when implemented): Node 20+ (pnpm preferred)
- **Python** binding: Python 3.11+ (`uv` or `pip`)

## Quick start

> **Note:** the root `pyproject.toml` is a *dev-tooling* config (pytest/black/ruff) for running checks across the workspace — it does **not** install any Python package. Real Python work happens inside the `python/pheno-mcp` submodule.

Clone with submodules:

```bash
git clone --recurse-submodules https://github.com/KooshaPari/McpKit.git
# or, after a plain clone:
git submodule update --init --recursive
```

Then build the binding you need:

```bash
# Rust (real)
cd rust && cargo build --workspace && cargo test --workspace

# Python (real — work inside the submodule)
cd python/pheno-mcp
pip install -e '.[dev]'   # or: uv sync
pytest

# Workspace dev tools (lint/format only — does NOT install pheno-mcp)
pip install -e '.[dev]' .  # from repo root, optional
```

Sample servers and a getting-started walkthrough live in the [PhenoMCP repo](https://github.com/KooshaPari/PhenoMCP). The McpKit-side `examples/` directory referenced in earlier drafts of this doc has not landed yet; track it via the open issue list.

Go and TypeScript bindings are not yet runnable — see **Status** above.

## Structure

```
go/            # Go MCP bindings — scaffold (go.work only)
rust/          # Rust MCP crates (cargo workspace) — real
typescript/    # TypeScript MCP bindings — scaffold (placeholder)
python/        # Python MCP bindings (submodule -> KooshaPari/PhenoMCP) — real
registry.yaml  # Canonical MCP tool/resource/prompt registry — source of truth
pyproject.toml # Workspace dev-tooling config (pytest/black/ruff); no package
```

## Design principles

- **Registry is the source of truth.** All bindings derive from `registry.yaml`; drift is a bug.
- **Idiomatic per language.** Each binding feels native (Go interfaces, Rust traits, TS generics, Python protocols) — the registry normalizes semantics, not surface syntax.
- **Wrap, do not hand-roll.** Leverages the official `modelcontextprotocol` SDKs where available; adds Phenotype conventions on top.
- **Fail loudly on contract mismatch.** Registry/binding divergence is caught at build time, not runtime.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Ownership lives in [CODEOWNERS](./CODEOWNERS). Report security issues per [SECURITY.md](./SECURITY.md).

## License

Dual-licensed under Apache-2.0 OR MIT. See [LICENSE-APACHE](./LICENSE-APACHE) and [LICENSE-MIT](./LICENSE-MIT).
