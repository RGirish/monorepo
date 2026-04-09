# OpenClaw — Sandboxed AI Coding

**Link:** [openclaw.ai](https://openclaw.ai/) · [Docker Blog: Run OpenClaw Securely](https://www.docker.com/blog/run-openclaw-securely-in-docker-sandboxes/)
**Covered in:** [Week 9](../weeks/week-09-2026-03-02.md)

---

## What It Is

OpenClaw is an AI coding tool that runs inside Docker containers to provide secure, isolated code execution. The core problem it solves is that AI agents that can write and execute code pose a real security risk if run with unrestricted host access — they can modify system files, make network requests, or consume excessive resources. OpenClaw addresses this by running each agent session inside a sandboxed container.

## Security Architecture

The Docker blog post outlines the sandboxing approach:
- Each AI coding session gets a **dedicated, ephemeral container** with no host filesystem access
- **Network egress** is controlled — the agent can't make arbitrary outbound requests
- **Resource limits** prevent runaway compute or memory usage
- **Session isolation** ensures different sessions can't interfere with each other

## Why This Matters

Sandboxing AI code execution is increasingly important as agents become more capable:
- Reduces the blast radius of mistakes (the agent can only break its container)
- Enables running untrusted or LLM-generated code safely
- Provides an audit trail of what the agent did within the sandbox

## Relationship to Broader Trends

OpenClaw represents a security-first approach to agentic coding. As AI agents get more autonomous (see [Ralph](ralph.md), [Strands Agents](strands-agents.md)), the question of what privileges they should have becomes critical. Container sandboxing is one architectural answer.

## Related Concepts

- [Agent Protocols](../concepts/agent-protocols.md) — protocol-level approaches to structuring agent behavior
