"""Utilities for working with JSONL files."""

import json
import os


def read_jsonl(file_path: str) -> list[dict]:
    """Reads a JSONL file and returns a list of JSON objects.

    Args:
        file_path: The path to the JSONL file.

    Returns:
        A list of dictionaries. Returns empty list if file doesn't exist.
    """
    if not os.path.exists(file_path):
        return []

    items = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def write_jsonl(items: list[dict], file_path: str) -> None:
    """Writes an array of JSON objects to a JSONL file.

    Args:
        items: A list of dictionaries to write.
        file_path: The path to the JSONL file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def append_jsonl(item: dict, file_path: str) -> None:
    """Appends a single JSON object to a JSONL file.

    Args:
        item: A dictionary to append.
        file_path: The path to the JSONL file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "a") as f:
        f.write(json.dumps(item) + "\n")
