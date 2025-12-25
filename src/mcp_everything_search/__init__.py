"""
Everything MCP Server
An MCP server that provides file search capabilities using Everything (voidtools)
"""

__version__ = "0.2.1"

from .server import mcp, main

__all__ = ["mcp", "main"]
