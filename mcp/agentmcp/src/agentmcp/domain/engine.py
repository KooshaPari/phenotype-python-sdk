"""Agent execution engine (pure logic)."""

from .models import Agent, McpTool


class AgentEngine:
    def __init__(self, agent: Agent):
        self.agent = agent

    def can_handle(self, tool_name: str) -> bool:
        return any(t.name == tool_name for t in self.agent.tools)

    def list_tools(self) -> list[str]:
        return [t.name for t in self.agent.tools]

    def add_tool(self, tool: McpTool) -> None:
        self.agent.tools.append(tool)
