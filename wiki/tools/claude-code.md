# Claude Code

**Created by:** Anthropic
**Link:** [claude.com/product/claude-code](https://claude.com/product/claude-code)
**Covered in:** [Week 2](../weeks/week-02-2026-01-12.md)

---

## What It Is

Claude Code is Anthropic's official CLI tool for AI-assisted coding. Unlike IDE plugins that provide inline suggestions, Claude Code runs in the terminal and acts as an agent: it can read and write files, run shell commands, search codebases, and call MCP servers — all within a single conversation context.

## Key Capabilities

- **File system access** — reads, writes, and creates files across the project
- **Shell execution** — runs tests, builds, scripts, and arbitrary commands
- **MCP integration** — connects to MCP servers to extend its tool surface (databases, APIs, etc.)
- **Codebase awareness** — can search and navigate large codebases to answer questions or make targeted edits
- **Agentic loops** — can execute multi-step tasks that span multiple tools and file operations

## Why It Matters

Claude Code is particularly effective for tasks that require understanding and modifying a whole system rather than a single file — refactoring, debugging across layers, implementing features end-to-end. The MCP integration means its capabilities can be extended by any MCP server, making it highly composable.

It was used throughout this project for wiki management and code generation.

## Related Concepts

- [Model Context Protocol](../concepts/model-context-protocol.md) — the tool integration protocol Claude Code uses
- [TODO MCP Server](../builds/todo-mcp-server.md) — an MCP server built to be consumed by Claude Code and similar clients
