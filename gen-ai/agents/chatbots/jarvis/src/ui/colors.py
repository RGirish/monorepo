"""ANSI color codes for terminal output."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Colors:
    """Terminal color codes."""

    MUTED_BLUE: str = "\033[38;5;67m"
    RESET: str = "\033[0m"
    RED: str = "\033[31m"
    GREEN: str = "\033[32m"
    YELLOW: str = "\033[33m"


COLORS = Colors()
