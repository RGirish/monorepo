"""Main entry point for the Jarvis CLI."""

import sys

from src.agent.callbacks import StreamingCallbackHandler
from src.agent.factory import AgentCreationError, create_agent
from src.cli.repl import run_interactive_loop
from src.ui.console import print_assistant_prefix, print_greeting
from src.ui.spinner import Spinner


def main() -> int:
    """Main entry point for the jarvis CLI command.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    print_greeting()

    spinner = Spinner()
    callback_handler = StreamingCallbackHandler(
        spinner=spinner,
        on_first_token=print_assistant_prefix,
    )

    try:
        agent = create_agent(callback_handler=callback_handler)
    except AgentCreationError as e:
        print(f"Error: {e}")
        return 1

    try:
        run_interactive_loop(agent, spinner, callback_handler)
    finally:
        agent.cleanup()
    return 0


if __name__ == "__main__":
    sys.exit(main())
