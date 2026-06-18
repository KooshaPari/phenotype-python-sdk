"""MCP server port."""

from abc import ABC, abstractmethod
from typing import Any


class McpServerPort(ABC):
    @abstractmethod
    def start(self) -> None:
        """Start the MCP server."""
        ...

    @abstractmethod
    def register_tool(self, name: str, handler: Any) -> None:
        """Register a tool handler."""
        ...

    @abstractmethod
    def register_resource(self, uri: str, handler: Any) -> None:
        """Register a resource handler."""
        ...