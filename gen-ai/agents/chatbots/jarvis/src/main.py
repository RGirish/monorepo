"""Main entry point for the Jarvis CLI."""

import argparse

from strands import Agent
from strands.models.ollama import OllamaModel


def main():
    """Main entry point for the jarvis CLI command."""
    parser = argparse.ArgumentParser(
        prog="jarvis",
        description="Jarvis - A Python CLI application",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    print("Hello from Jarvis!")

    # Create an Ollama model instance
    ollama_model = OllamaModel(
        host="http://localhost:11434",  # Ollama server address
        model_id="mistral:7b"  # Specify which model to use
    )

    # Create an agent using the Ollama model
    agent = Agent(model=ollama_model)

    # Use the agent
    agent("Tell me about Strands agents.")


if __name__ == "__main__":
    main()
