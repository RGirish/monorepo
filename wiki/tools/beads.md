# Beads — Coding Agent Memory System

**Created by:** Steve Yegge
**Links:** [GitHub](https://github.com/steveyegge/beads) · [Introducing Beads (Medium)](https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a)
**Covered in:** [Week 1](../weeks/week-01-2026-01-05.md)

---

## What It Is

Beads is a memory system designed for AI coding agents. It addresses a fundamental limitation of current agents: they lose all context when a session ends, forcing the human to re-explain the codebase and project state at the start of every conversation. Beads provides a structured way to persist, organize, and retrieve that context across sessions.

## Core Concept: Beads as Memory Units

A "bead" is a discrete unit of structured memory — a fact, decision, code snippet, or observation that an agent considers worth remembering. Beads are stored in a persistent store and tagged in a way that allows relevant ones to be retrieved and injected into the agent's context when needed.

The design is deliberately minimal: rather than trying to summarize entire codebases (which loses detail), Beads stores specific, retrievable facts. The agent decides what to bead; the system handles storage and retrieval.

## Why It Matters

- Solves the "context amnesia" problem for long-running coding projects
- Works alongside existing coding agents (Cursor, Claude Code, etc.) rather than replacing them
- Enables agents to accumulate institutional knowledge about a codebase over time
- Relevant to any agentic system that needs memory beyond a single context window

## Related Concepts

- [Agent Client Protocol](agent-client-protocol.md) — another approach to structuring agent-client interactions
- [Ralph](ralph.md) — a separate system for structuring autonomous agent task workflows
