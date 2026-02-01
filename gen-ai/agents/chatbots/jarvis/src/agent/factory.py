"""Factory functions for creating Jarvis agents."""

from __future__ import annotations

from typing import Callable, Optional

from mcp.client.streamable_http import streamable_http_client
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient

from src.agent.prompts import SYSTEM_PROMPT
from src.config import JarvisConfig, get_config


class AgentCreationError(Exception):
    """Raised when agent creation fails."""
    pass


def create_ollama_model(config: Optional[JarvisConfig] = None) -> OllamaModel:
    """Create an Ollama model instance.

    Args:
        config: Configuration to use. Defaults to global config.

    Returns:
        Configured OllamaModel instance.

    Raises:
        AgentCreationError: If connection to Ollama fails.
    """
    cfg = config or get_config()

    try:
        model = OllamaModel(
            host=cfg.ollama.host,
            model_id=cfg.ollama.model_id,
        )
        return model
    except Exception as e:
        raise AgentCreationError(
            f"Could not connect to Ollama at {cfg.ollama.host}. "
            "Make sure Ollama is running: ollama serve"
        ) from e


def create_todo_mcp_client(config: Optional[JarvisConfig] = None) -> MCPClient:
    """Create TODO MCP client based on configuration.

    Args:
        config: Configuration to use. Defaults to global config.

    Returns:
        Configured MCPClient instance for the TODO MCP server,
        or None if the server is not available.
    """
    cfg = config or get_config()
    client = MCPClient(
        lambda url=cfg.todo_mcp.url: streamable_http_client(url),
        startup_timeout=cfg.todo_mcp.startup_timeout,
    )
    return client


def create_agent(
        callback_handler: Optional[Callable] = None,
        config: Optional[JarvisConfig] = None,
) -> Agent:
    """Create a fully configured Jarvis agent.

    Args:
        callback_handler: Optional callback for streaming responses.
        config: Configuration to use. Defaults to global config.

    Returns:
        Configured Agent instance.

    Raises:
        AgentCreationError: If agent creation fails.
    """
    cfg = config or get_config()
    model = create_ollama_model(cfg)

    todo_mcp_client = create_todo_mcp_client(cfg)

    agent = Agent(
        model=model,
        callback_handler=callback_handler,
        tools=[todo_mcp_client],
        system_prompt=SYSTEM_PROMPT,
    )
    return agent
