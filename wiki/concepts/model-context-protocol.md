# Model Context Protocol (MCP)

**Appears in:** [Week 2](../weeks/week-02-2026-01-12.md) · [Week 4](../weeks/week-04-2026-01-26.md)

---

## What It Is

MCP (Model Context Protocol) is an open standard developed by Anthropic for giving AI models structured access to tools, resources, and data sources. It defines a server/client architecture where:
- **MCP Servers** expose capabilities (tools, resources, prompts) with defined schemas
- **MCP Clients** (agents, IDEs, CLI tools) connect to servers and invoke their capabilities

The protocol handles capability discovery, input/output schema validation, and the message format for tool calls and results.

## Server/Client Pattern

```
┌─────────────────┐         MCP Protocol         ┌──────────────────┐
│   MCP Client    │◄──────────────────────────────►  MCP Server      │
│ (agent, IDE,    │   discover tools               │ (TODO server,    │
│  Claude Code)   │   call tool(name, args)        │  database,       │
│                 │   receive result               │  filesystem...)  │
└─────────────────┘                               └──────────────────┘
```

## How Tools Are Defined

Each tool has:
- **Name** — unique identifier (`add_todo`, `search_files`, etc.)
- **Description** — natural language description the model uses to decide when to call it
- **Input schema** — JSON Schema defining expected parameters
- **Return type** — what the tool returns

The model sees these definitions in its context and generates tool calls as structured JSON.

## Appearances in This Project

### Week 2: Building a Server
Built the [TODO MCP server](../builds/todo-mcp-server.md) — a server that exposes `add_todo`, `list_todos`, `complete_todo`, and `delete_todo` as AI-callable tools. This established the producer side of the pattern.

### Week 4: Consuming a Server
Connected [Jarvis](../builds/jarvis-todo-integration.md) to the TODO MCP server as an MCP client. Jarvis discovers the available tools at startup and can call them during conversations. This completed the full MCP client/server cycle.

## Key Properties

- **Framework-agnostic** — any MCP server can be consumed by any MCP client
- **Discoverable** — clients enumerate available tools at runtime, no hardcoding
- **Composable** — an agent can connect to multiple MCP servers simultaneously
- **Standardized** — tool call and result message formats are consistent across all servers

## MCP in the Broader Protocol Stack

MCP handles the **tool access** layer. It works alongside:
- [A2A Protocol](../tools/a2a-protocol.md) — agent-to-agent coordination
- [AG-UI](../tools/ag-ui.md) — streaming agent output to frontends
- [ACP](../tools/agent-client-protocol.md) — client application interface

See [Agent Protocols](agent-protocols.md) for the full picture.

## Related Builds

- [TODO MCP Server](../builds/todo-mcp-server.md) — the MCP server built in week 2
- [Jarvis TODO Integration](../builds/jarvis-todo-integration.md) — MCP client consuming that server
