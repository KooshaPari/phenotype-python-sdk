# Boundary Lock: Python SDK index (`py-sdk-index`)

**Status:** ACTIVE — canonical Python package workspace for Phenotype fleet domain facades.

## Owns

- Root **uv workspace** (`pyproject.toml`, `uv.lock`) for publishable Python members
- Absorbed kit **Python facades** under `packages/`:
  - `observability-kit/python` — `[observe]` role edge
  - `testing-kit/python` — `[test]` role edge (mcp-qa, CLIs, qa-kit)
  - `resilience-kit/python` — `[resilience]` role edge (ci-cd-kit, pheno-deploy; deploy-kit pending)
  - `data-kit/python/db_kit` — data access helpers
  - `auth-kit/python` — `[connect]` auth edge (consumer repoint pending)
  - `mcp-kit/python` — thin MCP edge; framework → PhenoFastMCP
- Hoisted PhenoKits publishables: `phenotype-config`, `phenotype-logging`, `phenotype-id`,
  `phenotype-py-kit`, `phenotype-testing`, `pheno-cli-builder`, `pheno-cli-kit`
- Genesis governance: `charter.md`, intent, SOTA, OKF
- Absorption evidence docs (e.g. `docs/observe/observability-kit-retired.md`)

## Does NOT own

| Boundary | Owner repo |
|----------|------------|
| Rust observe core (tracing, metrics, OTEL) | **PhenoObservability**, **phenotype-otel** |
| Rust testing core (BDD, contract, fixtures) | **TestingKit** |
| Rust auth / identity core | **Authvault** |
| MCP framework (server/client SDK, transports) | **PhenoFastMCP**, **PhenoMCPServers** |
| Rust config core (`settly`) | **phenotype-config** workspace |
| Rust resilience patterns | **phenotype-resilience** (target) |
| Go platform / MCP HTTP edges | **phenotype-go-sdk** |
| Genesis templates and bootstrap scaffolds | **HexaKit** |
| E2E journey harness | **phenotype-journeys** |
| Fleet registry and role authority | **phenotype-registry** |

## Polyglot staging (temporary)

Rust/Go trees retained inside absorbed kit subtrees (`packages/*/rust/`, `packages/*/go/`)
are **absorption artifacts** — not long-term owners. Decompose to role workspaces per
Block-C disposition; do not add new polyglot release trains here.

## Consumer guidance

- **Python fleet consumers:** install from this repo (path dep or future PyPI extras) — not archived *Kit repos.
- **Rust/Go consumers:** use domain workspace owners above — not kit subtrees in this repo.

**Block-C disposition:** [docs/boundary/DISPOSITION.md](./docs/boundary/DISPOSITION.md)
