"""Callback handlers for agent streaming responses."""

from __future__ import annotations

from typing import Any, Callable, Optional, Protocol, runtime_checkable


@runtime_checkable
class SpinnerProtocol(Protocol):
    """Protocol for spinner-like objects."""

    def stop(self) -> None:
        """Stop the spinner."""
        ...


class StreamingCallbackHandler:
    """Callback handler for streaming model responses.

    Handles the transition from spinner to streamed output on first token.

    Args:
        spinner: Object that can be stopped when streaming begins.
        on_first_token: Callback invoked on first token received.
    """

    def __init__(
        self,
        spinner: Optional[SpinnerProtocol] = None,
        on_first_token: Optional[Callable[[], None]] = None,
    ) -> None:
        """Initialize the callback handler.

        Args:
            spinner: Optional spinner to stop when first token arrives.
            on_first_token: Optional callback to invoke on first token.
        """
        self._spinner = spinner
        self._on_first_token = on_first_token
        self._first_token = True

    def __call__(self, **kwargs: Any) -> None:
        """Handle streaming callback from agent.

        Args:
            **kwargs: Callback data, expects 'data' key with token content.
        """
        data = kwargs.get("data", "")

        if data:
            if self._first_token:
                self._handle_first_token()
            print(data, end="", flush=True)

    def reset(self) -> None:
        """Reset handler state for next response."""
        self._first_token = True

    def _handle_first_token(self) -> None:
        """Handle first token - stop spinner, invoke callback."""
        if self._spinner:
            self._spinner.stop()
        if self._on_first_token:
            self._on_first_token()
        self._first_token = False
