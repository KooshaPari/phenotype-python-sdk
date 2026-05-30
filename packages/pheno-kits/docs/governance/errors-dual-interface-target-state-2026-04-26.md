# Errors Dual-Interface Target State - 2026-04-26

## Decision Summary

Use both interfaces, but keep one contract:

- Rust owns the canonical taxonomy and conversions in `phenotype-error-core`.
- TypeScript exposes the same transport contract through `@phenotype/errors`.
- `phenotype-errors` as a Rust crate is optional and must be a thin facade over
  `phenotype-error-core` if it is created.

## Current Drift To Fix

| Surface | Current issue | Target |
|---|---|---|
| `phenoShared/PRD.md` | still references `@helios/errors` | rename contract docs to `@phenotype/errors` |
| `phenoShared/FUNCTIONAL_REQUIREMENTS.md` | still references `@helios/errors` | rename contract docs to `@phenotype/errors` |
| `phenoShared/packages/types/src/index.ts` | error envelope uses `code: string` | import or mirror the shared `ErrorCode` type |
| `phenoShared/package.json` | docs-only, no JS workspace wiring | explicitly include `packages/errors` in package/publish workflow |
| `phenoShared/packages/errors/package.json` | minimal metadata | add description, repository, license, readme, publish policy |
| `phenoShared/crates/phenotype-error-core` | Rust taxonomy is richer than JS flat codes | expose a stable wire-code/envelope layer |
| `phenoShared/crates/phenotype-errors` | absent | create only if real Rust consumers require facade name |

## Target File Map

### Contract Fixtures

```text
phenoShared/contracts/errors/
  error-codes.json
  error-envelope.schema.json
  fixtures/
    api-error.json
    domain-error.json
    repository-error.json
    config-error.json
    storage-error.json
```

Purpose: language-neutral contract. Rust and TS tests consume these fixtures.

### Rust

```text
phenoShared/crates/phenotype-error-core/
  Cargo.toml
  README.md
  CHANGELOG.md
  src/
    lib.rs
    code.rs
    envelope.rs
    layered.rs
  tests/
    contract_fixtures.rs
```

Required API:

```rust
pub enum ErrorCode { /* stable transport codes */ }

pub struct ErrorEnvelope {
    pub code: ErrorCode,
    pub message: String,
    pub details: serde_json::Value,
}

pub trait IntoErrorEnvelope {
    fn into_error_envelope(self) -> ErrorEnvelope;
}
```

Layered Rust-only errors (`ApiError`, `DomainError`, `RepositoryError`,
`ConfigError`, `StorageError`) remain allowed, but each must map to `ErrorCode`.

Optional facade:

```text
phenoShared/crates/phenotype-errors/
  Cargo.toml
  README.md
  CHANGELOG.md
  src/lib.rs
```

The facade may only re-export `phenotype-error-core`; it must not define a second
taxonomy.

### TypeScript

```text
phenoShared/packages/errors/
  package.json
  README.md
  CHANGELOG.md
  src/
    index.ts
    codes.ts
    envelope.ts
  tests/
    errors.test.ts
    contract-fixtures.test.ts
```

Required API:

```ts
export type ErrorCode = /* stable transport code union */;

export interface ErrorEnvelope {
  code: ErrorCode;
  message: string;
  details?: unknown;
}

export class PhenotypeError extends Error {
  readonly code: ErrorCode;
  readonly details?: unknown;
}
```

`HeliosAppError` can remain as a compatibility alias only if existing callers require
it. New docs should use `PhenotypeError`.

### Type Package Consumer

```text
phenoShared/packages/types/src/index.ts
```

Replace plain `code: string` envelopes with `ErrorCode` imported from
`@phenotype/errors`, or generate a shared local type if package workspace wiring is not
ready yet.

## Migration Order

1. Fix naming/spec drift: `@helios/errors` -> `@phenotype/errors`.
2. Add contract fixtures and schemas.
3. Add Rust wire-code/envelope API in `phenotype-error-core`.
4. Add package metadata and fixture tests to `packages/errors`.
5. Align `packages/types` envelope typing.
6. Create optional `crates/phenotype-errors` facade only if a real consumer requires
   the crate name.
7. Replace sibling-path consumers with tagged dependencies after tests pass.

## Validation Gates

- Rust tests parse all JSON fixtures and round-trip each `ErrorCode`.
- TypeScript tests parse the same fixtures and assert matching code strings.
- Docs list `@phenotype/errors`, not `@helios/errors`.
- `packages/types` no longer exposes generic `code: string` for shared errors.
- No release consumer points at `branch = "main"` or workstation-relative sibling
  paths.

## Non-Goals

- No WASM bridge.
- No FFI bridge.
- No second Rust taxonomy.
- No crates.io publishing until tag-based releases are proven.
