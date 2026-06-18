# agentmcp-hex

Agentic Model Context Protocol framework — **hexagonal DDD adapter layer**
for the Phenotype ecosystem.

This package provides a clean, framework-agnostic core for building MCP-aware
agent applications, organized as a Ports & Adapters (hexagonal) Domain-Driven
Design layout. The domain logic has no framework dependencies; MCP server
exposure, CLI shells, and other transport concerns are isolated in pluggable
adapters behind well-defined port interfaces.

## Architecture

```
agentmcp_hex/
├── domain/     # Pure logic — Agent, McpTool, McpResource, AgentEngine
├── ports/      # Trait contracts — McpServerPort, ResourcePort
├── adapters/   # Concrete impls — FastMcpAdapter, CliAdapter
└── app/        # Composition root — App wires adapters to domain
```

| Layer | Depends on | May NOT depend on |
|-------|-----------|-------------------|
| `domain/` | stdlib + pydantic | any framework / adapter / port |
| `ports/` | stdlib + abc | adapters / domain / app |
| `adapters/` | ports + domain + framework (e.g. fastmcp) | app |
| `app/` | everything | — |

This matches the hexagonal pattern described in the McpKit absorption audit
(the "cleanest code in the repo" — out-of-domain hexagonal adapter pattern).

## Public API

### Domain

```python
from agentmcp_hex.domain import Agent, McpTool, McpResource, AgentEngine
```

- `Agent(name, instructions, tools=[], resources=[])` — pydantic model of an agent.
- `McpTool(name, description, parameters)` — pydantic tool descriptor.
- `McpResource(uri, mime_type, contents)` — pydantic resource descriptor.
- `AgentEngine(agent)` — pure-logic engine with `can_handle`, `list_tools`, `add_tool`.

### Ports (abstract contracts)

```python
from agentmcp_hex.ports import McpServerPort, ResourcePort
```

- `McpServerPort` — `start()`, `register_tool(name, handler)`, `register_resource(uri, handler)`.
- `ResourcePort` — `fetch(uri)`, `list()`.

### Adapters (concrete implementations)

```python
from agentmcp_hex.adapters import FastMcpAdapter, CliAdapter
```

- `FastMcpAdapter(agent)` — exposes an agent as an MCP server via the
  [`fastmcp`](https://pypi.org/project/fastmcp/) library.
- `CliAdapter(engine)` — interactive REPL shell for an `AgentEngine`.

### App (composition root)

```python
from agentmcp_hex.app import App
```

- `App(agent)` — wires an `AgentEngine`, a `FastMcpAdapter`, and a `CliAdapter`.
  - `App.run_server()` — starts the MCP server (blocking).
  - `App.run_cli()` — starts the interactive shell (blocking).

## Quickstart

```python
from agentmcp_hex.domain import Agent, McpTool
from agentmcp_hex.app import App

agent = Agent(
    name="my-agent",
    instructions="Be helpful and concise.",
    tools=[McpTool(name="echo", description="echo input", parameters={})],
)
app = App(agent)
app.run_cli()        # or app.run_server()
```

To plug in a different MCP transport (e.g. a custom HTTP server, a Stdio
bridge, a remote MCP proxy), implement `McpServerPort` and pass it to `App`
or instantiate it directly:

```python
from agentmcp_hex.domain import Agent
from agentmcp_hex.ports import McpServerPort

class MyServer(McpServerPort):
    def __init__(self, agent): ...
    def start(self): ...
    def register_tool(self, name, handler): ...
    def register_resource(self, uri, handler): ...

server = MyServer(Agent(name="x", instructions="y"))
server.register_tool("hello", lambda: "world")
server.start()
```

## Installation

This package lives in the `phenotype-python-sdk` monorepo. From the SDK root:

```bash
uv sync
```

This installs all workspace members including `agentmcp-hex`. To work on this
package in isolation:

```bash
cd packages/agentmcp-hex
pip install -e ".[dev]"
```

## Development

```bash
# from this package directory
pytest tests -v
ruff check src tests
ruff format --check src tests
mypy src
```

## Origin

Extracted from `KooshaPari/McpKit` (archived 2026-06-17) per the McpKit
absorption audit (L5-099 in `findings/2026-06-17-L5-099-mcpkit-absorption.md`).
The package originally lived at `McpKit/python/agentmcp/`. The documented
supersession path in `PhenoFastMCP/FORK-NOTES.md:121` referenced a future
`python/pheno/` layer that did not yet exist; this package is the
realization of that intent, taking the cleaner hexagonal-DDD code rather
than the older McpKit internal abstractions.

See [`ORIGIN.md`](./ORIGIN.md) for the full extraction provenance and
[`CHANGELOG.md`](./CHANGELOG.md) for release history.

## License

MIT — see the parent [`LICENSE`](../../LICENSE).