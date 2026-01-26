"""UI module for Jarvis CLI."""

from src.ui.colors import COLORS
from src.ui.console import print_assistant_prefix, print_error, print_greeting, reset_output
from src.ui.spinner import Spinner

__all__ = [
    "COLORS",
    "Spinner",
    "print_assistant_prefix",
    "print_error",
    "print_greeting",
    "reset_output",
]
