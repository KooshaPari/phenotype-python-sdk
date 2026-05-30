# Worktree Quarantine Ledger - 2026-04-26

## Policy

This ledger is preservation-first. It classifies worktree containers and recovered
trees before any deletion or mutation. A path appearing here is not authorization to
delete it.

## Summary

| Metric | Count |
|---|---:|
| `.worktrees` containers | 6 |
| legacy `*-wtrees` containers | 37 |
| recovered containers | 1 |
| total containers | 44 |
| top-level wrapper roots | 33 |
| repo-local nested wrapper roots | 11 |
| immediate child dirs under wrappers | 284 |
| nested `.git` dirs within depth 3 | 142 |

## Disposition Vocabulary

| Disposition | Meaning |
|---|---|
| `keep-active` | Known active worktree with current work |
| `salvage` | Contains potentially useful work but must be split/replayed cleanly |
| `archive-reference` | Keep as read-only evidence/reference |
| `delete-candidate` | May be removed only after branch tip and PR state are recorded |
| `unknown` | Needs inspection before any decision |

## First-Pass Buckets

| Bucket | Includes | Rule |
|---|---|---|
| `active-worktree-forest` | non-empty `.worktrees` and `*-wtrees` roots | reconcile with `git worktree list --porcelain` |
| `recovered-checkout` | `Tracera-recovered` | create provenance record before any move/delete |
| `tombstone-or-marker` | empty wrapper roots | keep until owner and sentinel intent are known |

## Container Ledger

| Path | Type | Initial disposition | Notes |
|---|---|---|---|
| `.worktrees` | dot-worktrees | `unknown` | shelf-level worktree root; inspect each child |
| `agentapi-plusplus-wtrees` | legacy-wtrees | `salvage` | related P0 dirty repo; no deletion |
| `agentapi-plusplus/.worktrees` | dot-worktrees | `salvage` | nested project worktrees |
| `AgilePlus-wtrees` | legacy-wtrees | `salvage` | contains specs/runtime/generated state; inspect before pruning |
| `AgilePlus/.worktrees` | dot-worktrees | `salvage` | project-local worktrees |
| `AuthKit-wtrees` | legacy-wtrees | `salvage` | AuthKit has semantic stale-PR history |
| `bare-cua-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `BytePort-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `cliproxyapi-plusplus-wtrees` | legacy-wtrees | `unknown` | older recovery/build-fix lanes likely present |
| `cliproxyapi-plusplus/.worktrees` | dot-worktrees | `unknown` | project-local worktrees |
| `DataKit-wtrees` | legacy-wtrees | `unknown` | may include trusted-publishing lane |
| `Dino-wtrees` | legacy-wtrees | `salvage` | Dino local main is ahead/behind and dirty |
| `FocalPoint-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `helios-cli-wtrees` | legacy-wtrees | `unknown` | likely codex-rs/workspace dependency lanes |
| `heliosApp-wtrees` | legacy-wtrees | `unknown` | previous PR cleanup lanes may be stale |
| `heliosApp/heliosApp-wtrees` | legacy-wtrees | `unknown` | nested project worktrees |
| `heliosCLI-wtrees` | legacy-wtrees | `unknown` | classify separately from `helios-cli` |
| `heliosCLI/.worktrees` | dot-worktrees | `unknown` | project-local worktrees |
| `heliosCLI/heliosCLI-wtrees` | legacy-wtrees | `unknown` | nested project worktrees |
| `HexaKit-wtrees` | legacy-wtrees | `unknown` | shared-crate drift mirror context |
| `hwLedger-wtrees` | legacy-wtrees | `unknown` | contains canonical import/source lanes |
| `ObservabilityKit-wtrees` | legacy-wtrees | `unknown` | shared crate/vendor context |
| `pheno-wtrees` | legacy-wtrees | `unknown` | shared-crate drift mirror context |
| `PhenoKits-wtrees` | legacy-wtrees | `unknown` | coordination repo worktrees |
| `PhenoLang-wtrees` | legacy-wtrees | `unknown` | shared-crate drift mirror context |
| `PhenoObservability-wtrees` | legacy-wtrees | `unknown` | shared-crate consumer/path-dep context |
| `PhenoObservability/PhenoObservability-wtrees` | legacy-wtrees | `unknown` | nested project worktrees |
| `PhenoPlugins-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `PhenoRuntime-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `phenoShared-wtrees` | legacy-wtrees | `keep-active` | canonical shared-crate source may need release-prep lane |
| `PhenoSpecs-wtrees` | legacy-wtrees | `salvage` | local main is ahead/behind and dirty |
| `phenotype-infra-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `phenotype-journeys-wtrees` | legacy-wtrees | `unknown` | classify owner and PR state |
| `portage/portage-wtrees` | legacy-wtrees | `unknown` | nested repo worktrees |
| `repos-wtrees` | legacy-wtrees | `archive-reference` | shelf governance worktree history |
| `ResilienceKit-wtrees` | legacy-wtrees | `unknown` | shared crate/vendor context |
| `TestingKit-wtrees` | legacy-wtrees | `unknown` | shared crate consumer context |
| `thegent-wtrees` | legacy-wtrees | `unknown` | stale PR cluster history likely present |
| `thegent/.worktrees` | dot-worktrees | `unknown` | project-local worktrees |
| `thegent/thegent-wtrees` | legacy-wtrees | `unknown` | nested project worktrees |
| `Tracely-wtrees` | legacy-wtrees | `archive-reference` | separate from Tracera; do not merge identities |
| `Tracera-recovered` | recovered | `archive-reference` | recovery evidence; compare before deletion |
| `Tracera-recovered/trace-wtrees` | legacy-wtrees | `archive-reference` | recovered trace worktrees |
| `Tracera-wtrees` | legacy-wtrees | `salvage` | Tracera canonical checkout still needs routing |

## High-Risk Containers

- `.worktrees`: largest shared forest; includes AgilePlus, hexagonal ports,
  modules, portage, and Tracera docs lanes.
- `Tracera-recovered`: recovered checkout with runtime state, not disposable
  worktree noise.
- `AgilePlus/.worktrees`: active-looking project-local lanes, including paired
  clean branches.
- `heliosCLI/.worktrees` and `heliosCLI/heliosCLI-wtrees`: dual wrapper surfaces
  inside one repo.
- `thegent/.worktrees` and `thegent/thegent-wtrees`: dual wrapper surfaces inside
  one repo.

## Next Inspection Command

```bash
for d in .worktrees *-wtrees */.worktrees */*-wtrees *-recovered; do
  [ -d "$d" ] || continue
  find "$d" -maxdepth 2 -name .git -type d -print
done
```

For each nested repo found, record branch, upstream, dirty status, open PR URL,
and final disposition before removal or replay.
