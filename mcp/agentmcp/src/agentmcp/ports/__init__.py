"""Ports layer — trait definitions (input/output contracts)."""

from .server import McpServerPort
from .resource import ResourcePort

__all__ = ["McpServerPort", "ResourcePort"]
