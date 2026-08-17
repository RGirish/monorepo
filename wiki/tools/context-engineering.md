# Context Engineering

**Covered in:** [Week 15](../weeks/week-15-2026-04-13.md)

**Source:** [Effective Context Engineering for AI Agents — Anthropic Engineering Blog](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

---

## What It Is

Context engineering is the discipline of deciding *what information goes into an LLM's context window, when, and in what form*. It is the natural evolution of [prompt engineering](prompt-engineering.md) — where prompt engineering focuses on crafting effective instructions for a single discrete task, context engineering addresses the full question: "what configuration of context is most likely to generate the desired model behavior?"

The distinction matters most for agents operating across multiple inference turns. For single-shot tasks, a well-crafted prompt is sufficient. For agents doing long-horizon work, the question shifts from "how do I phrase this?" to "what should the model even be aware of right now?"

---

## Key Ideas

### 1. Context Rot and Attention Budgets

LLMs get *worse* as context grows — a phenomenon called **context rot**. The root cause is the transformer's n² pairwise attention calculation: every token attends to every other token, so larger contexts strain the model's "attention budget," reducing precision for information retrieval and long-range reasoning.

Treat context as a **finite, scarce resource**. More context is not better; the goal is always the smallest set of high-signal tokens that accomplish the task.

### 2. Anatomy of Good Context

A context window contains several distinct components, each with its own failure modes:

- **System prompts** — must be specific enough to guide behavior but flexible enough to provide useful heuristics. Brittle hardcoded logic and vague high-level guidance are both failure modes.
- **Tools** — must be well-understood by the model, non-overlapping in function, self-contained, and extremely clear about intended use. A bloated toolset with ambiguous decision points creates failure modes at every choice point.
- **Examples** — curate diverse, canonical examples rather than exhaustive edge cases. Examples are "pictures worth a thousand words" for LLMs — they demonstrate the intended behavior pattern more efficiently than instructions alone.

### 3. Just-in-Time Context Retrieval

Rather than pre-loading all potentially relevant data upfront, effective agents use **just-in-time retrieval**: maintain lightweight identifiers (file paths, queries, links) and dynamically load data using tools only when needed.

This is **progressive disclosure**: agents incrementally discover relevant context through exploration, keeping only what's necessary in working memory at each step. Claude Code exemplifies this — it writes targeted database queries rather than loading full objects into context.

### 4. Long-Horizon Task Management

For tasks that exceed context window limits, three techniques manage **context pollution**:

- **Compaction** — summarize conversation history and reinitialize with compressed content. The model preserves architectural decisions and critical details while discarding redundant outputs. Requires careful prompt tuning to maximize recall first, then improve precision.
- **Structured note-taking** — agents write persistent notes *outside* the context window and retrieve them later via a memory tool. Demonstrated by Claude playing Pokémon: maintaining precise tallies and strategic objectives across thousands of steps.
- **Sub-agent architectures** — specialized sub-agents handle focused tasks with clean context windows, returning condensed summaries (typically 1,000–2,000 tokens) rather than extensive exploration data. This separates detailed search contexts from high-level synthesis.

### 5. Guiding Principle

> *Find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome.*

This single directive unifies all context engineering decisions — whether designing system prompts, curating examples, building tools, or choosing between compaction and sub-agents. When in doubt, do the simplest thing that works.

---

## Relationship to Prompt Engineering

See also [Prompt Engineering](prompt-engineering.md) for the fundamentals this section compares against.

| | Prompt Engineering | Context Engineering |
|---|---|---|
| **Scope** | Single instruction or task | Multi-turn agent sessions |
| **Primary concern** | Phrasing and instruction quality | What information exists in context at all |
| **Key challenge** | Getting the right words | Managing a finite attention budget over time |
| **Main failure mode** | Vague or ambiguous instructions | Context rot from irrelevant or redundant tokens |

Context engineering subsumes prompt engineering — system prompt design is one component of the broader context management problem.

---

## See Also

- [Claude Code](claude-code.md) — exemplifies just-in-time context retrieval at scale
- [Agent Protocols](../concepts/agent-protocols.md) — infrastructure that shapes what context agents can access
- [Ralph](ralph.md) — structured agent workflow system that manages context via explicit task decomposition
- [Open Knowledge Format](open-knowledge-format.md) — addresses the same underlying problem (agents lacking accessible context) from the storage/format side rather than the runtime-management side
- [Agent Evaluation](agent-evaluation.md) — the other half of running an agent reliably over long sessions: this page manages what's in context, that page evaluates whether the agent behaved well given it
