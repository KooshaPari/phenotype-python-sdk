# Technical — SOTA (phenotype-python-sdk)

## Use case

Deliver consolidated Python SDK kits and hoisted publishables as the canonical `py-sdk-index` role owner for Phenotype-org.

**AgilePlus / FR trace:** ADR-011 Python kit absorption

## Requirements

| Requirement | Weight |
|-------------|--------|
| Single canonical package name per SDK concern | must |
| `uv sync` satisfiable for active workspace members | must |
| Tier 2 Python justification documented | must |
| Genesis governance linked from root | must |
| Rust rewrite of kit edges without SOTA | nice |

## Language placement

| Component | Lang | Tier | Rationale |
|-----------|------|------|-----------|
| testing-kit Python (qa-kit, pheno-testing-cli, …) | Python | 2 | Absorbed TestingKit; uv velocity; test role Py edge |
| observability-kit Python | Python | 2 | Absorbed ObservabilityKit; observe role Py edge |
| resilience-kit Python (ci-cd-kit, pheno-deploy) | Python | 2 | Absorbed ResilienceKit; resilience role Py edge |
| auth-kit / mcp-kit Python surfaces | Python | 2 | connect role Py edge; Poetry umbrellas pending uv member |
| phenotype-config / phenotype-logging hoists | Python | 2 | Shared SDK utilities; config role Py edge |
| Kit Rust/Go assets | Rust/Go | 2–3 | Retained in subtree when split cost exceeds benefit |
| Role cores (settly, Traceon, Authvault) | Rust | 1 | Owned outside this repo per DOMAIN_ROLES |

## Alternatives considered

| Alternative | Type | Pros | Cons | Verdict |
|-------------|------|------|------|---------|
| Keep *Kit standalone repos | internal | zero migration | N× governance; agent confusion | rejected — ADR-011 |
| Rust rewrite of all Python kits | internal | Tier 1 alignment | high cost; breaks Python consumers | rejected — no migration plan |
| Split Python packages per GitHub repo | internal | isolation | N× governance; package name drift | rejected |
| Poetry-only monorepo | internal | familiar | slow cross-kit resolution vs uv | rejected |
| **uv workspace monorepo (`phenotype-python-sdk`)** | chosen | absorption + single charter; fast sync | multi-kit maintenance | **chosen** |

Research sources: [phenotype-registry DOMAIN_ROLES](https://github.com/KooshaPari/phenotype-registry/blob/main/DOMAIN_ROLES.md), ADR-011, kit absorption execution.

## Chosen strategy

Root `pyproject.toml` defines `[tool.uv.workspace]` members for publishable Python packages. Absorbed kit subtrees retain polyglot assets under `packages/<kit>/`. auth-kit and mcp-kit excluded from uv members until Poetry umbrellas expose installable modules. All new Python workspace members require Tier 2 paragraph in this file before merge.

Link: [charter.md](../../../charter.md) · [intent.md](../../../intent.md)

## Evolution triggers

Re-open this dimension when:

- auth-kit / mcp-kit gain uv-compatible installable modules
- Rust core crate covers a kit edge with parity — revisit Python necessity
- uv workspace policy changes fleet layout

Update [alternatives.md](alternatives.md) and [../../../SOTA.md](../../../SOTA.md) executive table when verdict changes.
