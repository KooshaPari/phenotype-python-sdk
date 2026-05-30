> **Pinned references (Phenotype-org)**
> - MSRV: see rust-toolchain.toml
> - cargo-deny config: see deny.toml
> - cargo-audit: rustsec/audit-check@v2 weekly
> - Branch protection: 1 reviewer required, no force-push
> - Authority: AGENTS.md

# PhenoKits

**The Phenotype org's umbrella checkout and shared-artifact monorepo.**

## What is this?

PhenoKits plays two related roles, which is the source of common confusion:

1. **Umbrella checkout (parent directory).** When you clone the full Phenotype workspace, `PhenoKits/` is the parent directory that holds ~30 sibling repos (AgilePlus, heliosApp, thegent, Civis, bifrost, etc.) as subdirectories so cross-cutting agents and humans can do org-wide work in one tree. In that role, PhenoKits is **not a project** — it is the workspace root.
2. **Shared-artifact monorepo (this repository).** Independently, `KooshaPari/PhenoKits` is a real git repo containing 12 categories of shared, cross-org artifacts (templates, configs, libs, governance, security, etc.) that every Phenotype project consumes.

In addition, **`HexaKit/`** inside this repo is a **sub-monorepo** included as a git submodule — a separate template/registry workspace, not a sibling subdir.

If you only see this single repo in isolation, you are looking at role (2): the shared-artifact monorepo. The umbrella role (1) only exists when this repo is checked out alongside the rest of the Phenotype org.

## Overview

PhenoKits-the-monorepo organizes artifacts into 12 distinct categories, each with clear mutability rules and agent interaction patterns.

## Categories

| # | Category | Purpose | Mutability |
|---|----------|---------|------------|
| 1 | [`templates/`](templates/) | Scaffolding for new projects | Editable |
| 2 | [`configs/`](configs/) | Parameterized configs | Parameters only |
| 3 | [`libs/`](libs/) | Multi-language libraries | Import/extend |
| 4 | [`secrets/`](secrets/) | Secret management patterns | Locked |
| 5 | [`governance/`](governance/) | ADRs, RFCs, standards | Varies |
| 6 | [`security/`](security/) | Scanning, policies, hardening | Locked |
| 7 | [`observability/`](observability/) | Logging, metrics, tracing | Configurable |
| 8 | [`docs/`](docs/) | API docs, runbooks, guides | Editable |
| 9 | [`scripts/`](scripts/) | Build, release, quality scripts | Executable |
| 10 | [`schemas/`](schemas/) | Type definitions, API specs | Locked |
| 11 | [`policies/`](policies/) | OPA, GitHub, compliance | Enforced |
| 12 | [`credentials/`](credentials/) | Auth configs, patterns | Locked |

## Bundled Kits

These are the buildable / structured kits available inside or alongside this repo.

| Kit | Location | Type | Notes |
|-----|----------|------|-------|
| HexaKit | [`HexaKit/`](HexaKit/) | **Sub-monorepo (git submodule)** | Hexagonal-architecture template CLI + registry. Has its own Cargo workspace; build from inside `HexaKit/`. |
| Civis | [`KooshaPari/Civis`](https://github.com/KooshaPari/Civis) | Sibling repo | Deterministic simulation and policy-driven architecture workspace. Cloned as a sibling at the umbrella level, not embedded here. |
| Hexagon | [`hexagon/`](hexagon/) | In-repo directory | Hexagonal artifacts curated alongside the kits. |

> Removed from prior docs: `PhenoLibs` row — that kit does not exist in this repo. Use [`libs/`](libs/) for multi-language library artifacts instead.

## Quick Reference

### Agent Interaction Matrix

| Category | Agent Observes | Agent Mutates | Agent Validates |
|----------|----------------|---------------|-----------------|
| Templates | Yes | Instantiated outputs only | No |
| Configs | Yes | Parameters only | Yes (validation) |
| Libs | Yes | No, except generated wrappers | No |
| Secrets | References and metadata only | No | Yes (scanning) |
| Governance | Yes | Yes (ADRs) | No |
| Security | Yes | Yes | Yes (scanning) |
| Observability | Yes | Yes (configs/dashboards) | Yes (monitoring) |
| Docs | Yes | Yes | No |
| Scripts | Yes | Yes | No |
| Schemas | Yes | Yes (code gen) | Yes (type checking) |
| Policies | Yes | Yes | Yes (OPA, gates) |
| Credentials | Broker state only | No | Yes (rotation/expiry checks) |

This matrix describes permission boundaries, not broad technical capability.
Agents should never read or write raw secret or credential material; they may
reference vault handles, metadata, rotation status, and validation results.

## Directory Structure

```
PhenoKits/
├── HexaKit/             # Sub-monorepo (git submodule) — template CLI + registry
├── templates/           # 1. Scaffolding
│   ├── hexagonal/       # Hexagonal architecture templates
│   ├── clean-rust/      # Clean architecture Rust template
│   └── phenotype-api/   # Phenotype API template
├── configs/             # 2. Parameterized configs
├── libs/                # 3. Libraries (rust/python/typescript/go)
├── secrets/             # 4. Secret management
├── governance/          # 5. ADRs, RFCs, standards
├── security/            # 6. Security configs
├── observability/       # 7. Logging, metrics
├── docs/                # 8. Documentation
├── scripts/             # 9. Automation scripts
├── schemas/             # 10. Type definitions
├── policies/            # 11. Enforcement policies
├── credentials/         # 12. Auth configs
└── hexagon/             # Curated hexagonal artifacts
```

## Quick Start

### Clone with the HexaKit sub-monorepo

```bash
git clone --recurse-submodules https://github.com/KooshaPari/PhenoKits.git
cd PhenoKits
# If you forgot --recurse-submodules:
git submodule update --init --recursive
```

### Build the HexaKit sub-monorepo

The repo root's `Cargo.toml` declares `members = []` (it intentionally excludes
`HexaKit/` and the language-specific `libs/*` workspaces). To build buildable
Rust code, enter the relevant sub-workspace:

```bash
# Build HexaKit (sub-monorepo Cargo workspace)
cd HexaKit && cargo build

# Or build the Rust libs sub-workspace
cd libs/rust && cargo build
```

### For Agents

```bash
# Read agent patterns
cat docs/AGENT_PATTERNS.md

# Apply a config
python3 scripts/utility/parameterize.py \
    configs/params.example.json \
    configs/cicd/github-actions/ci.yml
```

### For Developers

```bash
# Apply org configs
cp -r configs/tooling/pre-commit/* .git/hooks/

# Set up CI
cp configs/cicd/github-actions/* .github/workflows/

# Configure observability
cp configs/observability/prometheus.yml ./
```

## Related

- [RESTRUCTURING_PLAN.md](docs/RESTRUCTURING_PLAN.md) — Full restructuring plan
- [RESTRUCTURING_ADR.md](docs/RESTRUCTURING_ADR.md) — Decision record
- [AGENT_PATTERNS.md](docs/AGENT_PATTERNS.md) — Agent consumption patterns
- [HexaKit/](HexaKit/) — Template CLI and registry (sub-monorepo)
- [PhenoKit](https://github.com/KooshaPari/PhenoKit) — Core SDK
- [PhenoSpecs](https://github.com/KooshaPari/PhenoSpecs) — Specifications
- [Civis](https://github.com/KooshaPari/Civis) — Sibling governance/simulation workspace
