# MCP-QA Testing Framework

**Version:** 1.0.0

A comprehensive, enterprise-grade testing framework for Model Context Protocol (MCP) implementations. This framework provides automated testing capabilities, OAuth flow simulation, multi-client support, and detailed reporting for MCP servers and clients.

## Overview

The MCP-QA Testing Framework is a standalone testing solution designed for universal MCP testing. It provides:

- **Base Test Runner** - Parallel/sequential test execution with caching and progress tracking
- **Base Client Adapter** - Abstraction for MCP client interactions with error handling
- **OAuth/Auth Management** - Credential brokering, caching, and multi-provider support (GitHub, Google, Microsoft, Auth0)
- **Reporters** - Console, JSON, HTML, and markdown output formats with rich visualizations
- **Fast HTTP Client** - High-performance HTTP client with retries and connection pooling
- **TUI Components** - Rich terminal UI for test dashboards and real-time progress display
- **Mocking & Fixtures** - Comprehensive test data generation and mock server utilities
- **Pytest Integration** - Full pytest plugin with markers, fixtures, and configuration

## Installation

```bash
# Install from PyPI
pip install mcp-qa

# Or install with development dependencies
pip install mcp-qa[dev]

# Or install from source
pip install -e .
```

## Quick Start

### 1. Create a Client Adapter

Your project needs to implement a client adapter that handles MCP tool calls:

```python
from mcp_qa import BaseClientAdapter
import json

class MyProjectClientAdapter(BaseClientAdapter):
    """Adapter for MyProject MCP server."""

    def __init__(self, client, verbose_on_fail=False):
        super().__init__(client, verbose_on_fail)
        self.endpoint = client.mcp_url  # Store endpoint for reports

    def _process_result(self, result, tool_name, params):
        """Transform FastMCP result to project format."""
        # Handle FastMCP result format
        if hasattr(result, 'content'):
            # Extract content from FastMCP response
            content = result.content
            if isinstance(content, list) and len(content) > 0:
                # Get first text block
                return content[0].text
            return content
        return result

    def _log_error(self, error, tool_name, params):
        """Log errors in project-specific format."""
        print(f"❌ Tool call failed: {tool_name}")
        print(f"   Params: {json.dumps(params, indent=2, default=str)}")
        print(f"   Error: {error}")
```

### 2. Create a Test Runner

Extend `BaseTestRunner` to create your project's test runner:

```python
from mcp_qa import BaseTestRunner
from typing import Dict, Any

class MyProjectTestRunner(BaseTestRunner):
    """Test runner for MyProject."""

    def _get_metadata(self) -> Dict[str, Any]:
        """Return project-specific metadata for reports."""
        return {
            "endpoint": self.client_adapter.endpoint,
            "project": "myproject",
            "environment": "production"
        }

    def _get_category_order(self):
        """Define test execution order by category."""
        return ["core", "entity", "query", "integration"]
```

### 3. Write Tests Using Decorators

Use the test registry decorators to mark your test functions:

```python
from mcp_qa.core.test_registry import register_test

@register_test("core", "list_resources")
async def test_list_resources(client_adapter):
    """Test listing available resources."""
    result = await client_adapter.call_tool("list_resources", {})
    assert result is not None
    assert "resources" in result
    return {"success": True}

@register_test("entity", "create_workspace")
async def test_create_workspace(client_adapter):
    """Test workspace creation."""
    result = await client_adapter.call_tool("workspace_operation", {
        "operation": "create",
        "name": "Test Workspace",
        "description": "Created by test"
    })

    assert result.get("success") is True
    assert "workspace_id" in result
    return {"success": True}
```

### 4. Run Your Tests

