"""Tools for the MCP server.
"""

import json
import os
from datetime import datetime

from snowflake import SnowflakeGenerator

from .server import mcp

TODO_DB_PATH = "/Users/girishraman/todos/db.jsonl"

_snowflake_gen = SnowflakeGenerator(instance=1)


@mcp.tool()
def create_todo_item(name: str, description: str) -> str:
    """Creates an item to do later.

    Args:
        name: A short name for the item.
        description: A detailed description for the item.

    Returns:
        An identifier for the to-do item just created.
    """
    item_id = str(next(_snowflake_gen))
    todo_item = {
        "id": item_id,
        "name": name,
        "description": description,
        "created_at": datetime.utcnow().isoformat(),
    }

    os.makedirs(os.path.dirname(TODO_DB_PATH), exist_ok=True)

    with open(TODO_DB_PATH, "a") as f:
        f.write(json.dumps(todo_item) + "\n")

    return item_id
