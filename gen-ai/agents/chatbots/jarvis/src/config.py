"""Configuration management for Jarvis."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class OllamaConfig:
    """Ollama model configuration."""

    host: str = "http://localhost:11434"
    model_id: str = "mistral:7b"

    @classmethod
    def from_env(cls) -> OllamaConfig:
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv("JARVIS_OLLAMA_HOST", cls.host),
            model_id=os.getenv("JARVIS_MODEL_ID", cls.model_id),
        )


@dataclass(frozen=True)
class UIConfig:
    """UI-related configuration."""

    exit_commands: Tuple[str, ...] = ("exit", "quit", "bye", "q")
    spinner_interval: float = 0.1
    user_prompt: str = "You: "
    assistant_name: str = "Jarvis"
    greeting: str = "Hey there! I'm Jarvis. How can I help you?"


@dataclass(frozen=True)
class JarvisConfig:
    """Main application configuration."""

    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    ui: UIConfig = field(default_factory=UIConfig)

    @classmethod
    def from_env(cls) -> JarvisConfig:
        """Create full configuration from environment."""
        return cls(
            ollama=OllamaConfig.from_env(),
            ui=UIConfig(),
        )


_config: JarvisConfig | None = None


def get_config() -> JarvisConfig:
    """Get or create the global configuration."""
    global _config
    if _config is None:
        _config = JarvisConfig.from_env()
    return _config


def reset_config() -> None:
    """Reset the global configuration (useful for testing)."""
    global _config
    _config = None
