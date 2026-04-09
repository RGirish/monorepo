"""Interactive REPL for Jarvis CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.config import get_config
from src.ui.colors import COLORS
from src.ui.console import print_error, reset_output

if TYPE_CHECKING:
    from strands import Agent

    from src.agent.callbacks import StreamingCallbackHandler
    from src.ui.spinner import Spinner


class JarvisREPL:
    """Interactive Read-Eval-Print Loop for Jarvis.

    Manages the conversation loop with proper error handling
    and terminal state management.
    """

    def __init__(
        self,
        agent: Agent,
        spinner: Spinner,
        callback_handler: StreamingCallbackHandler,
    ) -> None:
        """Initialize REPL with required components.

        Args:
            agent: The AI agent to interact with.
            spinner: Spinner for visual feedback.
            callback_handler: Handler for streaming responses.
        """
        self._agent = agent
        self._spinner = spinner
        self._callback = callback_handler
        self._config = get_config()

    def run(self) -> None:
        """Run the interactive loop until exit."""
        while True:
            try:
                if not self._process_input():
                    break
            except KeyboardInterrupt:
                self._handle_interrupt()
            except EOFError:
                self._handle_eof()
                break
            except Exception as e:
                self._handle_error(e)

    def _process_input(self) -> bool:
        """Process one round of user input.

        Returns:
            True to continue, False to exit.
        """
        user_input = input(self._config.ui.user_prompt).strip()

        if user_input.lower() in self._config.ui.exit_commands:
            print("Goodbye!")
            return False

        if not user_input:
            return True

        self._send_message(user_input)
        return True

    def _send_message(self, message: str) -> None:
        """Send a message to the agent and display response.

        Args:
            message: The user's message to send.
        """
        print()  # Spacing before response

        self._callback.reset()
        self._spinner.start()

        try:
            self._agent(message)
        finally:
            self._spinner.stop()
            self._spinner.restore_terminal()

        reset_output()
        print()  # Spacing after response

    def _handle_interrupt(self) -> None:
        """Handle Ctrl+C gracefully."""
        self._spinner.stop()
        self._spinner.restore_terminal()
        print(f"{COLORS.RESET}\n\nInterrupted. Type 'exit' to quit or continue chatting.\n")

    def _handle_eof(self) -> None:
        """Handle Ctrl+D / EOF."""
        self._spinner.restore_terminal()
        print("\nGoodbye!")

    def _handle_error(self, error: Exception) -> None:
        """Handle unexpected errors.

        Args:
            error: The exception that occurred.
        """
        self._spinner.stop()
        self._spinner.restore_terminal()
        print_error(str(error))


def run_interactive_loop(
    agent: Agent,
    spinner: Spinner,
    callback_handler: StreamingCallbackHandler,
) -> None:
    """Run the interactive REPL (convenience function).

    Args:
        agent: The AI agent to interact with.
        spinner: Spinner for visual feedback.
        callback_handler: Handler for streaming responses.
    """
    repl = JarvisREPL(agent, spinner, callback_handler)
    repl.run()
