# Strands Agents

**Link:** [strandsagents.com](https://strandsagents.com/)
**Covered in:** [Week 3](../weeks/week-03-2026-01-19.md) · [Week 4](../weeks/week-04-2026-01-26.md)

---

## What It Is

Strands Agents is a Python framework for building AI agents. It handles the core agent loop — parsing LLM responses, dispatching tool calls, managing conversation history, and feeding results back to the model — so the developer can focus on defining tools and agent behavior rather than plumbing.

## Week 3 — Initial Exploration

First explored alongside [Ollama](ollama.md) to build a locally-running personal chatbot. The key appeal of Strands was its clean Python API: define tools as decorated functions, point the agent at a model, and the framework manages the rest. The first build was [Jarvis](../builds/jarvis-chatbot.md), a personal assistant that runs entirely on local hardware.

## Week 4 — Deeper Dive + AG-UI

Returned to Strands alongside exploring the [AG-UI protocol](ag-ui.md). Went deeper into how Strands handles streaming, state management, and multi-step tool use. Also extended Jarvis to consume the [TODO MCP server](../builds/todo-mcp-server.md) as a Strands tool, demonstrating the MCP integration pattern.

## Key Concepts

- **Tool definitions** — Python functions decorated with `@tool` that the agent can invoke
- **Agent loop** — the framework manages the LLM ↔ tool execution cycle automatically
- **Model flexibility** — works with local models (via Ollama) and remote APIs

## Related Concepts

- [Jarvis System](../concepts/jarvis-system.md) — the agent built with Strands across weeks 3–5
- [Model Context Protocol](../concepts/model-context-protocol.md) — used to connect Strands agents to MCP tool servers
- [Agent Protocols](../concepts/agent-protocols.md) — the broader ecosystem of agent communication standards
