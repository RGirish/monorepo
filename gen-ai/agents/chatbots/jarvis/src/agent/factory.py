"""Factory functions for creating Jarvis agents."""

from __future__ import annotations

from typing import Callable, Optional

from strands import Agent
from strands.models.ollama import OllamaModel

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
    model = create_ollama_model(config)

    agent = Agent(
        model=model,
        callback_handler=callback_handler,
    )
    return agent
