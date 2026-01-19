# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a TODO MCP (Model Context Protocol) server built with FastMCP. It exposes tools that can be called by MCP clients (like Claude Desktop or other AI assistants).

## Commands

```bash
# Install dependencies (use the existing venv)
source venv/bin/activate
pip install -e .

# Run the server
mcp-server
# or
python -m server.server
```

## Architecture

The server uses FastMCP to expose tools via the Model Context Protocol:

- `server/server.py` - Creates the FastMCP instance and runs the server
- `server/tools.py` - Tool definitions decorated with `@mcp.tool()`

### Adding New Tools

Tools are defined in `server/tools.py` using the `@mcp.tool()` decorator:

```python
from .server import mcp

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description shown to MCP clients.

    Args:
        param: Parameter description.

    Returns:
        What the tool returns.
    """
    return result
```

The docstring becomes the tool's description in the MCP protocol.
