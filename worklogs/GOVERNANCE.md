# GOVERNANCE

Entries tracking policy, compliance, quality gates, enforcement, branch protection, and organizational governance decisions.

**Last updated:** 2026-04-26  
**Entries:** 4

---

## 2026-04-25 AgilePlus Pre-Push Hook Test Failure Triage

**Summary:** 17 failing tests across 4 AgilePlus crates (agileplus-api, agileplus-plane, agileplus-telemetry). Root causes: (a) real bug — duplicate route overlap; (c) fixture drift — utoipa 5 API removal, wiremock matcher shape; (d) test scope drift — doctest references removed symbols. Aggregate fix: 35–65 minutes. P0 blocker: api route merge kills 14 integration tests.

**Evidence:** 4 issues (P0–P1) with specific line refs and fix estimates. All failures deterministic and reproducible.

**Recommendation:** Re-enable pre-push hook on next PR (post-fix); hook bypass via `HOOKS_SKIP=1` is the exact failure mode CI Completeness Policy forbids.

**Source:** [AGILEPLUS_TEST_FAILURE_TRIAGE_2026_04_25.md](./AGILEPLUS_TEST_FAILURE_TRIAGE_2026_04_25.md)

---

## 2026-04-25 Phenotype Local Drift Manifest & Post-PR Cleanup Audit

**Summary:** Post-PR cleanup survey of 218 local repos found 186 with drift, 126 dirty working trees. GitHub PR count is zero; next backlog is branch hygiene, governance enforcement mismatch, and local work preservation. High-risk repos: agentapi-plusplus (4,681 changes), phenoSDK (2,189 changes), PhenoProc (nested gitlink dirt + ahead/behind).

**Key Findings:**
- 7 repos require split/discard decisions before sync
- Stale no-PR branches (pr/211, pr/683 on cliproxyapi-plusplus; calver-migration on heliosApp)
- Governance docs (CODEOWNERS, branch protection, rulesets) locally documented but not enforced on GitHub for 7+ repos
- Worklogs/session artifacts spread across shelf root and repo-specific dirs (needs consolidation)

**WBS:** P0 preserve/classify (freeze + manifest), P1 branch hygiene + governance enforcement, P2 docs/worklog consolidation.

**Source:** [PHENOTYPE_LOCAL_DRIFT_MANIFEST_2026_04_25.md](./PHENOTYPE_LOCAL_DRIFT_MANIFEST_2026_04_25.md) + [PHENOTYPE_POST_PR_CLEANUP_AUDIT_WBS_2026_04_25.md](./PHENOTYPE_POST_PR_CLEANUP_AUDIT_WBS_2026_04_25.md)

---

## 2026-04-26 Sunset Maturity Operating Model

**Summary:** PR cleanup is complete, but the ecosystem is not sunset-ready until every repo is classified as `ACTIVE`, `MAINTENANCE`, `SUNSET_READY`, `ARCHIVED`, or `QUARANTINE`. The model separates PR queue health from hidden local drift, shared-source sprawl, branch hygiene, and ruleset enforcement.

**Key Decisions:**
- Dirty or ambiguous repos default to `QUARANTINE`, not archive.
- Archived repos must have no open PRs and no active Dependabot config.
- Shared crates require a canonical home before forced adoption.
- Live GitHub rulesets, not docs alone, define actual governance enforcement.

**Source:** [SUNSET_MATURITY_WBS_2026_04_26.md](./SUNSET_MATURITY_WBS_2026_04_26.md), [../docs/governance/sunset-maturity-audit-2026-04-26.md](../docs/governance/sunset-maturity-audit-2026-04-26.md), [../docs/governance/adr-2026-04-26-sunset-maturity-operating-model.md](../docs/governance/adr-2026-04-26-sunset-maturity-operating-model.md)
