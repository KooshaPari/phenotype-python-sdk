---
title: Forced Adoption — Phase 1 Shared Crates (error-core, config-core, health)
status: PARTIAL_PROGRESS
state: PARTIAL_PROGRESS
date: 2026-04-25
last-updated: 2026-04-25
spec-id: forced-adoption-phase1-shared-crates
owners: phenotype-org / shared-platform
references:
  - docs/governance/cross-project-reuse-audit-2026-04-25.md
  - docs/governance/shared-crates-canonical-home-adr-2026-04.md
  - phenotype-infrakit PR #87 (Phase 1 LOC reduction, 2026-03-29)
---

## Reality 2026-04-25 (post-merge update)

Spec was authored and merged (PhenoKits PR #32) on 2026-04-25. Same-day
post-merge inspection of the actual consumer set on `origin/main`
revealed that the original audit's "8+ consumers per crate" framing was
inflated by drift, mirrors, and search-grep false-positives. The real
forced-adoption picture is materially smaller than spec assumed:

| Crate | Migrated | In flight | Remaining viable | Spec target |
|-------|----------|-----------|------------------|-------------|
| `phenotype-error-core` | 2 — AuthKit (PR #42), ResilienceKit (PR #15) | 0 | 1 candidate | ≥3 |
| `phenotype-config-core` | **0** | 0 | **0** — no real downstream consumers exist on origin/main | ≥3 (UNREACHABLE under current scope) |
| `phenotype-health` | 1 — TestingKit (PR #4) | 1 — hwLedger (PR pending; would bring to 2 simultaneous + 3-of-3 if it lands) | TBD | ≥3 |

**State transition:** `Draft → PARTIAL_PROGRESS`. The spec is partially
satisfiable for `error-core` and `health` but **structurally
unreachable for `config-core`** without either (a) descope of the
config-core branch from this spec, or (b) creating a new real consumer
(which is premature-extraction work, not adoption work). Recommendation
captured under "Adoption Reality" below.

## Adoption Reality

Three findings from the post-merge reality check, recorded here so the
next planner does not re-run the same broken audit:

1. **Audit inflation.** `cross-project-reuse-audit-2026-04-25.md` §2
   counted ~20 search hits per crate and labeled them "potential
   consumers". On real-Cargo-consumer inspection (a `[dependencies]`
   block in a non-infrakit, non-PhenoProc, non-PhenoObservability
   `Cargo.toml`), the realized pool is ~2–3 per crate, not 8+. Most
   hits were drift copies, vendored mirrors, or doc/spec/worklog
   prose. Treat any future "N consumers exist" claim as suspect until
   verified by `Cargo.toml` grep on `origin/main` only.
2. **`config-core` has zero real consumers.** Not "few" — zero. The
   crate consolidates a `figment`-backed `UnifiedConfigLoader` from
   patterns that, in practice, the downstream repos either do not use
   or have already inlined in shapes that don't fit the canonical
   API. This is **premature extraction**: shipped before any consumer
   demand existed, justified by a count that turned out to be
   doc-as-adoption.
3. **`error-core` and `health` are partially viable.** error-core has
   2 of 3 needed migrations done (AuthKit + ResilienceKit); 1 more
   suffices. health has 1 done (TestingKit) + 1 in flight (hwLedger);
   hitting ≥3 requires one more candidate after hwLedger lands.

### Recommended forward path (planner-only — no code in this spec)

- **error-core:** keep WP scope; identify one additional candidate
  (Discovery WP-001 / WP-004 substitute pool: Tracely, FocalPoint,
  Metron, BlueScript). Reach ≥3 via 1 more migration PR.
- **health:** land hwLedger PR (WP-014-equivalent for health, see
  tasks.md annotations); then identify one more candidate to backstop.
- **`config-core`: descope from this spec.** Either (a) move
  config-core to a separate "extraction validation" spec that requires
  finding/co-developing a real consumer before claiming reuse value,
  or (b) deprecate the crate as premature extraction and reclaim the
  ~400 LOC reduction claim from the original phenotype-infrakit PR
  #87 retrospective. The decision belongs to the canonical-home owner;
  this spec records the blocker, not the resolution.

### Status of original Goals (G-01..G-04)

- **G-01** (≥3 consumers per crate within one session): **partially
  achieved** for error-core (2/3) and health (1/3 + 1 in flight);
  **unreachable** for config-core under current consumer pool.
- **G-02** (per-PR LOC delta): **achieved** in landed PRs (AuthKit #42,
  ResilienceKit #15, TestingKit #4); LOC numbers tracked in PR bodies.
- **G-03** (≥5 distinct consumer repos in aggregate): **partially
  achieved** — 3 distinct repos so far (AuthKit, ResilienceKit,
  TestingKit), with hwLedger pending.
- **G-04** (audit re-run + doc update): **deferred** until error-core
  and health hit ≥3 each; config-core branch will not satisfy the
  original audit threshold and the audit doc must be amended to reflect
  the inflation finding from "Adoption Reality" item #1 above.

## Problem Statement

Phase 1 shared crates `phenotype-error-core`, `phenotype-config-core`, and
`phenotype-health` shipped on 2026-03-29 via phenotype-infrakit PR #87
(retroactive memory entry: "Phase 1 LOC Reduction Execution Complete"). The
PR consolidated 85+ error enums, 5+ health checks, and 4+ config loaders
into reusable building blocks projected to save ~2,350 LOC once adopted.

**One month later (2026-04-25), adoption is zero.** The cross-project
reuse audit (`docs/governance/cross-project-reuse-audit-2026-04-25.md`,
§2 "Adoption Rate") found:

- `phenotype-error-core`: ~20 search hits, **0** real Cargo consumers outside infrakit/PhenoProc
- `phenotype-config-core`: ~20 hits, **0** real Cargo consumers outside infrakit/PhenoProc
- `phenotype-health`: ~20 hits, **0–near-zero** real Cargo consumers outside infrakit/PhenoProc/PhenoObservability
- Direct `Cargo.toml` fetches for FocalPoint, Tracely, AgilePlus, thegent: **zero** `phenotype-*` entries.

The audit tags this the "doc-as-adoption antipattern": every search hit is
in `docs/adoption/`, `kitty-specs/`, audits, and worklogs — *talking*
about adoption, not adopting. The supply side is complete; the demand
side is empty.

### Canonical-home disambiguation

The canonical-home ADR (`docs/governance/shared-crates-canonical-home-adr-2026-04.md`)
designates **`phenoShared`** as the canonical home for the four legacy
crates (`phenotype-event-sourcing`, `-cache-adapter`, `-state-machine`,
`-policy-engine`). The Phase 1 crates are a **distinct cohort**:

| Crate | ADR canonical home | Phase 1 source | Plan-of-record canonical for adoption |
|-------|-------------------|----------------|----------------------------------------|
| `phenotype-event-sourcing` | `phenoShared` (ADR) | n/a | `phenoShared` |
| `phenotype-cache-adapter` | `phenoShared` (ADR) | n/a | `phenoShared` |
| `phenotype-state-machine` | `phenoShared` (ADR) | n/a | `phenoShared` |
| `phenotype-policy-engine` | `phenoShared` (ADR) | n/a | `phenoShared` |
| `phenotype-error-core` | (not in ADR) | `phenotype-infrakit` (PR #87) | `phenotype-infrakit` until org-hygiene migration is filed |
| `phenotype-config-core` | (not in ADR) | `phenotype-infrakit` (PR #87) | `phenotype-infrakit` until org-hygiene migration is filed |
| `phenotype-health` | (not in ADR) | `phenotype-infrakit` (PR #87); also present in `phenoShared/crates/phenotype-health` | **Disambiguation required** in Phase 1 Discovery — both copies exist; pick one canonical before forcing adoption |

Disambiguation work for `phenotype-health` is a **plan-phase deliverable**
(see plan.md Phase 1 Discovery, Task D-04). This spec does not
pre-resolve it; the discovery output feeds the migration delta in
Phase 2 Design.

## Goals

1. **G-01:** Within one session of agent-driven work, achieve **≥3 real
   downstream Cargo consumers** for each of the three Phase 1 crates
   (`phenotype-error-core`, `phenotype-config-core`, `phenotype-health`).
   "Real" = a `[dependencies]` block in a non-infrakit, non-PhenoProc,
   non-PhenoObservability `Cargo.toml` resolving against the canonical
   crate, with at least one canonical type referenced in `src/`.
2. **G-02:** Each migration PR demonstrates a measurable LOC delta:
   removal of the local error enum / config loader / health check that
   the canonical type now subsumes.
3. **G-03:** Aggregate-level: at least 5 distinct consumer repos
   complete at least one of the three migrations, providing a coverage
   matrix that is no longer monotone-zero.
4. **G-04:** Audit follow-up: re-run the §2 adoption-rate methodology
   from `cross-project-reuse-audit-2026-04-25.md` and update the doc
   with new counts (the audit explicitly flags this as Week 3–4 work,
   item #4 in §4 "Recommended Migration Order").

## Functional Requirements

| FR ID | Requirement | Acceptance Criteria |
|-------|-------------|---------------------|
| FR-01 | Candidate consumer set picked from top-active Phenotype-org repos | Phase 1 Discovery (plan.md) selects exactly 5 candidates from {AgilePlus, thegent, hwLedger, BytePort, PhenoKits} and records selection rationale in `discovery.md`. |
| FR-02 | Per-consumer migration delta documented before any code | Phase 2 Design (plan.md) produces, per (consumer × crate) pair, a side-by-side comparison of the consumer's local types vs. the canonical type, plus a written migration delta. No PR opens before this artifact exists. |
| FR-03 | AgilePlus adopts `phenotype-error-core` | AgilePlus crate(s) currently defining bespoke error enums add a `[dependencies]` entry for `phenotype-error-core`, replace ≥1 local error enum with a canonical type, and `cargo build --workspace` + `cargo test --workspace` pass. |
| FR-04 | AgilePlus adopts `phenotype-config-core` | One AgilePlus crate replaces a bespoke config loader with `UnifiedConfigLoader` from `phenotype-config-core`. Build + test green. |
| FR-05 | thegent adopts `phenotype-health` | thegent's harness/dispatcher (or other binary surface with a health probe) consumes `HealthChecker` from canonical `phenotype-health`. Build + test green. |
| FR-06 | hwLedger adopts `phenotype-error-core` | hwLedger replaces ≥1 local error type. Build + test green. Note: hwLedger already vendors `phenotype-event-sourcing` per ADR — coordinate to avoid double-touch in same PR. |
| FR-07 | BytePort adopts `phenotype-config-core` | BytePort replaces a local config loader. Build + test green. |
| FR-08 | PhenoKits adopts `phenotype-health` | PhenoKits adds a health-check surface using canonical `HealthChecker`. Build + test green. |
| FR-09 | Per-crate consumer count ≥3 | After all migration PRs land: `phenotype-error-core`, `phenotype-config-core`, `phenotype-health` each have ≥3 distinct repos in the consumer matrix (matrix lives in tasks.md). |
| FR-10 | Audit re-run | A follow-up commit to `docs/governance/cross-project-reuse-audit-2026-04-25.md` records the new adoption counts and removes the "Phase 1 supply/demand gap" finding from §5 once satisfied. |
| FR-11 | Canonical-home disambiguation for `phenotype-health` | Phase 1 Discovery output (plan.md D-04) selects exactly one canonical home between `phenotype-infrakit/crates/phenotype-health` and `phenoShared/crates/phenotype-health` and records ADR-style rationale. All FR-05/FR-08 PRs cite that selection. |

## Non-Goals

- **NG-01:** Do **not** deprecate any existing local error/config/health
  code in any consumer repo without a corresponding adoption PR landing
  first. The ADR's deprecation pattern (DEPRECATED.md banner, top-of-
  file marker, removal of duplicate sources) applies only **after**
  ≥3 real consumers exist; this spec explicitly forbids pre-adoption
  deprecation to avoid breaking the same workflows we are trying to
  consolidate.
- **NG-02:** No API changes to the canonical crates in this spec. If a
  consumer's local type cannot be expressed in the canonical type as
  shipped, that pair is **descoped from this spec** and routed to a
  separate "canonical API gap" follow-up. No "fix it as we go" canonical
  edits.
- **NG-03:** No re-homing of Phase 1 crates from `phenotype-infrakit`
  to `phenoShared` in this spec. That is a separate org-hygiene task
  (per ADR §"Out of scope"). The sole exception is FR-11's
  disambiguation for `phenotype-health`, which selects between two
  pre-existing copies — it does not create a new copy.
- **NG-04:** No Go-shared work (`phenotype-go-kit`, `urlguard`,
  `pathsafe`, etc.) — separate audit items #2 / #3 in the reuse audit.
- **NG-05:** No OTel-bootstrap consolidation (audit item #4) — separate
  spec.
- **NG-06:** No `phenotype-cloud-acquire` work (audit item #5) — defer
  per audit Week 5+ recommendation.

## Success Metric

A single command — re-running the audit grep methodology from
`cross-project-reuse-audit-2026-04-25.md` §2 — returns ≥3 real Cargo
consumers per Phase 1 crate, and the audit doc is amended accordingly.
Today that command returns **0** for all three. The forced-adoption
sweep is "done" when it returns ≥3 for all three.

## Cross-References

- **Reuse audit:** `docs/governance/cross-project-reuse-audit-2026-04-25.md`
  (see §2 Adoption Rate, §4 Recommended Migration Order item #4
  "Forced adoption sweep", §5 "Phase 1 supply/demand gap").
- **Canonical-home ADR:** `docs/governance/shared-crates-canonical-home-adr-2026-04.md`
  (this spec is downstream of the ADR for the `phenotype-health`
  disambiguation question only; Phase 1 crates are out of ADR scope).
- **Source PR:** phenotype-infrakit PR #87 (2026-03-29 LOC-reduction
  cohort). This spec is the missing demand-side counterpart.
