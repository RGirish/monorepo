"""Console output utilities for Jarvis."""

from src.config import get_config
from src.ui.colors import COLORS


def print_greeting() -> None:
    """Display the welcome greeting."""
    config = get_config()
    print(
        f"\n{COLORS.MUTED_BLUE}{config.ui.assistant_name}: "
        f"{config.ui.greeting}{COLORS.RESET}\n"
    )


def print_assistant_prefix() -> None:
    """Print the assistant name prefix for responses."""
    config = get_config()
    print(f"{COLORS.MUTED_BLUE}{config.ui.assistant_name}: ", end="", flush=True)


def print_error(message: str) -> None:
    """Print an error message in red.

    Args:
        message: The error message to display.
    """
    print(f"{COLORS.RED}Error: {message}{COLORS.RESET}")


def reset_output() -> None:
    """Reset terminal colors and add spacing."""
    print(f"{COLORS.RESET}")