```python
import asyncio
from fastmcp import FastMCP
from myproject.adapters import MyProjectClientAdapter
from myproject.test_runner import MyProjectTestRunner

async def main():
    # Connect to your MCP server
    client = FastMCP("MyProject MCP")
    await client.connect("http://localhost:8000/api/mcp")

    # Create adapter and runner
    adapter = MyProjectClientAdapter(client)
    runner = MyProjectTestRunner(
        client_adapter=adapter,
        cache=True,
        parallel=True,
        parallel_workers=4
    )

    # Run all tests
    summary = await runner.run_all()

    print(f"\n✅ Passed: {summary['passed']}")
    print(f"❌ Failed: {summary['failed']}")
    print(f"⏭️  Skipped: {summary['skipped']}")
    print(f"💾 Cached: {summary['cached']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Core Concepts

### BaseClientAdapter

Abstract base class for MCP client adapters. Your adapter must implement:

- `_process_result(result, tool_name, params)` - Transform raw MCP results
- `_log_error(error, tool_name, params)` - Project-specific error logging

**Features:**
- Automatic call statistics tracking
- Error counting and last error capture
- Call history for debugging
- Thread-safe operation

### BaseTestRunner

Abstract base class for test runners. Your runner must implement:

- `_get_metadata()` - Return project metadata for reports

**Features:**
- Parallel execution with configurable workers
- Test caching to skip passing tests
- Progress tracking with tqdm or enhanced display
- Multiple reporter support (console, JSON, markdown)
- Worker isolation with dedicated environments
- Connection pooling for performance
- Test categorization and ordering

### Test Registry

Centralized registry for organizing tests by category:

```python
from mcp_qa.core.test_registry import register_test

@register_test(category="core", tool_name="list_tools")
async def test_list_tools(client_adapter):
    """Test the list_tools endpoint."""
    result = await client_adapter.call_tool("list_tools", {})
    assert result is not None
    return {"success": True}
```

## Configuration

### Environment Variables

The framework uses environment variables for configuration:

```bash
# MCP Server Configuration
export MCP_BASE_URL="http://localhost:8000"
export MCP_ENDPOINT="http://localhost:8000/api/mcp"

# OAuth Configuration (if using OAuth)
export WORKOS_CLIENT_ID="your_client_id"
export FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL="https://your-server.com"
export FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN="https://your-authkit.app"

# Test Configuration
export TEST_PARALLEL_WORKERS="4"
export TEST_CACHE_ENABLED="true"
export TEST_TIMEOUT="60"
```

## Package Structure

```
mcp_qa/
├── __init__.py                 # Main exports
├── adapters/                   # HTTP clients and adapters
│   ├── fast_http_client.py    # High-performance HTTP client
│   └── adapters_base.py       # Base adapter classes
├── assertions/                 # Test assertion helpers
├── auth/                       # Authentication utilities
│   ├── credential_manager.py
│   ├── keychain_manager.py
│   └── pytest_fixtures.py
├── core/                       # Core framework components
│   ├── base/                  # Base classes
│   │   ├── test_runner.py    # BaseTestRunner
│   │   └── client_adapter.py # BaseClientAdapter
│   ├── test_registry.py      # Test registration
│   ├── cache.py              # Test caching
│   └── reporters.py          # Test reporting
├── execution/                  # Test execution engines
│   ├── parallel_clients.py
│   └── optimizations.py
├── fixtures/                   # Test fixtures
├── logging/                    # Logging utilities
├── mocking/                    # Mock servers and data
│   ├── server.py
│   ├── tools.py
│   └── builders.py
├── oauth/                      # OAuth integration
│   ├── credential_broker.py   # UnifiedCredentialBroker
│   └── playwright_adapter.py
├── performance/                # Performance testing
├── reporters/                  # Output formatters
│   ├── console.py            # ConsoleReporter
│   ├── json_reporter.py      # JSONReporter
│   └── markdown.py
├── testing/                    # Test utilities
└── tui/                        # Terminal UI components
```

## API Reference

### Main Exports

```python
from mcp_qa import (
    # Base classes for projects to extend
    BaseTestRunner,
    BaseClientAdapter,
    SimpleClientAdapter,
    # OAuth
    UnifiedCredentialBroker,
    CapturedCredentials,
    # Reporters
    ConsoleReporter,
    JSONReporter,
    # Adapters
    FastHTTPClient,
)
```

### Reporters

```python
from mcp_qa.reporters import (
    ConsoleReporter,      # Colorized console output
    JSONReporter,         # JSON format for CI/CD
    MarkdownReporter,     # Markdown reports
    HTMLReporter,         # HTML reports
    FunctionalityMatrixReporter,  # Feature matrix
    DetailedErrorReporter,        # Error details
    MultiReporter,                # Combine multiple reporters
)
```

### OAuth

```python
from mcp_qa.oauth import (
    UnifiedCredentialBroker,  # Multi-provider credential management
    OAuthProgressFlow,         # OAuth with progress display
    PlaywrightOAuthAdapter,    # Playwright automation
)
```

## License

MIT License - see LICENSE file for details.

## Credits

Originally developed for the Phenotype ecosystem and extracted as a standalone framework.
