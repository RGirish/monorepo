# Jarvis Chatbot

**Built in:** [Week 3](../weeks/week-03-2026-01-19.md)
**Code:** [gen-ai/agents/chatbots/jarvis](https://github.com/RGirish/monorepo/tree/main/code/gen-ai/agents/chatbots/jarvis)

---

## What It Is

Jarvis is a personal AI chatbot built with the [Strands Agents](../tools/strands-agents.md) framework, using [Ollama](../tools/ollama.md) for local model inference. It serves as a personal assistant that can hold multi-turn conversations and call tools, running entirely on local hardware without cloud API keys.

## Architecture

- **Framework:** Strands Agents handles the agent loop, tool dispatch, and conversation history
- **Model backend:** Ollama serves a local LLM (e.g., Llama or Mistral) via a local HTTP API
- **Tool interface:** Tools defined as Python functions decorated with `@tool`, automatically exposed to the model

## What Was Built in Week 3

The initial version is a bare-bones conversational assistant:
- Multi-turn conversation management
- Basic tool calling capability (foundation for later extensions)
- Fully local — no outbound API calls required

## Subsequent Extensions

Jarvis was extended across multiple weeks, making it a running project:

| Week | Extension | Build |
|------|-----------|-------|
| 4 | Connected to TODO MCP server | [Jarvis TODO Integration](jarvis-todo-integration.md) |
| 5 | Added A2A protocol server | [Jarvis A2A Server](jarvis-a2a-server.md) |

## Related Concepts

- [Jarvis System](../concepts/jarvis-system.md) — overview of the full Jarvis build arc across weeks 3–5
- [Strands Agents](../tools/strands-agents.md) — the framework Jarvis is built on
- [Model Context Protocol](../concepts/model-context-protocol.md) — used in week 4 extension
