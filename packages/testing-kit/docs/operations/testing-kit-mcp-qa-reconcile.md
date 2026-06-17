# TestingKit mcp-qa reconcile (2026-06-17)

Archived source: `KooshaPari/TestingKit` (`python/mcp-qa/`).
Canonical home: `phenotype-python-sdk` (`packages/testing-kit/python/mcp-qa/`).

## Reconcile action

Synced **23 Python modules** from the archived TestingKit tree into the SDK. GitHub blob SHA comparison (`gh api` on `main`) confirmed archive and SDK diverged on these paths; archive is source of truth for the absorption.

## Files synced from archive

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

All other `mcp-qa` Python files already matched byte-for-byte between archive and SDK.

## Archive retirement

After `phenotype-registry` marks TestingKit retired and dependents are repointed, the archived `KooshaPari/TestingKit` repository may be deleted.
