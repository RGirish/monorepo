# READ ME

## MBBALCP2026
*My Big Beautiful Ambitious Learning And Curiosity Plan For 2026*

Goal: One new AI topic learned and one new piece of software built, every week in 2026.

---

### Progress

| Week | Date | AI Topic | Build | Link |
|------|------|----------|-------|------|
| 01 | Jan 05 | Beads — coding agent memory system | Bloom filter | [Week 01](wiki/weeks/week-01-2026-01-05.md) |
| 02 | Jan 12 | Claude Code | TODO MCP server | [Week 02](wiki/weeks/week-02-2026-01-12.md) |
| 03 | Jan 19 | Strands Agents + Ollama | Jarvis chatbot | [Week 03](wiki/weeks/week-03-2026-01-19.md) |
| 04 | Jan 26 | AG-UI protocol | Jarvis TODO integration + two-phase commit | [Week 04](wiki/weeks/week-04-2026-01-26.md) |
| 05 | Feb 02 | A2A protocol | Jarvis A2A server | [Week 05](wiki/weeks/week-05-2026-02-02.md) |
| 06 | Feb 09 | Agent Client Protocol (ACP) | Symmetric encryption | [Week 06](wiki/weeks/week-06-2026-02-09.md) |
| 07 | Feb 16 | Embedding models + vector similarity | Vector database | [Week 07](wiki/weeks/week-07-2026-02-16.md) |
| 08 | Feb 23 | Ralph autonomous agent system | TCP three-way handshake | [Week 08](wiki/weeks/week-08-2026-02-23.md) |
| 09 | Mar 02 | OpenClaw — sandboxed AI coding | CRDT collaborative editor | [Week 09](wiki/weeks/week-09-2026-03-02.md) |
| 10 | Mar 09 | Language modeling — bigram model (makemore) | Bigram language model | [Week 10](wiki/weeks/week-10-2026-03-09.md) |
| 11 | Mar 16 | Language modeling — neural net framework (makemore) | Bigram model in PyTorch | [Week 11](wiki/weeks/week-11-2026-03-16.md) |
| 12 | Mar 23 | LLM Wiki (Karpathy) | LLM Music Producer *(in progress)* | [Week 12](wiki/weeks/week-12-2026-03-23.md) |

---

### Highlights (12 weeks in)

**Best builds:**
- [Jarvis](wiki/builds/jarvis-chatbot.md) — a personal AI assistant grown incrementally across 3 weeks, ending up with MCP tool access and an A2A server; a complete end-to-end agent system
- [CRDT Collaborative Editor](wiki/builds/crdt-collaborative-editor.md) — collision-free concurrent edits without coordination, elegant data structure design
- [Bigram Neural Net](wiki/builds/bigram-neural-net.md) — the moment count-based statistics and neural networks converge to the same answer

**Most interesting AI topics:**
- [Language Modeling fundamentals](wiki/concepts/language-modeling-fundamentals.md) — building a language model from scratch reveals how the entire LLM stack is constructed
- [Agent Protocols](wiki/concepts/agent-protocols.md) — three layers (MCP, A2A, ACP/AG-UI) converging into a standard agent communication stack

**Running themes:**
- Agent infrastructure — 7 of 12 weeks touched agent frameworks, protocols, or tooling
- Build-what-you-learn — several AI topics were immediately applied as hands-on builds (embeddings → vector DB, language modeling → bigram model, MCP → TODO server)
- Incremental systems — Jarvis and the makemore series both show how complex systems grow from simple foundations

---

### Explore

- [Wiki Index](wiki/index.md) — full internal catalog: tools, builds, concepts, synthesis
- [Tools](wiki/tools/) — one page per AI topic or tool learned
- [Builds](wiki/builds/) — one page per thing built
- [Concepts](wiki/concepts/) — cross-cutting ideas that emerged across multiple weeks
- [Code](code/) — all builds organized by domain

---

*Updated by LLM on every ingest. See [wiki/index.md](wiki/index.md) for the full internal catalog.*

--- 

*The markdown-based knowledge base in this repo is an implementation of the "LLM Wiki" idea from [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).* 
