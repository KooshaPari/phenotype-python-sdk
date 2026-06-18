# Changelog

All notable changes to `agentmcp-hex` are recorded here. The format is based
on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] — 2026-06-18

### Changed
- **Extracted from `KooshaPari/McpKit`** (archived 2026-06-17) into the
  `phenotype-python-sdk` monorepo under `packages/agentmcp-hex/`.
- Renamed Python import from `agentmcp` → `agentmcp_hex` to match the
  kebab-case package name and avoid collision with future
  `pheno-mcp-router` SDK bindings.
- Version bumped from `0.1.0` → `0.3.0` (skip `0.2.x` to signal the
  relocation and minor refactor).

### Refactor
- Fixed `__init__.py` docstrings (now include hexagonal layout guidance).
- Added type-only re-export ordering in `domain/__init__.py`,
  `ports/__init__.py`, `adapters/__init__.py` (alphabetical).
- Re-added `Any` import in `adapters/fastmcp.py` (was previously imported
  via star-usage of `Any` in source).
- Marked package as `py.typed` (PEP 561).

### Preserved (no behavioral change)
- All public symbols (`Agent`, `McpTool`, `McpResource`, `AgentEngine`,
  `McpServerPort`, `ResourcePort`, `FastMcpAdapter`, `CliAdapter`, `App`).
- All test cases (`test_domain.py`, `test_ports.py`) — re-imported from
  `agentmcp` to `agentmcp_hex`.
- All dependencies (`fastmcp>=0.4.0`, `pydantic>=2.0`, `structlog>=24.0`).
- Build tooling (`ruff`, `mypy`, `pytest`) — preserved with stricter
  `uv_build` backend per the `phenotype-python-sdk` workspace convention.

## [0.1.0] — 2026-06-08

### Added
- Initial release inside `KooshaPari/McpKit` at `python/agentmcp/`.
- Hexagonal layout: `domain/` (pure logic), `ports/` (abstract contracts),
  `adapters/` (concrete impls), `app/` (composition root).
- Domain models: `Agent`, `McpTool`, `McpResource`, `AgentEngine`.
- Port interfaces: `McpServerPort`, `ResourcePort`.
- Adapters: `FastMcpAdapter` (over `fastmcp>=0.4.0`), `CliAdapter`.
- Composition root: `App`.
- Test suite: `test_domain.py` (3 tests), `test_ports.py` (2 tests).
- Dependency on `fastmcp>=0.4.0`, `pydantic>=2.0`, `structlog>=24.0`.

[0.3.0]: https://github.com/KooshaPari/phenotype-python-sdk/releases/tag/agentmcp-hex-v0.3.0
[0.1.0]: https://github.com/KooshaPari/McpKit/tree/python/agentmcp