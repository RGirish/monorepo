"""Tools for the MCP server.
"""

from datetime import UTC, datetime
from enum import Enum

from snowflake import SnowflakeGenerator

from .jsonl import append_jsonl, read_jsonl, write_jsonl
from .server import mcp


class Status(str, Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"


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
        "status": Status.ACTIVE.value,
        "created_at": datetime.now(UTC).isoformat(),
    }

    append_jsonl(todo_item, TODO_DB_PATH)

    return item_id


@mcp.tool()
def list_todo_items() -> list[dict]:
    """Lists all to-do items.

    Returns:
        A list of to-do items, each with id, name, description, status, and created_at.
    """
    return read_jsonl(TODO_DB_PATH)


@mcp.tool()
def delete_todo_item(item_id: str) -> bool:
    """Deletes a to-do item by its ID.

    Args:
        item_id: The ID of the to-do item to delete.

    Returns:
        True if the item was deleted, False if not found.
    """
    items = read_jsonl(TODO_DB_PATH)
    filtered = [item for item in items if item["id"] != item_id]

    if len(filtered) == len(items):
        return False

    write_jsonl(filtered, TODO_DB_PATH)

    return True


@mcp.tool()
def complete_todo_item(item_id: str) -> bool:
    """Marks a to-do item as completed.

    Args:
        item_id: The ID of the to-do item to complete.

    Returns:
        True if the item was marked as completed, False if not found.
    """
    items = read_jsonl(TODO_DB_PATH)
    found = False

    for item in items:
        if item["id"] == item_id:
            item["status"] = Status.COMPLETED.value
            found = True
            break

    if not found:
        return False

    write_jsonl(items, TODO_DB_PATH)

    return True
