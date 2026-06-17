# Cost — SOTA (phenotype-python-sdk)

## Use case

Total cost of ownership: infrastructure, API usage, CI minutes, maintainer time, and **duplicate governance** across repos.

## Requirements

| Requirement | Weight |
|-------------|--------|
| Minimize duplicate doc/CI copies across fleet | should |
| CI cost proportional to change type | must |
| Avoid N× Kit repo pattern without justification | must (Phenotype org) |

## Comparison model

| Model | Governance copies | CI / maintenance | Verdict |
|-------|-------------------|------------------|---------|
| Separate AuthKit + TestingKit + … repos | N× governance | N× CI | rejected — ADR-011 |
| Rust rewrite without migration | 1× governance | high rewrite cost | rejected |
| **Single uv workspace + genesis docs** | 1× charter | targeted pytest | **chosen** |

Fill with real numbers where available:

| Cost driver | Monthly estimate | Notes |
|-------------|------------------|-------|
| GitHub Actions minutes | low | doc-only PRs skip full build |
| Cloud / API | none | library repo |
| Maintainer hours (governance) | low | genesis bootstrap once |

## Alternatives considered

| Alternative | Cost profile | Verdict |
|-------------|--------------|---------|
| Duplicate `*Kit` archived repos | High — 9× governance per audit | rejected |
| SaaS doc portal only | subscription + lock-in | rejected |
| **Shared HexaKit genesis + py-sdk-index monorepo** | Lower — single scrape/review standard | **chosen** |

## Chosen strategy

Consolidating absorbed Python kits into one workspace reduces duplicate governance and CI while preserving Tier 2 Python only where SDK velocity and absorption cost favor it.

## Evolution triggers

- Workspace exceeds ~40 members → evaluate feature-group publishing (not new Kit repos)
- CI minutes exceed budget → tighten smoke matrix
- Fleet doubles → automate OKF validate in CI

Update [alternatives.md](alternatives.md) when cost model changes.
