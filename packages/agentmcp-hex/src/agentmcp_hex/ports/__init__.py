"""Ports layer — trait definitions (input/output contracts)."""

from .resource import ResourcePort
from .server import McpServerPort

__all__ = ["McpServerPort", "ResourcePort"]