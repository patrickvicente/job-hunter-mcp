"""
MCP Module

This module contains the Model Context Protocol (MCP) server implementation
and all related tools, schemas, and metadata.
"""

from .server import mcp_server, mcp
from .metadata import get_tools_metadata, get_tool_metadata

__all__ = ['mcp_server', 'mcp', 'get_tools_metadata', 'get_tool_metadata']
