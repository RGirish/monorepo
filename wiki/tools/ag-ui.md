# AG-UI Protocol

**Full name:** Agent-User Interaction Protocol
**Link:** [docs.ag-ui.com](https://docs.ag-ui.com/)
**Covered in:** [Week 4](../weeks/week-04-2026-01-26.md)

---

## What It Is

AG-UI is an open protocol that standardizes how AI agents stream events and state to frontend user interfaces. It addresses the problem that every agent framework streams responses differently — making it hard to build a generic UI that works with multiple backends. AG-UI defines a common event vocabulary and state model so that a single UI implementation can work with any compliant agent.

## Core Design

AG-UI defines a set of event types that agents emit as they work:
- **Text events** — streaming tokens for chat responses
- **Tool call events** — when the agent invokes a tool (start, progress, end)
- **State events** — updates to shared application state between agent and UI
- **Lifecycle events** — run started, run completed, run failed

The UI subscribes to these events and renders them in real time, without needing to know which agent framework is producing them.

## Where It Fits

AG-UI sits at the **agent-to-UI** layer of the agent communication stack. It complements:
- [A2A Protocol](a2a-protocol.md) — handles agent-to-agent communication
- [Agent Client Protocol](agent-client-protocol.md) — handles client application requests to agents
- [Model Context Protocol](../concepts/model-context-protocol.md) — handles tool/resource access by agents

## Related Concepts

- [Agent Protocols](../concepts/agent-protocols.md) — overview of all three protocol layers
