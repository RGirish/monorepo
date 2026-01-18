"""Main MCP server module using FastMCP."""

from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("My MCP Server")

# Import custom tools (add your tools in tools.py)
from . import tools  # noqa: F401, E402


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
