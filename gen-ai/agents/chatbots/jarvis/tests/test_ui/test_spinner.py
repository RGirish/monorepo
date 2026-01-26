"""Tests for spinner module."""

from unittest.mock import patch, MagicMock

import pytest

from src.ui.spinner import Spinner


class TestSpinner:
    def test_context_manager_starts_and_stops(self):
        """Test spinner works as context manager."""
        with patch.object(Spinner, "_save_terminal_settings"):
            with patch.object(Spinner, "restore_terminal"):
                with Spinner() as spinner:
                    assert spinner._running is True
                assert spinner._running is False

    def test_double_start_no_op(self):
        """Test starting twice doesn't create two threads."""
        spinner = Spinner()
        with patch.object(spinner, "_save_terminal_settings"):
            spinner.start()
            thread1 = spinner._thread
            spinner.start()
            thread2 = spinner._thread
            assert thread1 is thread2
            spinner.stop()

    def test_custom_chars(self):
        """Test custom spinner characters."""
        chars = ("a", "b", "c")
        spinner = Spinner(chars=chars)
        assert next(spinner._chars) == "a"
        assert next(spinner._chars) == "b"
        assert next(spinner._chars) == "c"
        assert next(spinner._chars) == "a"  # cycles back

    def test_stop_without_start(self):
        """Test stopping spinner that was never started doesn't raise."""
        spinner = Spinner()
        spinner.stop()  # Should not raise
        assert spinner._running is False

    def test_restore_terminal_without_saved_settings(self):
        """Test restore_terminal handles case with no saved settings."""
        with patch("src.ui.spinner.termios") as mock_termios:
            spinner = Spinner()
            spinner._old_settings = None
            spinner.restore_terminal()  # Should not raise
            # tcsetattr should not be called when no settings saved
            mock_termios.tcsetattr.assert_not_called()

    def test_default_chars(self):
        """Test default spinner characters are set."""
        spinner = Spinner()
        # Should have default braille characters
        assert spinner.DEFAULT_CHARS == (
            "⠋",
            "⠙",
            "⠹",
            "⠸",
            "⠼",
            "⠴",
            "⠦",
            "⠧",
            "⠇",
            "⠏",
        )
