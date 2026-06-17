# Intent — phenotype-python-sdk

## Problem statement

Phenotype-org Python SDK kits (auth, MCP, testing, observability, resilience, data) lived in standalone repos with duplicated governance, inconsistent workspace tooling (Poetry vs uv), and no fleet-wide `py-sdk-index` boundary. Agents could not infer which Python package path is canonical or when Python is justified vs Rust core crates.

## Success criteria

- [ ] Single canonical `uv` workspace with satisfiable lockfile for active members
- [ ] Absorbed kit subtrees documented; archive retirement eligibility tracked per role
- [ ] Genesis doc set (charter, review, intent, SOTA, OKF) linked and agent-readable
- [ ] Python placement documented in SOTA (Tier 2 SDK edge per domain role)

## Non-goals

See [charter.md](charter.md#out-of-scope). Key exclusions:

- Rust observe/connect/config cores (owned by role-specific Rust workspaces)
- Go platform modules (owned by `phenotype-go-sdk`)
- Genesis templates (owned by `HexaKit`)

## Originating prompts

Deterministic provenance in [docs/intent/prompts/](docs/intent/prompts/README.md).

| Date | Tool | Session | Summary |
|------|------|---------|---------|
| 2026-06-16 | cursor | genesis-rollout | [py-sdk-index role + Python SDK genesis docs](docs/intent/prompts/.gitkeep) |

Refresh: `python scripts/extract-intent-prompts.py --out-dir docs/intent/prompts --repo phenotype-python-sdk`

## Synthesized goals

Full synthesis: [docs/intent/synthesis.md](docs/intent/synthesis.md)

**Confirmed (user-stated):**

1. Own the `py-sdk-index` domain role for Python package workspace / extras
2. Bootstrap genesis governance from HexaKit `templates/genesis/`
3. Document Python as Tier 2 SDK edge per `phenotype-registry` DOMAIN_ROLES

**Inferred (needs validation):**

1. Optional extras (`[observe]`, `[connect]`, etc.) map to fleet role boundaries
2. auth-kit / mcp-kit remain non-uv members until Poetry umbrellas gain installable modules

## Agent assumptions log

| Assumption | Action taken | Validated? |
|------------|--------------|------------|
| User wants genesis rollout on `feat/genesis-docs-rollout` | Copied and customized genesis template | pending |
| Python justified for SDK kit edges (Tier 2) | Added SOTA technical.md language placement | pending |

Details: [docs/intent/assumptions.md](docs/intent/assumptions.md)
