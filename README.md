<!-- AI-DD-META:START -->
<!-- This repository is planned, maintained, and managed by AI Agents only. -->
<!-- Slop issues are expected and intentionally present as part of an HITL-less -->
<!-- /minimized AI-DD metaproject of learning, refining, and building brute-force -->
<!-- training for both agents and the human operator. -->
![Downloads](https://img.shields.io/github/downloads/KooshaPari/phenotype-python-sdk/total?style=flat-square&label=downloads&color=blue)
![GitHub release](https://img.shields.io/github/v/release/KooshaPari/phenotype-python-sdk?style=flat-square&label=release)
![License](https://img.shields.io/github/license/KooshaPari/phenotype-python-sdk?style=flat-square)
![AI-Slop](https://img.shields.io/badge/AI--DD-Slop%20Expected-orange?style=flat-square)
![AI-Only-Maintained](https://img.shields.io/badge/Planned%20%26%20Maintained%20by-AI%20Agents%20Only-red?style=flat-square)
![HITL-less](https://img.shields.io/badge/HITL--less%20AI--DD-metaproject-yellow?style=flat-square)

> ⚠️ **AI-Agent-Only Repository**
>
> This repo is **planned, maintained, and managed exclusively by AI Agents**.
> Slop issues, rough edges, and AI artifacts are **expected and intentionally
> present** as part of an **HITL-less / minimized AI-DD** metaproject focused
> on learning, refining, and brute-force training both the agents and the
> human operator. Bug reports and contributions are still welcome, but please
> expect AI-generated code, comments, and documentation throughout.
<!-- AI-DD-META:END -->

> **Boundary disposition (Block-C, 2026-06-17):** This repo is the canonical **`py-sdk-index`**
> workspace — Python facades for absorbed fleet kits live here. Rust/Go cores belong to
> domain role owners (PhenoObservability, TestingKit, Authvault, PhenoFastMCP, …).
> See [`docs/boundary/DISPOSITION.md`](docs/boundary/DISPOSITION.md) · [`BOUNDARY.md`](BOUNDARY.md) · [`STATUS.md`](STATUS.md).

## Work State

| Field | Value |
|---|---|
| Last commit | 2026-06-17 |
| Open issues | 1 |
| Open PRs | 1 |
| Focus | Block-C boundary disposition + uv workspace hygiene |

Progress: ████████░░ 80%

# phenotype-python-sdk

Monorepo of Phenotype org **Python SDK facades**, consolidated from standalone kit repositories.
Polyglot trees inside kit subtrees are absorption staging — see [BOUNDARY.md](BOUNDARY.md).

## Governance

Genesis documentation (charter, intent, SOTA, review, OKF): see [charter.md](charter.md). Role: **`py-sdk-index`** per [phenotype-registry DOMAIN_ROLES](https://github.com/KooshaPari/phenotype-registry/blob/main/DOMAIN_ROLES.md).

## Workspace kits

| Kit | Path | Role extra | Notes |
|-----|------|------------|-------|
| **observability-kit** | `packages/observability-kit` | `[observe]` | Python facade; Rust → PhenoObservability |
| **testing-kit** | `packages/testing-kit` | `[test]` | mcp-qa reconciled; Rust → TestingKit |
| **resilience-kit** | `packages/resilience-kit` | `[resilience]` | deploy-kit excluded from uv pending dep fix |
| **data-kit** | `packages/data-kit` | — | `db_kit` uv member |
| **auth-kit** | `packages/auth-kit` | `[connect]` | Consumer repoint pending (Tracera, thegent) |
| **mcp-kit** ⚠️ | `packages/mcp-kit` | `[connect]` | **DEPRECATED 2026-06-18** — mirror of `KooshaPari/McpKit` (source archived 2026-06-17). Use [`PhenoFastMCP`](https://github.com/KooshaPari/PhenoFastMCP) / [`PhenoFastMCP-rust`](https://github.com/KooshaPari/PhenoFastMCP-rust) / [`PhenoFastMCP-go`](https://github.com/KooshaPari/PhenoFastMCP-go) instead. Full retirement scheduled **2026-06-22**. See [`packages/mcp-kit/DEPRECATED.md`](packages/mcp-kit/DEPRECATED.md). |

### Hoisted publishables (from PhenoKits de-nest)

| Package | Path |
|---------|------|
| phenotype-config | `packages/phenotype-config` |
| phenotype-logging | `packages/phenotype-logging` |
| phenotype-id | `packages/phenotype-id` |
| phenotype-py-kit | `packages/phenotype-py-kit` |
| phenotype-testing | `packages/phenotype-testing` |
| pheno-cli-builder | `packages/pheno-cli-builder` |
| pheno-cli-kit | `packages/pheno-cli-kit` |

### Standalone SDK packages (not kits)

| Package | Path | Notes |
|---------|------|-------|
| **agentmcp-hex** 🆕 | `packages/agentmcp-hex` | Agentic MCP framework with hexagonal DDD architecture (extracted from `KooshaPari/McpKit` 2026-06-18, source archived 2026-06-17). Domain / ports / adapters / app layout. See [`ORIGIN.md`](packages/agentmcp-hex/ORIGIN.md). |

### Python sub-projects (under kits)

- `packages/testing-kit/python/` — `qa-kit`, `pheno-testing-cli`, `pheno-quality-tools`, `pheno-quality-cli`, `pheno-analysis-cli`, `mcp-qa`
- `packages/resilience-kit/python/` — `deploy-kit`, `ci-cd-kit`, `pheno-deploy`
- `packages/observability-kit/python/` — `performance_kit`, logging helpers

See each package’s `README.md` and `pyproject.toml` for install and usage.

## Development

Root `pyproject.toml` documents the workspace layout. Per-package tooling may use Poetry, setuptools, or Hatch — follow the kit you are changing.

```bash
cd packages/<kit>/python   # when applicable
# use that package's documented install (poetry install, pip install -e ., etc.)
```

## License

MIT — see [LICENSE](LICENSE).