# ADR 2026-04-26: Sunset Maturity Operating Model

## Status

Accepted.

## Context

The org-wide PR queue was cleared, but "no open PRs" is not the same as mature or sunset-ready.
The next risk is hidden work: dirty local repos, stale no-PR branches, drifted shared crates,
archived repos that can still emit dependency PRs, and governance docs that diverge from live
GitHub rulesets.

Prior cleanup also showed that broad governance/doc scaffold PRs become stale quickly and are
expensive to rebase. Future work needs a state model that separates active work, maintenance,
sunset-ready repos, archived repos, and quarantined unknown states.

## Decision

Adopt a five-state repo maturity model:

- `ACTIVE`: live product/library; roadmap and CI expected.
- `MAINTENANCE`: used but low-change; security and dependency policy expected.
- `SUNSET_READY`: no feature work; no open PRs; no Dependabot config; successor or canonical home documented.
- `ARCHIVED`: GitHub archived/read-only; no open PRs; no active automation that creates PRs.
- `QUARANTINE`: unsafe to mutate until local drift or canonical-home ambiguity is resolved.

Use this model for cross-repo cleanup decisions. Do not archive, delete, or force-push repos from
`QUARANTINE`. Do not treat archive/deprecation labels as authoritative without live repo evidence.

## Consequences

- PR cleanup remains necessary but insufficient.
- Dirty local repos become preservation tasks first, implementation tasks second.
- Archived repos can be temporarily unarchived for hygiene cleanup, but must be re-archived.
- Shared-source adoption must be preceded by canonical-home collapse and versioning decisions.
- Governance docs must be reconciled against live GitHub rulesets, not assumed correct.

## Implementation Requirements

- Maintain a repo-state ledger that records maturity state, evidence, and next action.
- Add a sunset checklist before archiving:
  - no open PRs
  - no Dependabot config
  - no active branch intended for merge
  - README successor/canonical-home note
  - archive reason recorded
- Keep ruleset changes and docs changes in the same governance lane.
- Keep generated governance/doc scaffolding out of mixed source-code PRs.

## Non-Goals

- This ADR does not authorize deleting repositories.
- This ADR does not choose canonical homes for every duplicated crate.
- This ADR does not imply all low-activity repos should be archived.
