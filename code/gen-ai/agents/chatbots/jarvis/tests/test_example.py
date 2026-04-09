"""Example test file demonstrating testing setup."""

from src import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ == "0.1.0"
