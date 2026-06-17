# Intent synthesis — phenotype-python-sdk

> Generated from prompt provenance in `prompts/`. Last updated: 2026-06-16.

## Themes (from prompts)

### Theme: py-sdk-index Python consolidation

**Prompts:** genesis rollout (cursor)

**User language (paraphrase with citations):**

- "Role: py-sdk-index per DOMAIN_ROLES.md" — genesis rollout directive
- "Copy/customize from HexaKit templates/genesis" — genesis bootstrap

## Confirmed goals

Goals explicitly stated by the user:

1. **Own `py-sdk-index` domain role** — Python package workspace / extras
2. **Bootstrap genesis docs from HexaKit template** — charter, intent, SOTA, OKF, review

## Inferred goals

Agent interpretation — **requires user validation**:

| Inferred goal | Evidence prompts | Agent action taken | Validate? |
|---------------|------------------|--------------------|-----------|
| Optional extras map to fleet roles | DOMAIN_ROLES | charter in-scope table | pending |
| auth-kit / mcp-kit stay non-uv until Poetry fix | pyproject.toml comments | SOTA technical.md | pending |

## Conflicts / tensions

| Tension | Prompts | Resolution |
|---------|---------|------------|
| Tier 1 Rust cores vs Python kit edges | DOMAIN_ROLES | SOTA technical.md Tier 2 table |
| Mixed Poetry/uv kits | pyproject.toml | Document exclusions in charter + dx |

## Rejected / deferred

- Rust rewrite of all Python kits without migration plan — deferred
- New standalone *Kit repos — rejected (absorbed)

## Recommended next actions (for agents)

1. Add auth-kit / mcp-kit to uv workspace when installable — aligns with [charter.md](../../../charter.md)
2. Run prompt scraper after significant sessions — update [intent.md](../../../intent.md)

## LLM grounding notes

When acting on this repo, agents should:

1. Read `charter.md` before adding Python packages
2. Prefer `docs/sota/technical.md` language placement over ad-hoc Rust ports
3. Append new user prompts to `prompts/` before large pivots
