# Block-C Audit — KooshaPari/phenotype-python-sdk

**Date:** 2026-06-17  
**Auditor:** ecosystem disposition wave (Block-C)  
**Charter:** [`phenotype-registry/docs/rationalization/boundary-shaping.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/rationalization/boundary-shaping.md)  
**Registry:** [`phenotype-registry/BOUNDARY_OWNERS.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/BOUNDARY_OWNERS.md) §Domain SDK  
**Role:** [`phenotype-registry/DOMAIN_ROLES.md`](https://github.com/KooshaPari/phenotype-registry/blob/main/DOMAIN_ROLES.md) — `py-sdk-index`

---

## Executive summary

| Signal | Finding |
|--------|---------|
| **Repo role** | Canonical **`py-sdk-index`** — Python package workspace + optional polyglot kit absorption staging |
| **Boundary lock** | **ACTIVE** — fleet Python install target for absorbed *Kit facades |
| **Absorption wave** | **MOSTLY COMPLETE** — ObservabilityKit, ResilienceKit, TestingKit reconciled; DataKit delete-eligible; AuthKit/McpKit blocked |
| **uv workspace** | **PASS** — 18 members resolve; `deploy-kit` excluded (stale `vercel` dep) |
| **Test collection** | **PARTIAL** — 109 collected; 11 collection errors (resilience impl gaps, mcp-qa naming collisions) |
| **Polyglot residue** | **HIGH** — Rust/Go trees retained inside kit subtrees; must **DECOMPOSE** to domain workspaces over time |
| **Primary risk** | Language-umbrella drift — duplicate per-kit `.github/`, governance markdown, non-Python release trains |
| **Recommended action** | Publish Block-C disposition; slim polyglot ponytails; execute chokepoint repoints; **KEEP ACTIVE** |

---

## Baseline checks

| Check | Result | Notes |
|-------|--------|-------|
| `uv sync --check` | **PASS** | Lockfile current @ c2338184d |
| uv workspace members resolve | **PASS** | 18 members; auth-kit/mcp-kit excluded (Poetry umbrellas) |
| `deploy-kit` in workspace | **FAIL** | Excluded — unsatisfiable `vercel>=0.10.0` vs PyPI |
| ObservabilityKit reconcile | **PASS** | 100% byte match; `docs/observe/observability-kit-retired.md` |
| TestingKit mcp-qa reconcile | **PASS** | PR #14; 34 blob divergences closed |
| ResilienceKit reconcile | **PASS** | PR #16; 2 divergent files documented |
| DataKit absorption | **PASS** | `packages/data-kit` full subtree; archive stub-only |
| AuthKit consumer repoint | **FAIL** | Tracera, thegent still blocked (batch3) |
| McpKit Py edge | **PARTIAL** | 12 Py files; framework → PhenoFastMCP (ADR-017) |
| `docs/boundary/DISPOSITION.md` | **FAIL** | This Block-C PR |
| `BOUNDARY.md` | **FAIL** | This Block-C PR |
| Genesis governance (charter, intent, SOTA) | **PASS** | PR #17 bootstrap |
| README kit table completeness | **FAIL** | Missing observability-kit, data-kit, hoisted packages |

---

## Absorbed-kit status (batch3 + registry)

| Source archive | SDK path | Reconcile | Archive gate |
|----------------|----------|-----------|--------------|
| ObservabilityKit | `packages/observability-kit` | 100% | **DELETE eligible** |
| ResilienceKit | `packages/resilience-kit` | 100% file copy | **KEEP_ARCHIVED** — Python impl red |
| TestingKit | `packages/testing-kit` | mcp-qa reconciled | **KEEP_ARCHIVED** — Rust split |
| DataKit | `packages/data-kit` | Full subtree | **DELETE eligible** |
| PhenoKits hoists | `packages/phenotype-*`, `pheno-cli-*` | De-nested 2026-06-02 | **KEEP_ARCHIVED** — template inflow |
| AuthKit | `packages/auth-kit` | Absorbed | **BLOCKED** — Tracera/thegent |
| McpKit | `packages/mcp-kit` | Partial Py | **BLOCKED** — PhenoFastMCP supersession |

---

## Role-indexed Python slices (registry authority)

Per `DOMAIN_ROLES.md` — organize by **domain role**, not language umbrella:

| Role extra | SDK path | Rust/Go canonical owner |
|------------|----------|-------------------------|
| `[observe]` | `packages/observability-kit/python` | **PhenoObservability** |
| `[test]` | `packages/testing-kit/python` | **TestingKit** `rust/` |
| `[resilience]` | `packages/resilience-kit/python` | **phenotype-resilience** (target) |
| `[connect]` | `packages/mcp-kit` (Py edge) + auth-kit Py | **PhenoFastMCP**, **Authvault** |
| `[config]` | `packages/phenotype-config` | **phenotype-config** / Settly |
| data | `packages/data-kit/python/db_kit` | **data-kit** role TBD |

---

## Cross-repo boundary overlaps

| Concern | Also present in | Canonical owner | SDK role |
|---------|-----------------|-----------------|----------|
| Rust auth crates | `packages/auth-kit/rust/` | **Authvault** | Staging — **DECOMPOSE** |
| Rust testing crates | archived TestingKit | **TestingKit** | Not duplicated here (Py only) |
| Rust observe | PhenoObservability | **PhenoObservability** | Py facade only |
| MCP framework | PhenoFastMCP, PhenoMCPServers | **PhenoFastMCP** | mcp-kit = Py edge + legacy polyglot |
| Go mcp/auth/platform | kit `go/` subtrees | **phenotype-go-sdk** | **DECOMPOSE** |
| Per-kit CI workflows | each `packages/*/.github/` | **This repo root** | Ponytail — consolidate |
| Genesis templates | HexaKit | **HexaKit** | Not owned |

---

## Archive gate status (for absorbed sources)

This repo is the **absorption target**, not an archive candidate. Gate applies to **source repos**:

| Source | Gate toward delete | SDK readiness |
|--------|-------------------|---------------|
| ObservabilityKit | 4/5 PASS | Facade canonical |
| DataKit | 4/5 PASS | Subtree complete |
| TestingKit (Py slice) | 5/5 PASS | Reconciled |
| ResilienceKit (Py slice) | 2/5 PARTIAL | File copy; impl red |
| AuthKit | 1/5 BLOCKED | Consumers open |
| McpKit | 2/5 BLOCKED | Framework moved |

**Verdict for this repo:** **KEEP ACTIVE** — do not archive or split.

---

## Related

- [`docs/boundary/DISPOSITION.md`](../boundary/DISPOSITION.md)
- [`docs/audit/BLOCK-C-CONSOLIDATION-PLAN.md`](BLOCK-C-CONSOLIDATION-PLAN.md)
- [`charter.md`](../../charter.md)
- [batch3 audit](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/operations/batch3-audit-2026-06-17.md)
