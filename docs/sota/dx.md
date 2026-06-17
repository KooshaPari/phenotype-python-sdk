# DX — SOTA (phenotype-python-sdk)

## Use case

How developers clone, sync, test, and publish Python SDK packages in this workspace.

## Requirements

| Requirement | Weight |
|-------------|--------|
| Documented bootstrap path (<15 min to first green test) | must |
| Local dev matches CI (`uv sync`, pytest) | should |
| Genesis docs discoverable from README | must |

## Workflow (chosen)

1. Clone repo and read [charter.md](../../../charter.md) for kit boundaries
2. Run `uv sync` from repo root
3. Test changed package: `uv run pytest packages/<kit>/python/<pkg>/tests` (or kit-documented command)
4. For governance changes, update OKF manifest and SOTA as needed

```bash
git clone https://github.com/KooshaPari/phenotype-python-sdk.git
cd phenotype-python-sdk
uv sync
uv run pytest packages/testing-kit/python/qa-kit/tests  # example
```

## Alternatives considered

| Alternative | Pros | Cons | Verdict |
|-------------|------|------|---------|
| Per-kit clone (old *Kit repos) | isolation | duplicate governance | rejected |
| README-only onboarding | zero maintenance | agents ignore scope | rejected |
| **uv workspace + genesis docs** | single charter; linked review/SOTA | manual member curation | **chosen** |

## Pain points mitigated

| Pain | Mitigation |
|------|------------|
| Duplicate package names | charter Block tier; uv workspace naming |
| Agent scope creep | review.md + charter out-of-scope table |
| Lost session prompts | `docs/intent/prompts/` scraper |
| Mixed Poetry/uv kits | pyproject.toml documents exclusions; per-kit README |

## Evolution triggers

- auth-kit / mcp-kit join uv workspace → update workflow
- `hexakit genesis init` ships → link from README
