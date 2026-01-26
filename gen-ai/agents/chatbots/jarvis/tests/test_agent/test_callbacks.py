"""Tests for callback handlers."""

from unittest.mock import MagicMock

import pytest

from src.agent.callbacks import SpinnerProtocol, StreamingCallbackHandler


class TestStreamingCallbackHandler:
    def test_stops_spinner_on_first_token(self):
        """Test that spinner is stopped when first token arrives."""
        spinner = MagicMock()
        handler = StreamingCallbackHandler(spinner=spinner)

        handler(data="Hello")

        spinner.stop.assert_called_once()

    def test_invokes_first_token_callback(self):
        """Test that first token callback is invoked."""
        callback = MagicMock()
        handler = StreamingCallbackHandler(on_first_token=callback)

        handler(data="Hello")

        callback.assert_called_once()

    def test_only_calls_first_token_once(self):
        """Test that spinner is only stopped once across multiple tokens."""
        spinner = MagicMock()
        handler = StreamingCallbackHandler(spinner=spinner)

        handler(data="Hello")
        handler(data=" world")

        assert spinner.stop.call_count == 1

    def test_reset_allows_new_first_token(self):
        """Test that reset allows first token handling again."""
        spinner = MagicMock()
        handler = StreamingCallbackHandler(spinner=spinner)

        handler(data="First")
        handler.reset()
        handler(data="Second")

        assert spinner.stop.call_count == 2

    def test_empty_data_ignored(self):
        """Test that empty data doesn't trigger first token handling."""
        spinner = MagicMock()
        handler = StreamingCallbackHandler(spinner=spinner)

        handler(data="")

        spinner.stop.assert_not_called()

    def test_no_spinner_no_error(self):
        """Test that handler works without spinner."""
        handler = StreamingCallbackHandler()

        handler(data="Hello")  # Should not raise

    def test_no_callback_no_error(self):
        """Test that handler works without first token callback."""
        handler = StreamingCallbackHandler()

        handler(data="Hello")  # Should not raise

    def test_spinner_protocol(self):
        """Test that SpinnerProtocol can be used for type checking."""

        class FakeSpinner:
            def stop(self) -> None:
                pass

        fake = FakeSpinner()
        assert isinstance(fake, SpinnerProtocol)
