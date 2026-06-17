# phenotype-python-sdk — Per-Module Boundary Disposition

**Status:** Approved assessment  
**Date:** 2026-06-17  
**Repo:** `KooshaPari/phenotype-python-sdk`  
**Charter:** [`charter.md`](../../charter.md) · [`phenotype-registry/docs/rationalization/boundary-shaping.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/rationalization/boundary-shaping.md)  
**Audit:** [`docs/audit/BLOCK-C-AUDIT.md`](../audit/BLOCK-C-AUDIT.md)  
**Registry:** [`phenotype-registry/BOUNDARY_OWNERS.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/BOUNDARY_OWNERS.md) — Domain SDK layer  
**Role:** [`phenotype-registry/DOMAIN_ROLES.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/DOMAIN_ROLES.md) — `py-sdk-index`

> **Doctrine:** This repo owns **Python facades** for fleet domain roles — not Rust/Go canonical cores.
> Polyglot trees inside absorbed kit subtrees are **staging residue** until decomposed to role owners.
> Hard delete of source archives applies only after registry 5-condition gate passes.

---

## 1. Summary — recommended end-state

**phenotype-python-sdk is the canonical `py-sdk-index` workspace** — active, not archived.

| Concern | Owner after disposition |
|---------|-------------------------|
| Python publishables (uv workspace members) | **This repo** `packages/` |
| Optional role extras (`[observe]`, `[test]`, `[connect]`, …) | **This repo** root `pyproject.toml` (target) |
| ObservabilityKit Python facade | **This repo** `packages/observability-kit/python` |
| TestingKit Python slice (mcp-qa, CLIs) | **This repo** `packages/testing-kit/python` |
| ResilienceKit Python slice | **This repo** `packages/resilience-kit/python` (impl gap open) |
| DataKit Python (`db_kit`) | **This repo** `packages/data-kit/python` |
| PhenoKits hoisted packages | **This repo** `packages/phenotype-*`, `pheno-cli-*` |
| AuthKit Python (when repointed) | **This repo** `packages/auth-kit/python` |
| McpKit Python edge | **This repo** `packages/mcp-kit` — thin; framework → PhenoFastMCP |
| Rust auth core | **Authvault** — **DECOMPOSE** from `packages/auth-kit/rust/` |
| Rust testing core | **TestingKit** — not hosted here |
| Rust observe core | **PhenoObservability** |
| MCP framework | **PhenoFastMCP** + **PhenoMCPServers** |
| Go platform / MCP edges | **phenotype-go-sdk** — **DECOMPOSE** kit `go/` trees |
| Genesis templates | **HexaKit** |
| Fleet registry / role authority | **phenotype-registry** |
| This repository | **KEEP ACTIVE** |

**Do not** treat this repo as a language umbrella for Rust/Go. Retained polyglot assets are absorption artifacts with explicit decomposition targets.

---

## 2. Method

- Git tree `main` @ c2338184d (2026-06-17, post genesis PR #17)
- Cross-repo compare: absorbed archives (batch3 audit), sibling Block-C dispositions (TestingKit, PhenoObservability)
- Registry: `BOUNDARY_OWNERS.md`, `DOMAIN_ROLES.md`, `projects/*.json`
- Workspace: `uv sync --check`; pytest collect (109 tests, 11 collection errors)
- Prior work: PRs #14–#17 (kit reconciles + genesis bootstrap)

---

## 3. Top-level modules — disposition table

| # | Module (path) | What it is | Disposition | Target repo | Rationale |
|---|---------------|------------|-------------|-------------|-----------|
| 1 | Root `pyproject.toml` + `uv.lock` | uv workspace orchestrator | **DYNAMIC-KEEP** | This repo | SSOT for Python install graph |
| 2 | `packages/observability-kit/python/` | Python obs facade (`performance_kit`, logging helpers) | **DYNAMIC-KEEP** | This repo | `observe` role Py edge; 100% reconcile |
| 3 | `packages/observability-kit/go/` | Go obs stubs from archive | **DECOMPOSE** | PhenoObservability / go-sdk | Not py-sdk-index scope |
| 4 | `packages/testing-kit/python/` | mcp-qa, qa-kit, quality/analysis CLIs | **DYNAMIC-KEEP** | This repo | `test` role Py edge; reconciled |
| 5 | `packages/testing-kit/.github/` | Per-kit CI from archive | **DECOMPOSE** | Root `.github/` | Ponytail — consolidate workflows |
| 6 | `packages/resilience-kit/python/ci-cd-kit` | CI workflow templates (Python) | **DYNAMIC-KEEP** | This repo | uv member; resilience role edge |
| 7 | `packages/resilience-kit/python/pheno-deploy` | Deploy CLI (uv member) | **DYNAMIC-KEEP** | This repo | Active publishable |
| 8 | `packages/resilience-kit/python/deploy-kit` | Full deploy library | **DYNAMIC-KEEP** | This repo | Excluded from uv — fix `vercel` dep |
| 9 | `packages/resilience-kit/python/` pheno_resilience tests | Retry/CB/bulkhead impl | **ABSORB** | This repo | Tests red — impl landing required |
| 10 | `packages/resilience-kit/rust/` | Rust resilience from archive | **DECOMPOSE** | phenotype-resilience / rust-sdk | Wrong layer per BOUNDARY_OWNERS |
| 11 | `packages/data-kit/python/db_kit` | DB access helpers | **DYNAMIC-KEEP** | This repo | uv member; DataKit archive delete-eligible |
| 12 | `packages/data-kit/rust/`, `go/` | Polyglot data kit | **DECOMPOSE** | Role owner TBD | Staging only |
| 13 | `packages/auth-kit/python/` | Auth Python (Poetry umbrella) | **DYNAMIC-KEEP** | This repo | Blocked on Tracera/thegent repoint |
| 14 | `packages/auth-kit/rust/` | Auth Rust crates | **DECOMPOSE** | Authvault | Canonical connect/auth core |
| 15 | `packages/auth-kit/typescript/` | TS auth stubs | **DECOMPOSE** | Authvault / Conft edge | Not py-sdk-index |
| 16 | `packages/mcp-kit/python/` | MCP Python edge (12 files) | **DYNAMIC-KEEP** → slim | This repo | Framework → PhenoFastMCP; keep thin extras |
| 17 | `packages/mcp-kit/rust/`, `go/` | MCP polyglot from McpKit | **DECOMPOSE** | PhenoFastMCP*, go-sdk | ADR-017 supersession |
| 18 | `packages/phenotype-config` | Python config package | **DYNAMIC-KEEP** | This repo | `config` role Py edge |
| 19 | `packages/phenotype-logging` | Structured logging helpers | **DYNAMIC-KEEP** | This repo | Hoisted from PhenoKits |
| 20 | `packages/phenotype-id` | ID generation utilities | **DYNAMIC-KEEP** | This repo | Hoisted publishable |
| 21 | `packages/phenotype-py-kit` | Python kit umbrella module | **DYNAMIC-KEEP** | This repo | Hoisted publishable |
| 22 | `packages/phenotype-testing` | Testing utilities module | **DYNAMIC-KEEP** | This repo | Hoisted; pairs with testing-kit |
| 23 | `packages/pheno-cli-builder` | CLI scaffold builder | **DYNAMIC-KEEP** | This repo | Hoisted from PhenoKits |
| 24 | `packages/pheno-cli-kit` | CLI runtime kit | **DYNAMIC-KEEP** | This repo | Hoisted from PhenoKits |
| 25 | `docs/observe/observability-kit-retired.md` | Archive retirement note | **DYNAMIC-KEEP** | This repo | Absorption evidence |
| 26 | `charter.md`, `intent.md`, `SOTA.md`, `okf/` | Genesis governance | **DYNAMIC-KEEP** | This repo | py-sdk-index charter |
| 27 | `docs/intent/`, `docs/sota/` | Agent intent + SOTA corpus | **DYNAMIC-KEEP** | This repo | Genesis PR #17 |
| 28 | Per-kit governance (`SPEC.md`, `PLAN.md`, `PRD.md` in kits) | Archive planning markdown | **DECOMPOSE** → slim | phenotype-registry session artifacts | Ponytail on slim PR |
| 29 | Per-kit `docs/journeys/` | Journey manifest stubs | **DECOMPOSE** | phenotype-journeys | Not owned here |
| 30 | Per-kit `docs/operations/iconography/` | Unused SVG assets | **DELETE** | — | No fleet consumer |
| 31 | Root `.github/workflows/ci.yml` | Workspace CI | **DYNAMIC-KEEP** | This repo | Expand to cover uv members |
| 32 | `justfile` | Local dev tasks | **DYNAMIC-KEEP** | This repo | Agent ergonomics |
| 33 | `packages/*/registry.yaml` | Kit registry metadata | **DECOMPOSE** | phenotype-registry | Fleet index lives in registry |
| 34 | Role extras `[observe]` etc. (target) | Optional pip install groups | **ABSORB** | Root `pyproject.toml` | Not yet wired — P1 |
| 35 | `packages/auth-kit` uv exclusion | Poetry umbrella, empty packages | **DYNAMIC-KEEP** | This repo | Convert to hatchling member when Py lands |
| 36 | `packages/mcp-kit` uv exclusion | Same pattern | **DYNAMIC-KEEP** → slim | This repo | Align with PhenoFastMCP Py bindings |
| 37 | Source archive delete coordination | Registry gate for absorbed repos | **DYNAMIC-KEEP** | phenotype-registry | SDK is evidence holder |
| 38 | Consumer repoint (Tracera, thegent, Pyron) | Chokepoint manifests | **ABSORB** | Fleet consumers | Unblocks AuthKit archive |
| 39 | `pheno_resilience` implementation | Missing Python resilience core | **ABSORB** | `packages/resilience-kit/python` | Unblocks ResilienceKit archive |
| 40 | Repo itself | py-sdk-index canonical workspace | **KEEP ACTIVE** | phenotype-registry role map | Not archive candidate |

---

## 4. Supersession map

| Retired surface | Successor | Evidence |
|-----------------|-----------|----------|
| Standalone *Kit Python installs | This repo uv workspace | batch3 audit; subtree merges |
| ObservabilityKit archive | `packages/observability-kit` | 100% byte match doc |
| TestingKit Python install target | `packages/testing-kit` | mcp-qa reconcile PR #14 |
| McpKit as MCP framework | PhenoFastMCP + PhenoMCPServers | ADR-017; DOMAIN_ROLES `connect` |
| Language-umbrella SDK pattern | Role-indexed `py-sdk-index` | DOMAIN_ROLES anti-pattern table |
| PhenoKits as collection index | This repo IS the index | pyproject de-nest 2026-06-02 |

---

## 5. Execution phases

| Phase | Scope | Acceptance |
|-------|-------|------------|
| **P0** (this PR) | Block-C disposition + audit + consolidation plan | Docs on `main` |
| **P1** | Wire role extras; fix deploy-kit uv exclusion | `uv sync` includes deploy-kit |
| **P2** | AuthKit/McpKit consumer repoint (Tracera, thegent) | batch3 AuthKit unblocked |
| **P3** | Implement `pheno_resilience`; green resilience tests | ResilienceKit gate 4/5 |
| **P4** | Polyglot ponytail cut (kit `.github/`, rust/go DECOMPOSE PRs) | No independent kit release trains |
| **P5** | PyPI publish + fleet manifest scan | Consumers default to SDK extras |
| **P6** | Source archive delete execution | Registry 5/5 per absorbed repo |

---

## 6. Related documents

- [`docs/audit/BLOCK-C-AUDIT.md`](../audit/BLOCK-C-AUDIT.md)
- [`docs/audit/BLOCK-C-CONSOLIDATION-PLAN.md`](../audit/BLOCK-C-CONSOLIDATION-PLAN.md)
- [`BOUNDARY.md`](../../BOUNDARY.md)
- [`charter.md`](../../charter.md)
- [TestingKit Block-C disposition](https://github.com/KooshaPari/TestingKit/blob/main/docs/boundary/DISPOSITION.md)
- [PhenoObservability Block-C disposition](https://github.com/KooshaPari/PhenoObservability/blob/docs/block-c-boundary-disposition/docs/boundary/DISPOSITION.md)
