# Alternatives index — phenotype-python-sdk

Master comparison index across SOTA dimensions. PRs that change strategic choices must update the relevant dimension file **and** this index.

## Dimension decisions

| Dimension | File | Decision (one line) | Confidence |
|-----------|------|---------------------|------------|
| Technical | [technical.md](technical.md) | uv workspace monorepo; Tier 2 SDK edge | high |
| DX | [dx.md](dx.md) | `uv sync` + genesis docs | med |
| UX | [ux.md](ux.md) | N/A — library repo | n/a |
| AX | [ax.md](ax.md) | Genesis doc set + OKF + scraper | high |
| Security | [security.md](security.md) | Kilo Code Stand + CI secret scan | med |
| Ops | [ops.md](ops.md) | Targeted pytest per package | med |
| Cost | [cost.md](cost.md) | One Python SDK vs N Kit repos | high |

Executive summary: [../../../SOTA.md](../../../SOTA.md)

## Cross-cutting alternatives

| Decision | Alternatives rejected | Primary reason | ADR link |
|----------|----------------------|----------------|----------|
| Python SDK monorepo | Rust rewrite, split repos | absorption cost + SDK velocity | ADR-011 |
| uv workspace | Poetry-only monorepo | cross-kit resolution speed | ADR-011 |
| Single py-sdk-index owner | per-kit GitHub repos | N× governance | DOMAIN_ROLES |

## Fork repos

Not a fork — see [fork-rationale.md](fork-rationale.md).

## Research refresh log

| Date | Researcher | Dimensions updated | Notes |
|------|------------|-------------------|-------|
| 2026-06-16 | agent | all (bootstrap) | Genesis rollout from HexaKit template |

## Enforcement

[review.md](../../../review.md) Block tier: new uv workspace member or dependency without updating this index or SOTA technical.md → fail PR.
