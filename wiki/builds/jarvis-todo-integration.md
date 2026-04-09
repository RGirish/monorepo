# Jarvis TODO Integration

**Built in:** [Week 4](../weeks/week-04-2026-01-26.md)
**Code:** [commit 61727d1](https://github.com/RGirish/monorepo/commit/61727d1339f0d8d30def120ef9d8de3167a103ce)

---

## What It Is

An extension to the [Jarvis chatbot](jarvis-chatbot.md) that connects it to the [TODO MCP server](todo-mcp-server.md) built in week 2. Jarvis can now create, list, and complete todo items during conversations by calling the MCP server's tools.

## What Changed

This build demonstrates Jarvis acting as an **MCP client** — consuming tools exposed by an external MCP server. The change involved:
1. Configuring Jarvis to connect to the running TODO MCP server
2. Making the MCP tools available within Jarvis's tool registry
3. Testing the end-to-end flow: conversational input → tool call → MCP server → response

## Why This Matters

This completes the MCP pattern first introduced in week 2:
- **Week 2:** Built the MCP server (tool producer)
- **Week 4:** Connected an agent to consume those tools (tool consumer)

It validates that the MCP server works correctly when called by a real agent in a realistic conversation, not just a test client. It also shows that MCP servers written for one use case can be reused across different agent systems.

## Related Concepts

- [Model Context Protocol](../concepts/model-context-protocol.md) — the protocol this integration uses
- [Jarvis System](../concepts/jarvis-system.md) — the full multi-week Jarvis build arc
