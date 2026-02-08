"""A2A server entry point for Jarvis."""

from __future__ import annotations

import sys

from strands.multiagent.a2a import A2AServer

from src.agent.factory import AgentCreationError, AgentMode, create_agent
from src.config import get_config


def create_a2a_server() -> A2AServer:
    """Create and configure the A2A server.

    Returns:
        Configured A2AServer instance.

    Raises:
        AgentCreationError: If agent creation fails.
    """
    config = get_config()

    # Create agent in A2A mode (no callback handler, includes name/description)
    agent = create_agent(mode=AgentMode.A2A, config=config)

    # Wrap agent with A2A server
    server = A2AServer(
        agent=agent,
        host=config.a2a.host,
        port=config.a2a.port,
        version=config.a2a.version,
    )

    return server


def main() -> int:
    """Main entry point for the jarvis-server command.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    config = get_config()

    print(f"Starting Jarvis A2A Server...")
    print(f"  Host: {config.a2a.host}")
    print(f"  Port: {config.a2a.port}")
    print(f"  Agent: {config.a2a.agent_name}")
    print()

    try:
        server = create_a2a_server()
    except AgentCreationError as e:
        print(f"Error: {e}")
        return 1

    try:
        # serve() blocks until server is stopped
        server.serve()
    except KeyboardInterrupt:
        print("\nShutting down...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
