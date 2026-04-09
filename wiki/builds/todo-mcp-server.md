# TODO MCP Server

**Built in:** [Week 2](../weeks/week-02-2026-01-12.md)
**Code:** [gen-ai/mcp/todo-mcp-server](https://github.com/RGirish/monorepo/tree/main/gen-ai/mcp/todo-mcp-server)

---

## What It Is

An MCP (Model Context Protocol) server that exposes TODO management as a set of AI-callable tools. Any MCP-compatible client — Claude Code, Jarvis, or another agent — can connect to this server and create, list, complete, and delete todo items through the standardized MCP tool interface.

## MCP Overview

MCP (Model Context Protocol) is an open standard for giving AI models access to tools, resources, and data. It defines a server/client architecture:
- **Server** — exposes capabilities as tools with defined input/output schemas
- **Client** — the AI agent or application that discovers and calls those tools

This server implements the server side of that contract for a simple todo list.

## Tools Exposed

| Tool | Description |
|------|-------------|
| `add_todo` | Create a new todo item with a title and optional description |
| `list_todos` | Return all todos, with optional filtering by status |
| `complete_todo` | Mark a todo as completed by ID |
| `delete_todo` | Remove a todo by ID |

## Why This Is Interesting

The value of an MCP server over a plain REST API is that AI agents can discover and use it without any custom integration code. Claude Code can introspect the available tools and their schemas, then call them as naturally as any other operation in a conversation.

This server was later consumed by [Jarvis](jarvis-todo-integration.md) in week 4, demonstrating that MCP servers written once can be reused across different agent clients.

## Related Concepts

- [Model Context Protocol](../concepts/model-context-protocol.md) — the protocol this server implements
- [Claude Code](../tools/claude-code.md) — an MCP client that can consume this server
