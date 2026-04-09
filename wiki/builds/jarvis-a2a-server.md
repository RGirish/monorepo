# Jarvis A2A Server

**Built in:** [Week 5](../weeks/week-05-2026-02-02.md)
**Code:** [gen-ai/agents/chatbots/jarvis/src/server/a2a.py](https://github.com/RGirish/monorepo/blob/main/gen-ai/agents/chatbots/jarvis/src/server/a2a.py)

---

## What It Is

An [A2A protocol](../tools/a2a-protocol.md) server added to the Jarvis chatbot, allowing other agents to discover Jarvis and delegate tasks to it over the standardized A2A interface. This transforms Jarvis from a standalone chatbot into a participant in a multi-agent network.

## What Was Added

The A2A server implementation handles:
- **Agent Card** — serves a machine-readable description of Jarvis's capabilities at the discovery endpoint
- **Task intake** — accepts incoming tasks from A2A clients with structured messages
- **Task lifecycle management** — tracks task state (submitted → working → completed/failed) and reports status
- **Streaming responses** — streams progress updates back to calling agents as Jarvis works

## Jarvis's Full Stack After Week 5

| Capability | How |
|------------|-----|
| Conversational AI | Strands Agents + Ollama (week 3) |
| TODO management | TODO MCP server as client (week 4) |
| Callable by other agents | A2A server (week 5) |

## Why This Is Interesting

By week 5, Jarvis is a microcosm of the full agent communication stack:
- It **consumes tools** via MCP (week 4)
- It **exposes itself** as a service via A2A (week 5)

This mirrors how production agent systems work: each agent is both a consumer of capabilities from below (tools, data) and a provider of capabilities to peers or orchestrators above.

## Related Concepts

- [Jarvis System](../concepts/jarvis-system.md) — the full Jarvis build arc
- [A2A Protocol](../tools/a2a-protocol.md) — the protocol this server implements
- [Agent Protocols](../concepts/agent-protocols.md) — where A2A fits in the layered protocol stack
