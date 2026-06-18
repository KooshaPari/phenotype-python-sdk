"""Tests for port contracts."""

import pytest

from agentmcp_hex.ports import McpServerPort, ResourcePort


def test_mcp_server_port_is_abstract():
    with pytest.raises(TypeError):
        McpServerPort()


def test_resource_port_is_abstract():
    with pytest.raises(TypeError):
        ResourcePort()