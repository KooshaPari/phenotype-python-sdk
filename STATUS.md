# phenotype-python-sdk — Status

**Last updated:** 2026-06-17  
**Disposition:** [`docs/boundary/DISPOSITION.md`](docs/boundary/DISPOSITION.md)  
**Audit:** [`docs/audit/BLOCK-C-AUDIT.md`](docs/audit/BLOCK-C-AUDIT.md)

## Boundary verdict

**AFFIRM / KEEP ACTIVE** — canonical **`py-sdk-index`** workspace.

| Layer | Status | Canonical owner |
|-------|--------|-----------------|
| Python uv workspace (18 members) | Active | **This repo** |
| ObservabilityKit Py facade | Reconciled | **This repo** `packages/observability-kit` |
| TestingKit Py slice | Reconciled | **This repo** `packages/testing-kit` |
| ResilienceKit Py slice | File copy; impl red | **This repo** `packages/resilience-kit` |
| DataKit Py subtree | Complete | **This repo** `packages/data-kit` |
| AuthKit Py edge | Blocked | **This repo** — Tracera/thegent repoint open |
| McpKit Py edge | Partial | **This repo** — framework → PhenoFastMCP |
| PhenoKits hoists | De-nested | **This repo** `packages/phenotype-*` |
| Rust/Go in kit subtrees | Staging | **DECOMPOSE** to role owners |

## Consumer guidance

- **Python:** `uv sync` at repo root; install members per `pyproject.toml` workspace table.
- **Observe / test / resilience extras:** target `pip install phenotype-python-sdk[observe|test|resilience]` (P1 — not yet wired).
- **Rust/Go:** use PhenoObservability, TestingKit, Authvault, phenotype-go-sdk — not kit subtrees here.

## Next actions

1. Merge Block-C disposition PR.
2. Fix deploy-kit uv exclusion + wire role extras (Phase 2).
3. Execute chokepoint repoints for AuthKit (Phase 3).
4. Land `pheno_resilience` impl (Phase 4).
5. Polyglot ponytail DECOMPOSE PRs (Phase 5).
