"""Tests for configuration module."""

import os
from unittest.mock import patch

import pytest

from src.config import (
    JarvisConfig,
    OllamaConfig,
    TodoMCPConfig,
    UIConfig,
    get_config,
    reset_config,
)


class TestOllamaConfig:
    def test_defaults(self):
        config = OllamaConfig()
        assert config.host == "http://localhost:11434"
        assert config.model_id == "mistral:7b"

    def test_from_env(self):
        with patch.dict(
            os.environ,
            {
                "JARVIS_OLLAMA_HOST": "http://custom:1234",
                "JARVIS_MODEL_ID": "llama2:13b",
            },
        ):
            config = OllamaConfig.from_env()
            assert config.host == "http://custom:1234"
            assert config.model_id == "llama2:13b"

    def test_from_env_uses_defaults_when_not_set(self):
        with patch.dict(os.environ, {}, clear=True):
            config = OllamaConfig.from_env()
            assert config.host == "http://localhost:11434"
            assert config.model_id == "mistral:7b"

    def test_immutable(self):
        config = OllamaConfig()
        with pytest.raises(Exception):
            config.host = "http://other:1234"


class TestUIConfig:
    def test_defaults(self):
        config = UIConfig()
        assert config.exit_commands == ("exit", "quit", "bye", "q")
        assert config.spinner_interval == 0.1
        assert config.user_prompt == "You: "
        assert config.assistant_name == "Jarvis"

    def test_immutable(self):
        config = UIConfig()
        with pytest.raises(Exception):
            config.user_prompt = ">> "


class TestTodoMCPConfig:
    def test_defaults(self):
        config = TodoMCPConfig()
        assert config.url == "http://127.0.0.1:8000/mcp"
        assert config.startup_timeout == 30

    def test_from_env(self):
        with patch.dict(
            os.environ,
            {
                "JARVIS_TODO_MCP_URL": "http://custom:9000/mcp",
                "JARVIS_TODO_MCP_TIMEOUT": "60",
            },
        ):
            config = TodoMCPConfig.from_env()
            assert config.url == "http://custom:9000/mcp"
            assert config.startup_timeout == 60

    def test_from_env_uses_defaults_when_not_set(self):
        with patch.dict(os.environ, {}, clear=True):
            config = TodoMCPConfig.from_env()
            assert config.url == "http://127.0.0.1:8000/mcp"
            assert config.startup_timeout == 30

    def test_immutable(self):
        config = TodoMCPConfig()
        with pytest.raises(Exception):
            config.url = "http://other:8000/mcp"


class TestJarvisConfig:
    def test_defaults(self):
        config = JarvisConfig()
        assert isinstance(config.ollama, OllamaConfig)
        assert isinstance(config.ui, UIConfig)
        assert isinstance(config.todo_mcp, TodoMCPConfig)

    def test_from_env(self):
        with patch.dict(
            os.environ,
            {
                "JARVIS_OLLAMA_HOST": "http://test:5000",
                "JARVIS_TODO_MCP_URL": "http://test:9000/mcp",
            },
        ):
            config = JarvisConfig.from_env()
            assert config.ollama.host == "http://test:5000"
            assert config.todo_mcp.url == "http://test:9000/mcp"

    def test_immutable(self):
        config = JarvisConfig()
        with pytest.raises(Exception):
            config.ollama = OllamaConfig()


class TestGetConfig:
    def setup_method(self):
        reset_config()

    def teardown_method(self):
        reset_config()

    def test_returns_config(self):
        config = get_config()
        assert isinstance(config, JarvisConfig)

    def test_returns_same_instance(self):
        config1 = get_config()
        config2 = get_config()
        assert config1 is config2

    def test_reset_config_clears_cache(self):
        config1 = get_config()
        reset_config()
        config2 = get_config()
        assert config1 is not config2
