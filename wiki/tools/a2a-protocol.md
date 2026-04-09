# A2A Protocol

**Full name:** Agent-to-Agent Protocol
**Link:** [a2a-protocol.org](https://a2a-protocol.org/)
**Covered in:** [Week 5](../weeks/week-05-2026-02-02.md)

---

## What It Is

A2A (Agent-to-Agent) is an open protocol for enabling AI agents to communicate with, discover, and delegate tasks to each other — regardless of which framework or vendor built them. It treats each agent as a service that can be called by other agents, enabling composition of specialized agents into larger systems.

## Core Concepts

- **Agent Card** — a machine-readable description of an agent's capabilities, used for discovery
- **Task lifecycle** — standardized states: `submitted → working → completed | failed | cancelled`
- **Message passing** — structured messages with parts (text, files, data) passed between agents
- **Streaming** — agents can stream progress updates back to callers during long-running tasks

## How It Works

An A2A client discovers an agent by fetching its Agent Card (typically at `/.well-known/agent`). It submits a task with an initial message, and the agent processes it asynchronously, streaming updates and returning a final result when done.

## Where It Fits

A2A sits at the **agent-to-agent** layer. It complements:
- [AG-UI Protocol](ag-ui.md) — handles streaming from agent to frontend UI
- [Agent Client Protocol](agent-client-protocol.md) — handles human-facing client interactions
- [Model Context Protocol](../concepts/model-context-protocol.md) — handles tool/resource access within an agent

## Related Builds

- [Jarvis A2A Server](../builds/jarvis-a2a-server.md) — A2A server added to Jarvis in week 5

## Related Concepts

- [Agent Protocols](../concepts/agent-protocols.md) — overview of all three protocol layers
- [Jarvis System](../concepts/jarvis-system.md) — the agent that was exposed via A2A
