"""
Pytest plugins for mcp-qa.
"""

from mcp_qa.pytest_plugins import auth_plugin
from mcp_qa.pytest_plugins.auth_plugin import *  # noqa: F401,F403  (re-export plugin API)

__all__ = ["auth_plugin"]
