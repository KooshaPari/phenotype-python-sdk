# ADR: Errors Dual-Interface Strategy

**Date:** 2026-04-26
**Status:** Accepted
**Decision owner:** phenotype-org / shared-platform
**Related:**

- `docs/governance/shared-crates-distribution-strategy-adr.md`
- `docs/governance/sunset-maturity-batch-3-execution-log-2026-04-26.md`
- `docs/governance/actual-shared-crates-audit-2026-04-25.md`

## Context

The sunset audit identified `phenotype-errors` as the only "shared errors" surface
with real cross-repo pressure. Follow-up inspection found that current `phenoShared`
does not contain `crates/phenotype-errors`; it contains:

- `crates/phenotype-error-core`: Rust canonical error foundation.
- `packages/errors`: a TypeScript package named `@phenotype/errors`.

Older docs mention `phenotype-errors` as if it were already present in `phenoShared`,
but current manifests do not support that. Creating a Rust crate solely to satisfy
stale prose would repeat the drift problem.

## Decision

Adopt a dual-interface strategy:

1. **Rust source of truth:** `phenotype-error-core` remains the canonical Rust error
   taxonomy and runtime type foundation.
2. **Rust facade only if needed:** create `crates/phenotype-errors` only as a thin
   facade over `phenotype-error-core` when an actual Rust consumer requires the
   facade name.
3. **TypeScript interface:** `packages/errors` remains the JS/TS interface for the
   same taxonomy, published separately as `@phenotype/errors`.
4. **Shared contract:** both interfaces must align through a small explicit schema
   or fixture set, not by one package pretending to be the other.
5. **Distribution:** Rust uses versioned git tags first; JS uses package-manager
   package metadata and tags. Do not use `branch = "main"` or workspace-relative
   sibling paths for release consumers.

## Rationale

- Rust and TypeScript consumers have different packaging and runtime needs.
- `phenotype-error-core` already exists in `phenoShared`; `phenotype-errors` does not.
- `packages/errors` already exists, so deleting or ignoring it would create another
  orphaned surface.
- A shared schema/fixture contract gives multi-language parity without forcing FFI,
  WASM, or generated bindings before there is evidence they are needed.

## Implementation Order

### Phase 1 - Contract

- Define canonical error codes, categories, and wire shape in one small contract file.
- Add conformance fixtures consumed by both Rust and TypeScript tests.
- Document the taxonomy in `phenoShared` root docs.

### Phase 2 - TypeScript Release Prep

- Add `packages/errors/README.md`.
- Add `packages/errors/CHANGELOG.md`.
- Add package metadata: `description`, `repository`, `license`, `readme`, and publish
  controls.
- Wire `packages/errors` into the repo's JS package workspace/publish flow.

### Phase 3 - Rust Release Prep

- Promote `phenotype-error-core` with README, changelog, and tag metadata.
- Only create `crates/phenotype-errors` if existing Rust consumers require the facade
  name; if created, it must re-export `phenotype-error-core` rather than define a
  parallel taxonomy.

### Phase 4 - Consumer Migration

- Replace sibling-path consumers with versioned tags or package versions.
- Convert JS consumers to `@phenotype/errors`.
- Convert Rust consumers to `phenotype-error-core` unless they explicitly need the
  facade crate.

## Non-Goals

- No WASM bridge in the first implementation.
- No FFI bridge in the first implementation.
- No crates.io publishing until the tag-based flow works and the API stabilizes.
- No Rust `phenotype-errors` crate unless there is a real consumer-driven need.

## Acceptance Criteria

- Rust and TypeScript tests consume the same error fixtures.
- `packages/errors` has release metadata and package-level docs.
- `phenotype-error-core` has release metadata and tag plan.
- No release consumer uses `branch = "main"` or a workstation-relative sibling path.
- If `crates/phenotype-errors` is created, it is a facade over `phenotype-error-core`
  and contains no independent taxonomy.
