# Plan: Org Sunset Maturity Program

## Phase 0 - Evidence Baseline

1. Snapshot open PRs, repo archive state, rulesets, and local drift manifests.
2. Save outputs in governance docs or worklogs.
3. Mark repos with unsafe local drift as `QUARANTINE`.

## Phase 1 - P0 Preservation

1. For each P0 repo, produce a file-level drift manifest.
2. Identify coherent lanes:
   - docs/governance
   - dependency/vendor cleanup
   - generated artifact cleanup
   - source behavior
   - nested gitlink repair
3. Create no PR until the lane is clean and current-main based.

## Phase 2 - Canonical Sources

1. Import Phase 1 shared crates into `phenoShared`.
2. Decide canonical owner for duplicated Kit crates.
3. Convert consumers from brittle relative paths to versioned git/tag or registry deps.
4. Update forced-adoption specs after canonical source PR lands.

## Phase 3 - Governance and Rulesets

1. Inventory all active repo rulesets.
2. Apply baseline only to repos with known CI workflows.
3. Update local governance docs alongside ruleset changes.
4. Avoid all-refs rulesets without bypass actors.

## Phase 4 - Branch and Archive Hygiene

1. Inventory no-PR branches older than 30 days.
2. Capture tip SHA before deleting any branch.
3. Remove Dependabot configs before archiving.
4. Re-run open PR search after each cleanup wave.

## Phase 5 - Consolidation

1. Merge dated worklogs into category indexes.
2. Preserve unique content from temporary docs.
3. Publish final maturity ledger.
