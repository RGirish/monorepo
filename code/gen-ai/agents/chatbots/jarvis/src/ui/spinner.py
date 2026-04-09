"""CLI spinner for visual feedback during async operations."""

from __future__ import annotations

import itertools
import sys
import termios
import threading
import time
import tty
from typing import Iterator, Optional, Tuple

from src.config import get_config


class Spinner:
    """A threaded CLI spinner for visual feedback.

    Manages terminal settings to prevent input echo during operation.

    Example:
        with Spinner() as spinner:
            # Long-running operation
            pass
    """

    DEFAULT_CHARS: Tuple[str, ...] = ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏")

    def __init__(self, chars: Optional[Tuple[str, ...]] = None) -> None:
        """Initialize spinner with optional custom characters.

        Args:
            chars: Tuple of characters to cycle through for animation.
        """
        self._chars: Iterator[str] = itertools.cycle(chars or self.DEFAULT_CHARS)
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._old_settings: Optional[list] = None
        self._interval = get_config().ui.spinner_interval
        self._lock = threading.Lock()
        self._needs_clear = False

    def __enter__(self) -> Spinner:
        """Context manager entry - starts spinner."""
        self.start()
        return self

    def __exit__(self, *args) -> None:
        """Context manager exit - stops and restores terminal."""
        self.stop()
        self.restore_terminal()

    def start(self) -> None:
        """Start the spinner animation in a background thread."""
        if self._running:
            return

        self._running = True
        self._needs_clear = True
        self._save_terminal_settings()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the spinner animation."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=0.5)
            self._thread = None
        with self._lock:
            if self._needs_clear:
                print("\r  \r", end="", flush=True)
                self._needs_clear = False

    def restore_terminal(self) -> None:
        """Restore terminal settings and flush buffered input."""
        if self._old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._old_settings)
            self._old_settings = None
        try:
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except termios.error:
            pass

    def _save_terminal_settings(self) -> None:
        """Save current terminal settings for later restoration."""
        try:
            self._old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        except termios.error:
            self._old_settings = None

    def _spin(self) -> None:
        """Animate the spinner (runs in background thread)."""
        while self._running:
            char = next(self._chars)
            with self._lock:
                if self._running:
                    print(f"\r{char} ", end="", flush=True)
            time.sleep(self._interval)
