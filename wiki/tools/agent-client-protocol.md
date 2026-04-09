# Agent Client Protocol (ACP)

**Full name:** Agent Client Protocol
**Link:** [agentclientprotocol.com](https://agentclientprotocol.com/get-started/introduction)
**Covered in:** [Week 6](../weeks/week-06-2026-02-09.md)

---

## What It Is

ACP (Agent Client Protocol) defines how client applications — browsers, mobile apps, desktop tools, scripts — interact with AI agents. It standardizes the request/response format, streaming conventions, and error handling for the human-facing side of agent communication.

## Why a Separate Protocol

The agent communication landscape has three distinct interfaces, each with different requirements:

| Layer | Protocol | Who talks to whom |
|-------|----------|------------------|
| Tool access | MCP | Agent ↔ tools/resources |
| Agent-to-agent | A2A | Agent ↔ agent |
| Client-facing | ACP | Client app ↔ agent |

ACP fills the gap at the top of this stack. Without it, every agent framework exposes a different API surface for client applications, making it hard to build reusable frontend code.

## Core Design

ACP defines:
- How clients initiate agent sessions and send messages
- How agents return structured responses (text, data, artifacts)
- How streaming works for real-time response display
- Error handling and status reporting conventions

## Where It Fits

- [AG-UI Protocol](ag-ui.md) — handles the UI-side streaming events (complementary to ACP)
- [A2A Protocol](a2a-protocol.md) — handles agent-to-agent delegation

## Related Concepts

- [Agent Protocols](../concepts/agent-protocols.md) — overview of all three protocol layers
