"""Main entry point for the Jarvis CLI."""

import itertools
import sys
import termios
import threading
import time
import tty

from strands import Agent
from strands.models.ollama import OllamaModel

# ANSI color codes
MUTED_BLUE = '\033[38;5;67m'  # Muted blue (256-color)
RESET = '\033[0m'


class Spinner:
    """A simple CLI spinner for visual feedback."""

    def __init__(self):
        self.spinner_chars = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.running = False
        self.thread = None
        self.old_settings = None

    def start(self):
        """Start the spinner in a background thread."""
        self.running = True
        # Disable terminal echo to prevent input during spinner
        try:
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except termios.error:
            self.old_settings = None
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def _spin(self):
        """Animate the spinner."""
        while self.running:
            char = next(self.spinner_chars)
            print(f'\r{char} ', end='', flush=True)
            time.sleep(0.1)

    def stop(self):
        """Stop the spinner animation (but keep input disabled)."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.2)
        print('\r  \r', end='', flush=True)  # Clear spinner

    def restore_terminal(self):
        """Restore terminal settings and flush any buffered input."""
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            self.old_settings = None
        # Flush any input typed during spinner/streaming
        try:
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except termios.error:
            pass


class StreamingCallbackHandler:
    """Custom callback handler that properly flushes output for streaming."""

    def __init__(self, spinner: Spinner):
        self.spinner = spinner
        self.first_token = True

    def __call__(self, **kwargs):
        data = kwargs.get("data", "")

        if data:
            # Stop spinner on first token
            if self.first_token:
                self.spinner.stop()
                print(f"{MUTED_BLUE}Jarvis: ", end="", flush=True)
                self.first_token = False

            print(data, end="", flush=True)

    def reset(self):
        """Reset for next response."""
        self.first_token = True


def print_greeting():
    """Display the welcome greeting."""
    print(f"\n{MUTED_BLUE}Jarvis: Hey there! I'm Jarvis. How can I help you?{RESET}\n")


def create_agent(callback_handler) -> Agent:
    """Create and return the Ollama-backed agent."""
    try:
        ollama_model = OllamaModel(
            host="http://localhost:11434",  # Ollama server address
            model_id="mistral:7b"  # Specify which model to use
        )
        agent = Agent(
            model=ollama_model,
            callback_handler=callback_handler
        )
        return agent
    except Exception as e:
        print(f"Error connecting to Ollama: {e}")
        print("Make sure Ollama is running: ollama serve")
        sys.exit(1)


def run_interactive_loop(agent: Agent, spinner: Spinner, callback_handler: StreamingCallbackHandler) -> None:
    """Run the interactive prompt loop."""

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ('exit', 'quit', 'bye', 'q'):
                break

            if not user_input:
                continue

            print()  # Extra blank line for readability

            # Reset callback and start spinner
            callback_handler.reset()
            spinner.start()

            # Agent call - input is implicitly blocked during this
            agent(user_input)

            # Ensure spinner is stopped (in case of empty response)
            spinner.stop()
            spinner.restore_terminal()
            print(RESET)  # Reset color and newline
            print()  # Extra blank line for readability

        except KeyboardInterrupt:
            spinner.stop()
            spinner.restore_terminal()
            print(f"{RESET}\n\nInterrupted. Type 'exit' to quit or continue chatting.\n")
        except EOFError:
            spinner.restore_terminal()
            print("\nGoodbye!")
            break
        except Exception as e:
            spinner.stop()
            spinner.restore_terminal()
            print(f"{RESET}\nError: {e}\n")


def main():
    """Main entry point for the jarvis CLI command."""
    print_greeting()

    spinner = Spinner()
    callback_handler = StreamingCallbackHandler(spinner)
    agent = create_agent(callback_handler)

    run_interactive_loop(agent, spinner, callback_handler)


if __name__ == "__main__":
    main()
