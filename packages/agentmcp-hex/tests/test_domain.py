"""Unit tests for AgentMCP domain."""

from agentmcp_hex.domain import Agent, AgentEngine, McpTool


def test_agent_can_handle_tool():
    agent = Agent(
        name="test",
        instructions="test",
        tools=[McpTool(name="echo", description="echo", parameters={})],
    )
    engine = AgentEngine(agent)
    assert engine.can_handle("echo") is True
    assert engine.can_handle("missing") is False


def test_engine_list_tools():
    agent = Agent(
        name="test",
        instructions="test",
        tools=[
            McpTool(name="a", description="a", parameters={}),
            McpTool(name="b", description="b", parameters={}),
        ],
    )
    engine = AgentEngine(agent)
    assert engine.list_tools() == ["a", "b"]


def test_engine_add_tool():
    agent = Agent(name="test", instructions="test")
    engine = AgentEngine(agent)
    engine.add_tool(McpTool(name="new", description="new", parameters={}))
    assert engine.can_handle("new") is True