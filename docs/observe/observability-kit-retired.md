# ObservabilityKit retired (2026-06-17)

Archived source: `KooshaPari/ObservabilityKit` (archived on GitHub).
Canonical home: `phenotype-python-sdk` (`packages/observability-kit/`).

## Absorption status

Byte-for-byte reconcile completed: every file in the archived ObservabilityKit tree matches the SDK copy on `main`. No further code sync is required.

## Archive retirement

The archived `KooshaPari/ObservabilityKit` repository may be **deleted** after:

1. `phenotype-registry` marks ObservabilityKit `retired` with `absorbed_into: phenotype-python-sdk`.
2. Any registry consumers and CI jobs that still reference the archive repo are repointed to `phenotype-python-sdk`.

Rust observability primitives that remain outside this Python kit live under **PhenoObservability** and **phenotype-otel** per `phenotype-registry/DOMAIN_ROLES.md`.
