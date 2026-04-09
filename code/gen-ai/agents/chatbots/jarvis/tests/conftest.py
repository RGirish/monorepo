"""Shared test fixtures."""

from unittest.mock import MagicMock

import pytest

from src.config import JarvisConfig, OllamaConfig, UIConfig, reset_config


@pytest.fixture(autouse=True)
def reset_config_fixture():
    """Reset global config before each test."""
    reset_config()
    yield
    reset_config()


@pytest.fixture
def mock_config() -> JarvisConfig:
    """Provide a test configuration."""
    return JarvisConfig(
        ollama=OllamaConfig(host="http://test:11434", model_id="test-model"),
        ui=UIConfig(),
    )


@pytest.fixture
def mock_spinner() -> MagicMock:
    """Provide a mock spinner."""
    spinner = MagicMock()
    spinner.stop = MagicMock()
    spinner.start = MagicMock()
    spinner.restore_terminal = MagicMock()
    return spinner


@pytest.fixture
def mock_agent() -> MagicMock:
    """Provide a mock agent."""
    return MagicMock()


@pytest.fixture
def mock_callback_handler() -> MagicMock:
    """Provide a mock callback handler."""
    handler = MagicMock()
    handler.reset = MagicMock()
    return handler
