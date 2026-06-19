# TestingKit boundary split — SDK edge (P4 #96)

**Date:** 2026-06-19  
**Registry SSOT:** [testingkit-boundary-split.md](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/disposition/testingkit-boundary-split.md)  
**Lane:** Non-blocker (ECOSYSTEM_DAG NB table)

## What this package owns

`packages/testing-kit` is the **Python test-role edge** of `phenotype-python-sdk`:

- `python/mcp-qa/` — MCP QA coordinator, pytest plugins, OAuth test helpers
- `python/qa-kit/`, quality/analysis CLIs absorbed from archived TestingKit
- Hoisted `packages/phenotype-testing` utilities

## What this package does **not** own

| Concern | Canonical owner |
|---------|-----------------|
| Rust BDD (`phenotype-bdd`) | **TestingKit** `rust/phenotype-bdd` |
| Rust contract tests | **TestingKit** `rust/phenotype-contract` |
| Rust fixtures / test infra | **TestingKit** `rust/phenotype-test-*` |
| E2E journey harness | **phenotype-journeys** |
| Playwright / per-repo CI scaffolds | **phenokits-commons** |

File parity with archived `KooshaPari/TestingKit` does not close the testing boundary — see registry doc for the full slice matrix and delete gate.

## Consumer pattern

```bash
# Target (when root extras land):
pip install "phenotype-sdk[test]"

# Today:
pip install -e "packages/testing-kit/python/mcp-qa"
```

Rust consumers must **not** use this subtree — pin `git+https://github.com/KooshaPari/TestingKit.git` workspace members under `rust/`.

## Related docs

- [testing-kit-mcp-qa-reconcile.md](../operations/testing-kit-mcp-qa-reconcile.md)
- [docs/boundary/DISPOSITION.md](../../../../docs/boundary/DISPOSITION.md) — module #4–5
