"""FastMCP adapter — implements McpServerPort via fastmcp library."""

from ..ports.server import McpServerPort
from ..domain.models import Agent


class FastMcpAdapter(McpServerPort):
    def __init__(self, agent: Agent):
        self.agent = agent
        self._tools: dict[str, Any] = {}
        self._resources: dict[str, Any] = {}

    def start(self) -> None:
        from fastmcp import FastMCP
        mcp = FastMCP(self.agent.name)
        for name, handler in self._tools.items():
            mcp.add_tool(handler, name=name)
        mcp.run()

    def register_tool(self, name: str, handler: Any) -> None:
        self._tools[name] = handler

    def register_resource(self, uri: str, handler: Any) -> None:
        self._resources[uri] = handler
