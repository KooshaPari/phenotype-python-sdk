# Charter — phenotype-python-sdk

> **Boundary class:** sdk-domain  
> **Role:** py-sdk-index  
> **Lifecycle:** active  
> **Genesis template:** HexaKit `templates/genesis/` v1.0.0

## Mission

Consolidated Python package workspace and optional polyglot kit edges for Phenotype-org — the canonical `py-sdk-index` domain role owner per `phenotype-registry/DOMAIN_ROLES.md`.

## Scope

### In scope

- Root `uv` workspace (`pyproject.toml`, `uv.lock`) orchestrating publishable Python members
- Absorbed kit subtrees under `packages/`:
  - `auth-kit`, `data-kit`, `mcp-kit`, `observability-kit`, `resilience-kit`, `testing-kit`
  - Hoisted publishables: `pheno-cli-builder`, `pheno-cli-kit`, `phenotype-config`, `phenotype-id`, `phenotype-logging`, `phenotype-py-kit`, `phenotype-testing`
- Optional Python extras aligned to fleet roles: `[observe]`, `[connect]`, `[resilience]`, `[test]`
- Non-Python assets retained inside kit subtrees (Rust/Go) when absorption is cheaper than split
- Genesis governance: intent, charter, review, SOTA, OKF

### Out of scope

| Boundary | Owner repo |
|----------|------------|
| Rust config core (`settly`) | `phenotype-config` workspace |
| Rust observe core (Traceon, phenotype-otel) | `PhenoObservability`, `phenotype-otel` |
| Rust connect core (PhenoMCP, Authvault) | connect role crates |
| Go platform modules (devhex, devenv) | `phenotype-go-sdk` |
| Rust developer tooling, CI wrappers | `phenotype-tooling` |
| Static analysis runtime | `KodeVibe` |
| LLM validation | `kwality` |
| Genesis templates and bootstrap scaffolds | `HexaKit` |
| Application / product logic | product repos |
| Fleet registry and domain role authority | `phenotype-registry` |

## Governance artifacts

| Artifact | Path |
|----------|------|
| Intent | [intent.md](intent.md) |
| Review (Kilo Code Stand) | [review.md](review.md) |
| SOTA | [SOTA.md](SOTA.md) |
| OKF manifest | [okf/manifest.okf.yaml](okf/manifest.okf.yaml) |

Specs: [HexaKit docs/genesis/STANDARD.md](https://github.com/KooshaPari/HexaKit/blob/main/docs/genesis/STANDARD.md)

## Decision rights

| Action | Authority |
|--------|-----------|
| Merge to `main` | KooshaPari + 1 reviewer |
| Agent-authored PR | Allowed per [review.md](review.md) |
| Scope expansion | Charter amendment + intent synthesis update |
| New uv workspace member without SOTA | **Blocked** — requires `docs/sota/technical.md` justification |

**Agent autonomy:** Level 2 — agents may edit packages/docs within charter scope; new Python surfaces need SOTA paragraph.

## Dependencies

- Genesis bootstrap: HexaKit templates version `v1.0.0`
- Absorbed sources: AuthKit, DataKit, McpKit, ObservabilityKit, ResilienceKit, TestingKit, PhenoKits hoists
- Fleet registry: `phenotype-registry` (`py-sdk-index` role)

## Retirement

If this repo is absorbed: require **100% boundary coverage** in role owners before delete. Update `phenotype-registry` and OKF manifest.

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-06-16 | Initial charter from genesis template | agent |

## Attestation

This charter supersedes informal README scope claims. On conflict, charter wins.
