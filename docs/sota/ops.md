# Ops — SOTA (phenotype-python-sdk)

## Use case

How this repo is built, tested, deployed, observed, and maintained in CI/CD and production (if applicable).

## Requirements

| Requirement | Weight |
|-------------|--------|
| PR CI completes in acceptable time budget | must |
| Default branch always green or explicitly quarantined | must |
| Template/doc changes have proportionate gates | must (genesis repos) |
| Runbooks for on-call (if production) | should |

## CI strategy (chosen)

| Change class | Gate |
|--------------|------|
| Docs / genesis markdown only | Link check; OKF validate (planned); **no full workspace build** |
| Single package change | Targeted `uv sync` + pytest for affected member |
| Workspace member add/remove | Full `uv lock` check + SOTA technical.md update |
| Governance doc change | Review agent charter/SOTA alignment |

```bash
# Example smoke — customize paths
uv sync && uv run pytest packages/testing-kit/python/qa-kit/tests
```

## Alternatives considered

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| Full workspace pytest on every PR | thorough | slow; doc PR friction | rejected for genesis |
| No CI on templates | fast | silent breakage | rejected |
| Nightly only CI | cheap | broken main until next day | rejected |
| **Targeted smoke per changed package** | proportional signal | requires path-aware CI | **chosen** |

## Observability (if applicable)

| Signal | Tool | Owner |
|--------|------|-------|
| CI failures | GitHub Actions | repo maintainers |

## Evolution triggers

- Smoke script false negatives → expand matrix row
- New kit subtree added → register in smoke script + this doc
- Production SLO breach → add ops runbook section

Update [../../../SOTA.md](../../../SOTA.md) Ops row when strategy changes.
