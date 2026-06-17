# Assumptions log — phenotype-python-sdk

Agents record beliefs about user intent here before acting on ambiguous asks. Each row links to prompt evidence where possible.

| Assumption | Evidence | Action taken | Validated? | Date |
|------------|----------|--------------|------------|------|
| Genesis rollout on feat/genesis-docs-rollout | genesis directive | Copied HexaKit templates/genesis/ | pending | 2026-06-16 |
| Python justified for py-sdk-index (Tier 2) | DOMAIN_ROLES + ADR-011 | SOTA technical.md language table | pending | 2026-06-16 |
| KooshaPari is default maintainer for review.md | fleet convention | review.md owner field | pending | 2026-06-16 |

## Validation states

| State | Meaning |
|-------|---------|
| `pending` | Agent acted; user has not confirmed |
| `yes` | User confirmed in session or follow-up prompt |
| `no` | User rejected — update [synthesis.md](synthesis.md) and [charter.md](../../../charter.md) if scope impact |

## Rules

1. Append a row when implementing an **inferred** goal from [synthesis.md](synthesis.md)
2. Mark `yes`/`no` when user clarifies in a new prompt (scrape to `prompts/`)
3. Do not delete rows — strike through superseded assumptions with date note

Refresh: after each major agent session affecting scope or architecture.
