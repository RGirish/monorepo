# Agent Protocols — A2A, AG-UI, ACP

**Appears in:** [Week 4](../weeks/week-04-2026-01-26.md) · [Week 5](../weeks/week-05-2026-02-02.md) · [Week 6](../weeks/week-06-2026-02-09.md)

---

## Overview

As AI agents become more capable, three distinct communication interfaces are emerging as standardization targets: how agents talk to tools, how agents talk to each other, and how agents talk to users and client applications. Three open protocols have been developed to address these layers.

## The Three Layers

```
┌─────────────────────────────────────────────┐
│              Human / Client App              │
│         ← ACP: Agent Client Protocol →      │
├─────────────────────────────────────────────┤
│                  AI Agent                    │
│          ← A2A: Agent-to-Agent →            │
├─────────────────────────────────────────────┤
│       Tools / Resources / Other Agents       │
│     ← MCP: Model Context Protocol →         │
└─────────────────────────────────────────────┘
                    ↕
             Frontend/UI Layer
      ← AG-UI: Agent-User Interaction →
```

## Protocol Summary

| Protocol | Layer | Direction | Standardizes |
|----------|-------|-----------|--------------|
| [MCP](model-context-protocol.md) | Tool access | Agent → Tools | Tool definitions, resource access, context injection |
| [A2A](../tools/a2a-protocol.md) | Agent coordination | Agent ↔ Agent | Task delegation, agent discovery, task lifecycle |
| [AG-UI](../tools/ag-ui.md) | UI streaming | Agent → UI | Event types for streaming agent output to frontends |
| [ACP](../tools/agent-client-protocol.md) | Client interface | Client → Agent | Request/response format for client applications |

## Why This Matters

Before these protocols, every agent framework exposed a different interface:
- Different tool formats (function calling schemas varied by provider)
- No standard way for one agent to call another
- No standard way for a frontend to display agent progress
- No standard way for a client app to send requests to an agent

This fragmentation made it hard to compose agents from different frameworks or build reusable frontends. The protocols solve each layer independently, allowing mix-and-match: a Strands-based agent can expose an A2A endpoint that any A2A client can call, regardless of the client's framework.

## Pattern Seen in This Project

The Jarvis agent (weeks 3–5) was built up through all layers:
- **Week 2–4:** MCP (consumed the TODO MCP server)
- **Week 5:** A2A (exposed itself as an A2A service)

This mirrors how a production agent would be designed: consume tools via MCP, be discoverable and callable via A2A, stream output via AG-UI.

## Related Concepts

- [Model Context Protocol](model-context-protocol.md) — the tool-access layer
- [Jarvis System](jarvis-system.md) — the agent that demonstrates multiple layers
