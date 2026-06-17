# TestingKit reconcile (2026-06-17)

Archived source: `KooshaPari/TestingKit`.
Canonical home: `phenotype-python-sdk` (`packages/testing-kit/`).

## Blob compare (gh api, 2026-06-17)

Full-tree comparison between `KooshaPari/TestingKit` and `packages/testing-kit/` on SDK `main` found **34 divergent blobs** (387/422 archive paths matched). Breakdown:

| Category | Count | Action |
|----------|------:|--------|
| `python/mcp-qa/` | 23 | Synced from archive (this PR) |
| Other Python packages | 11 | SDK canonical — post-absorption fixes, no sync |
| SDK-only artifacts | 73 | `__pycache__/*.pyc` and other SDK-local files (ignored) |
| Archive-only | 1 | Absorbed elsewhere or obsolete |

## mcp-qa: synced from archive (23 files)

Archive is source of truth for absorption. These modules were copied into the SDK on branch `fix/testing-kit-mcp-qa-reconcile`; post-sync blob compare confirms **250/250** `python/mcp-qa/` blobs match.

- `src/mcp_qa/collaboration/coordinator.py`
- `src/mcp_qa/collaboration/models.py`
- `src/mcp_qa/core/optimization_batching.py`
- `src/mcp_qa/core/optimization_pool.py`
- `src/mcp_qa/core/base/_progress.py`
- `src/mcp_qa/core/base/test_runner.py`
- `src/mcp_qa/oauth/__init__.py`
- `src/mcp_qa/oauth/auth_session.py`
- `src/mcp_qa/oauth/session_oauth_broker.py`
- `src/mcp_qa/pytest_plugins/__init__.py`
- `src/mcp_qa/reporters/console.py`
- `src/mcp_qa/reporters/test_basic.py`
- `src/mcp_qa/testing/__init__.py`
- `src/mcp_qa/testing/tdd_test_runner.py`
- `src/mcp_qa/tui/__init__.py`
- `src/mcp_qa/tui/dashboard_config.py`
- `src/mcp_qa/tui/dashboard_execution.py`
- `src/mcp_qa/tui/dashboard_handlers.py`
- `src/mcp_qa/tui/dashboard_widgets.py`
- `src/mcp_qa/tui/dashboard.py`
- `src/mcp_qa/tui/tui_enhanced.py`
- `src/mcp_qa/tui/components/status_panel.py`
- `src/mcp_qa/ui/rich_tui.py`

## Other packages: SDK canonical (11 files)

These divergences are intentional SDK-side fixes (lint, typing, logging). **Do not sync from archive.**

- `python/pheno-analysis-cli/src/pheno_analysis_cli/cli.py`
- `python/pheno-quality-cli/src/pheno_quality/cli/main.py`
- `python/pheno-quality-cli/src/pheno_quality/tools/atlas_health.py`
- `python/pheno-quality-cli/src/pheno_quality/tools/code_smell_detector.py`
- `python/pheno-quality-cli/tests/test_quality.py`
- `python/pheno-quality-tools/src/pheno_quality_tools/cli.py`
- `python/pheno-quality-tools/src/pheno_quality_tools/export_import.py`
- `python/pheno-quality-tools/src/pheno_quality_tools/integration.py`
- `python/pheno-testing-cli/src/pheno_testing_cli/cli.py`
- `python/pheno-testing-cli/src/pheno_testing_cli/package_tester.py`
- `python/qa-kit/qa_kit_logging.py`

## Archive retirement

After `phenotype-registry` marks TestingKit retired and dependents are repointed, the archived `KooshaPari/TestingKit` repository may be deleted.
