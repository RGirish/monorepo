# Strands Agents

**Link:** [strandsagents.com](https://strandsagents.com/)
**Covered in:** [Week 3](../weeks/week-03-2026-01-19.md) · [Week 4](../weeks/week-04-2026-01-26.md) · [Week 19](../weeks/week-19-2026-05-11.md)

---

## What It Is

Strands Agents is a Python framework for building AI agents. It handles the core agent loop — parsing LLM responses, dispatching tool calls, managing conversation history, and feeding results back to the model — so the developer can focus on defining tools and agent behavior rather than plumbing.

## Week 3 — Initial Exploration

First explored alongside [Ollama](ollama.md) to build a locally-running personal chatbot. The key appeal of Strands was its clean Python API: define tools as decorated functions, point the agent at a model, and the framework manages the rest. The first build was [Jarvis](../builds/jarvis-chatbot.md), a personal assistant that runs entirely on local hardware.

## Week 4 — Deeper Dive + AG-UI

Returned to Strands alongside exploring the [AG-UI protocol](ag-ui.md). Went deeper into how Strands handles streaming, state management, and multi-step tool use. Also extended Jarvis to consume the [TODO MCP server](../builds/todo-mcp-server.md) as a Strands tool, demonstrating the MCP integration pattern.

## Week 19 — Evals SDK

Returned to Strands as a case study while learning [agent evaluation](agent-evaluation.md) in general — not to learn new Strands APIs for their own sake, but to check which techniques from the general theory a real framework actually implements, and to find gaps the theory hadn't covered yet.

Strands' `evals-sdk` turned out to be a fairly faithful, code-level realization of nearly the whole framework: a `Case` type that carries both `expected_output` and `expected_trajectory` as first-class fields (not output-only); rubric-based judges that mirror the decomposed-dimension, graduated-scale pattern almost verbatim; deterministic checks (`Equals`, `Contains`, `ToolCalled`, `StateEquals`) for the cheap/fast layer; and trace-based evaluation via OpenTelemetry instrumentation that doubles as the same substrate for production monitoring.

It also surfaced three techniques the general reading hadn't covered at all, which became new sections in the [agent evaluation](agent-evaluation.md) page rather than Strands-specific trivia: **red-teaming** (closed-loop adversarial attack strategies — gradual escalation, iterative refinement against judge feedback — scored against a deliberately conservative breach threshold), **chaos testing** (fault injection into tool calls, borrowed from systems engineering, with dedicated resilience evaluators for partial completion, honest failure communication, and recovery sophistication), and **simulation** (an LLM playing a user persona to generate realistic multi-turn traces, or standing in for a tool that doesn't exist yet — solving the upstream problem of how to get a trace to evaluate in the first place). A fourth capability, "Detectors" (root-cause diagnosis rather than scoring), was judged not a fully new category — same LLM-judge primitive, different output contract.

## Key Concepts

- **Tool definitions** — Python functions decorated with `@tool` that the agent can invoke
- **Agent loop** — the framework manages the LLM ↔ tool execution cycle automatically
- **Model flexibility** — works with local models (via Ollama) and remote APIs

## Related Concepts

- [Jarvis System](../concepts/jarvis-system.md) — the agent built with Strands across weeks 3–5
- [Model Context Protocol](../concepts/model-context-protocol.md) — used to connect Strands agents to MCP tool servers
- [Agent Protocols](../concepts/agent-protocols.md) — the broader ecosystem of agent communication standards
- [Agent Evaluation](agent-evaluation.md) — general theory; this page's Week 19 section is the framework-specific case study
