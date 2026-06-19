"""Domain models for AgentMCP."""

from pydantic import BaseModel
from typing import Any


class McpTool(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]


class McpResource(BaseModel):
    uri: str
    mime_type: str
    contents: bytes


class Agent(BaseModel):
    name: str
    instructions: str
    tools: list[McpTool] = []
    resources: list[McpResource] = []
