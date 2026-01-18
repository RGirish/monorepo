"""Tools for the MCP server.
"""

from .server import mcp


@mcp.tool()
def create_todo_item(name: str, description: str) -> str:
    """Creates an item to do later.

    Args:
        name: A short name for the item.
        description: A detailed description for the item.

    Returns:
        An identifier for the to-do item just created.
    """
    return name
