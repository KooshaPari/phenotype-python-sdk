# ResilienceKit reconcile (2026-06-17)

Archived source: `KooshaPari/ResilienceKit`.
Canonical home: `phenotype-python-sdk` (`packages/resilience-kit/`).

## Blob compare (gh api, 2026-06-17)

GitHub tree SHA comparison on `main` found **245/247** files byte-identical. Two paths diverged:

| Archive path | SDK path |
|--------------|----------|
| `python/pheno-deploy/original_source/scripts/analyze_quality_coverage.py` | `packages/resilience-kit/python/pheno-deploy/original_source/scripts/analyze_quality_coverage.py` |
| `python/pheno-deploy/original_source/tools/release_automation.py` | `packages/resilience-kit/python/pheno-deploy/original_source/tools/release_automation.py` |

## Reconcile action: SDK canonical

**Do not sync from archive.** The SDK copies contain post-absorption syntax fixes:

- `analyze_quality_coverage.py` — archive omits the closing `}` in `"gap": {"I"}` (invalid Python); SDK keeps valid dict syntax.
- `release_automation.py` — archive places `# noqa` inside the return-type annotation; SDK keeps a valid annotation with trailing `# noqa`.

The SDK is the canonical source for these two files. All other ResilienceKit paths already match the archive byte-for-byte.

## Archive retirement

After `phenotype-registry` marks ResilienceKit retired and dependents are repointed, the archived `KooshaPari/ResilienceKit` repository may be deleted.
