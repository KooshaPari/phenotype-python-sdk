# Block-C Consolidation Plan — KooshaPari/phenotype-python-sdk

**Date:** 2026-06-17  
**Status:** Approved for execution  
**Audit source:** `docs/audit/BLOCK-C-AUDIT.md`  
**Disposition:** `docs/boundary/DISPOSITION.md`  
**DAG lane:** Wave F (python/TS domain stubs) + Block-C boundary documentation

---

## Goal

Publish the **`py-sdk-index` boundary** for phenotype-python-sdk: canonical Python
install target for absorbed fleet kit facades; explicit decomposition targets for
retained polyglot (Rust/Go) staging trees; **KEEP ACTIVE** — not an archive candidate.

This **supersedes** implicit "language umbrella absorbs everything Python" interpretation
from early `RATIONALIZATION_PLAN.md` — role-indexed facades only per `DOMAIN_ROLES.md`.

---

## Current baseline (verified main @ c2338184d)

| Check | Result |
|-------|--------|
| `uv sync --check` | PASS |
| uv workspace members (18) | PASS |
| Genesis governance (charter, intent, SOTA) | PASS (PR #17) |
| ObservabilityKit reconcile | PASS |
| TestingKit mcp-qa reconcile | PASS (PR #14) |
| ResilienceKit reconcile docs | PASS (PR #16) |
| `docs/boundary/DISPOSITION.md` | This PR |
| deploy-kit in workspace | FAIL |
| AuthKit consumer repoint | FAIL (Tracera, thegent) |
| pheno_resilience impl + green tests | FAIL |
| Role extras `[observe]` etc. wired | FAIL (target) |
| Polyglot ponytail slim | FAIL |

---

## Phase 1 — Boundary documentation (P0)

| ID | Task | Acceptance |
|----|------|------------|
| C1.1 | Publish `docs/boundary/DISPOSITION.md` | 40-row module table |
| C1.2 | Publish `docs/audit/BLOCK-C-AUDIT.md` | Verdict = AFFIRM / KEEP ACTIVE |
| C1.3 | Publish this consolidation plan | Execution DAG documented |
| C1.4 | Add `BOUNDARY.md` + `STATUS.md` | Cross-references present |
| C1.5 | README disposition banner + full kit table | Links to disposition chain |

**Risk:** Low — docs only.

---

## Phase 2 — Workspace hygiene (P1)

| ID | Task | Acceptance |
|----|------|------------|
| C2.1 | Fix `deploy-kit` vercel dependency or pin alternative | `uv sync` includes deploy-kit |
| C2.2 | Wire optional role extras on root `[project.optional-dependencies]` | `pip install phenotype-python-sdk[observe]` resolves |
| C2.3 | Expand root CI to pytest uv members | CI green or documented skips |
| C2.4 | README: complete kit table (observability, data, hoists) | No stale 2026-06-02 work-state |

**Owner:** phenotype-python-sdk PRs post Block-C merge.

---

## Phase 3 — Chokepoint repoints (P2)

| ID | Task | Acceptance |
|----|------|------------|
| C3.1 | Tracera → `packages/auth-kit` path dep | AuthKit batch3 unblocked |
| C3.2 | thegent → auth-kit / Authvault facade | Same |
| C3.3 | Pyron → `phenotype-config` + obs extras | Registry wave3 lockstep |
| C3.4 | Fleet manifest scan: no new standalone *Kit Py imports | grep clean |

**Owner:** Consumer repos + registry chokepoint lane (L2).

---

## Phase 4 — Resilience implementation (P2–P3)

| ID | Task | Acceptance |
|----|------|------------|
| C4.1 | Implement `pheno_resilience` Python module | Tests collect + pass |
| C4.2 | Document ResilienceKit archive gate readiness | registry projects/ResilienceKit.json update |
| C4.3 | Strip `packages/resilience-kit/rust/` to pointer | DECOMPOSE PR paired with rust-sdk |

---

## Phase 5 — Polyglot decomposition (P3–P4)

| ID | Task | Acceptance |
|----|------|------------|
| C5.1 | Remove or redirect `packages/auth-kit/rust/` | Authvault owns crates |
| C5.2 | Slim `packages/mcp-kit` to Py edge; cite PhenoFastMCP | ADR-017 compliance |
| C5.3 | DECOMPOSE kit `go/` trees → phenotype-go-sdk | No Go release trains in py-sdk |
| C5.4 | Consolidate per-kit `.github/` into root | Single CI surface |
| C5.5 | Ponytail cut: kit `SPEC/PLAN/PRD` markdown zoo | Keep README + boundary docs |

---

## Phase 6 — Publish + archive execution (P5–P6)

| ID | Task | Acceptance |
|----|------|------------|
| C6.1 | PyPI trusted publishing for uv members | At least observe + test extras |
| C6.2 | Execute ObservabilityKit + DataKit archive delete | Registry gate 5/5 |
| C6.3 | Re-evaluate ResilienceKit + AuthKit + McpKit gates | Per-source verdict |
| C6.4 | Add `projects/phenotype-python-sdk.json` to registry | Role owner SSOT |

---

## Merge order

```text
Block-C docs (this PR)
  → Phase 2 workspace hygiene
  → Phase 3 chokepoints (parallel with Phase 4)
  → Phase 5 polyglot DECOMPOSE (paired PRs per kit)
  → Phase 6 publish + archive delete
```

---

## Related

- [TestingKit Block-C plan](https://github.com/KooshaPari/TestingKit/blob/main/docs/audit/BLOCK-C-CONSOLIDATION-PLAN.md)
- [PhenoObservability Block-C plan](https://github.com/KooshaPari/PhenoObservability/blob/docs/block-c-boundary-disposition/docs/audit/BLOCK-C-CONSOLIDATION-PLAN.md)
- [batch3 audit](https://github.com/KooshaPari/phenotype-registry/blob/main/docs/operations/batch3-audit-2026-06-17.md)
