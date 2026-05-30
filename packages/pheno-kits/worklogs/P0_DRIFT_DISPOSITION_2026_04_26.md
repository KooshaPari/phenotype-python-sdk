# P0 Drift Disposition - 2026-04-26

## Policy

P0 drift repos are preservation-blocked. Do not push, force-push, reset, archive, or
delete until the repo has a written split/discard/publish decision.

## Repo Dispositions

| Repo | Branch | Upstream relation | Dirty signal | Disposition | Next executable lane |
|---|---|---|---|---|---|
| `agentapi-plusplus` | `chore/infrastructure-push` | ahead 7 | large `vendor/` deletion set | `QUARANTINE` | write branch-tip manifest, then split vendor cleanup from infra/docs |
| `phenoSDK` | `main` | ahead 11 | broad deletion of governance, CI, docs, package files | `QUARANTINE` | preserve current tip, recreate valid docs-only deprecation lane from current `main` |
| `PhenoProc` | `main` | ahead 8 / behind 12 | modified Cargo/worklog files plus many untracked roots | `QUARANTINE` | split Cargo crate alignment from docs/governance and untracked repo-like imports |
| `Dino` | `main` | ahead 8 / behind 77 | docs/ADR plus SDK/test additions | `SALVAGEABLE_SPLIT` | recreate docs ADR lane first; defer SDK/test seed to product review |
| `PhenoSpecs` | `main` | ahead 4 / behind 16 | registry/spec edits plus archive deletions | `SALVAGEABLE_SPLIT` | split registry/spec edits from archive deletion cleanup |
| `AuthKit/go` | `main` | no upstream shown | clean local status; nested repo under `AuthKit` | `POLICY_REQUIRED` | leave untouched until submodule vs vendored nested repo vs flattened source decision |
| shelf root `repos` | `docs/sunset-maturity-batch-2` | clean tracked state | many untracked child/worktree paths | `GOVERNANCE_ONLY` | only land curated governance docs from clean branches |

## Required Per-Repo Manifest Fields

Each follow-up manifest under `worklogs/p0-drift/` must include:

- absolute path
- remote URL
- branch and upstream
- HEAD SHA
- ahead/behind
- tracked status summary
- untracked summary
- nested `.git` or gitlink summary
- open/closed/no PR state
- recommended salvage branches
- explicit do-not-touch paths

## First Three Follow-Up PRs

1. `PhenoKits`: docs-only shared-crate ADR consolidation.
2. `Dino`: docs-only ADR/worklog salvage recreated from current `main`.
3. `PhenoSpecs`: registry/spec-only salvage recreated from current `main`.

`agentapi-plusplus`, `phenoSDK`, and `PhenoProc` are too mixed for immediate
source PRs. Their next action is manifesting, not rebasing. `AuthKit/go` is not
dirty in this checkout; it remains listed only because nested-repo ownership must
be resolved before sunset classification.
