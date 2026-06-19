# AgentMCP

Agentic Model Context Protocol framework for the Phenotype ecosystem.

**Merged into McpKit** — this package now lives under `McpKit/python/agentmcp/`.

## Structure

- `domain/` — Agent, McpTool, McpResource, AgentEngine
- `ports/` — McpServerPort, ResourcePort (trait contracts)
- `adapters/` — FastMcpAdapter, CliAdapter
- `app/` — Composition root

## Usage

```python
from agentmcp.domain import Agent, McpTool
from agentmcp.app import App

agent = Agent(name="my-agent", instructions="Be helpful")
app = App(agent)
app.run_cli()
```

## License

MIT / Apache-2.0
