# Jarvis — Personal AI Assistant System

**Appears in:** [Week 3](../weeks/week-03-2026-01-19.md) · [Week 4](../weeks/week-04-2026-01-26.md) · [Week 5](../weeks/week-05-2026-02-02.md)

---

## Overview

Jarvis is a personal AI assistant built and extended incrementally across three weeks. It started as a basic local chatbot and was progressively enhanced with tool access (via MCP) and agent-network participation (via A2A). The Jarvis build arc is a concrete example of how a real-world agent system is assembled from standard components.

---

## Evolution by Week

### Week 3 — Initial Chatbot

**Built:** [Jarvis Chatbot](../builds/jarvis-chatbot.md)

Starting point: a personal AI chatbot built with [Strands Agents](../tools/strands-agents.md) and [Ollama](../tools/ollama.md) for local model inference. Capabilities at this point:
- Multi-turn conversational AI
- Tool calling framework (tools defined, but none connected yet)
- Fully local — no external API keys or network calls

### Week 4 — MCP Tool Access

**Built:** [Jarvis TODO Integration](../builds/jarvis-todo-integration.md)

Connected Jarvis to the [TODO MCP server](../builds/todo-mcp-server.md) built in week 2. Jarvis now acts as an MCP client, consuming external tools through the standardized protocol. New capabilities:
- Create, list, and complete todo items during conversation
- Demonstrated full MCP client/server pattern end-to-end

### Week 5 — A2A Protocol Server

**Built:** [Jarvis A2A Server](../builds/jarvis-a2a-server.md)

Added an A2A protocol server to Jarvis, making it discoverable and callable by other agents. New capabilities:
- Serves an Agent Card for capability discovery
- Accepts tasks from A2A clients
- Streams task progress and returns results

---

## Architecture Summary (End of Week 5)

```
                    ┌──────────────────────────────┐
Other Agents ──────►│  Jarvis                       │
  (via A2A)         │                               │
                    │  ┌─────────────────────────┐  │
Client App ────────►│  │  Strands Agent Loop     │  │
                    │  │  (conversation mgmt,    │  │
                    │  │   tool dispatch)         │  │
                    │  └──────────┬──────────────┘  │
                    │             │                  │
                    │  ┌──────────▼──────────────┐  │
                    │  │  Ollama (local LLM)      │  │
                    │  └─────────────────────────┘  │
                    └──────────────┬───────────────┘
                                   │ MCP client
                                   ▼
                    ┌──────────────────────────────┐
                    │  TODO MCP Server              │
                    └──────────────────────────────┘
```

---

## Why This Arc Is Instructive

Jarvis demonstrates that a production-grade agent isn't built all at once — it's assembled incrementally by connecting standard interfaces:
1. Start with a capable model + agent loop
2. Add tool access via MCP (consume external capabilities)
3. Expose yourself via A2A (become callable by others)

Each step added a well-defined interface without changing the existing internals.

---

## Related Concepts

- [Model Context Protocol](model-context-protocol.md) — the tool-access layer added in week 4
- [Agent Protocols](agent-protocols.md) — where A2A fits in the broader protocol landscape
