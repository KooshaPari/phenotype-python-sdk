# SSOT — AgentMCP (merged into McpKit)

## State
- Merged into: McpKit/python/agentmcp/
- Merge date: 2026-06-08
- Original repo: AgentMCP (archived)
- Status: active within McpKit

## Architecture
- Hexagonal: yes
- Ports: McpServerPort, ResourcePort
- Adapters: FastMcpAdapter, CliAdapter
- Domain: Agent, McpTool, McpResource, AgentEngine

## Next Steps
1. [ ] Integrate with McpKit registry.yaml
2. [ ] Add MCP server tool registration from registry
3. [ ] Connect to PhenoMCP submodule for shared server logic
