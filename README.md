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
| 12 | Mar 23 | LLM Wiki (Karpathy) | LLM Music Producer | [Week 12](wiki/weeks/week-12-2026-03-23.md) |
| 13 | Mar 30 | Feature engineering + representation learning | Bike Sharing Feature Pipeline | [Week 13](wiki/weeks/week-13-2026-03-30.md) |
| 14 | Apr 06 | Multi-turn reinforcement learning + RLHF | Asymmetric encryption | [Week 14](wiki/weeks/week-14-2026-04-06.md) |
| 15 | Apr 13 | Context engineering | Signal Protocol Chat | [Week 15](wiki/weeks/week-15-2026-04-13.md) |
| 16 | Apr 20 | *(AI topic TBD)* | Bike Sharing Feature Pipeline (Part 2) | [Week 16](wiki/weeks/week-16-2026-04-20.md) |
| 17 | Apr 27 | *(AI topic TBD)* | Signal Protocol Chat (Part 2) | [Week 17](wiki/weeks/week-17-2026-04-27.md) |
| 18 | May 04 | — | — | *(not started)* |
| 19 | May 04 | — | — | *(not started)* |
| 20 | May 11 | — | — | *(not started)* |
| 21 | May 18 | — | — | *(not started)* |
| 22 | May 25 | — | — | *(not started)* |
| 23 | Jun 01 | — | — | *(not started)* |
| 24 | Jun 08 | — | — | *(not started)* |
| 25 | Jun 15 | — | — | *(not started)* |
| 26 | Jun 22 | — | — | *(not started)* |
| 27 | Jun 29 | — | — | *(not started)* |
| 28 | Jul 06 | — | — | *(not started)* |
| 29 | Jul 13 | — | — | *(not started)* |

---

### Highlights (17 weeks in)

**Best builds:**
- [Signal Protocol Chat (Part 2)](wiki/builds/signal-protocol-chat-part-2.md) — Took Week 15's local crypto simulation onto two real phones over the actual internet: a Firebase-backed relay, persistent on-device sessions, and Firestore Security Rules as the real access-control boundary — not the Firebase API key, which isn't a secret
- [Signal Protocol Chat](wiki/builds/signal-protocol-chat.md) — E2E encrypted Android chat built on Signal's real `libsignal` library, not a reimplementation; PQXDH key agreement (with post-quantum Kyber pre-keys) and the Double Ratchet, with the UI enforcing the actual initiator/responder session asymmetry
- [LLM Music Producer](wiki/builds/llm-music-producer.md) — two complete pipelines for LLM-driven audio composition: Base95 frame payloads and MIDI-as-text; the MIDI approach produces genuinely musical output
- [Asymmetric Encryption](wiki/builds/asymmetric-encryption.md) — RSA with OAEP + PSS; four attack scenarios showing exactly what breaks and why; learned OAEP internals (seed, MGF, structural checks) deeply through build-time conversation
- [Jarvis](wiki/builds/jarvis-chatbot.md) — a personal AI assistant grown incrementally across 3 weeks, ending up with MCP tool access and an A2A server; a complete end-to-end agent system
- [CRDT Collaborative Editor](wiki/builds/crdt-collaborative-editor.md) — collision-free concurrent edits without coordination, elegant data structure design
- [Bigram Neural Net](wiki/builds/bigram-neural-net.md) — the moment count-based statistics and neural networks converge to the same answer

**Most interesting AI topics:**
- [Multi-turn Reinforcement Learning](wiki/tools/multi-turn-reinforcement-learning.md) — from RL fundamentals through RLHF to the full MTRL system architecture; reward design is where human intent meets mathematical optimization
- [LLM Wiki (Karpathy)](wiki/tools/llm-wiki.md) — a dense practitioner-oriented map of the entire LLM stack: architecture, training, inference, and emergent capabilities
- [Language Modeling fundamentals](wiki/concepts/language-modeling-fundamentals.md) — building a language model from scratch reveals how the entire LLM stack is constructed
- [Agent Protocols](wiki/concepts/agent-protocols.md) — three layers (MCP, A2A, ACP/AG-UI) converging into a standard agent communication stack

**Running themes:**
- Agent infrastructure — 7 of 14 weeks touched agent frameworks, protocols, or tooling
- Build-what-you-learn — several AI topics were immediately applied as hands-on builds (embeddings → vector DB, language modeling → bigram model, MCP → TODO server)
- Incremental systems — Jarvis and the makemore series both show how complex systems grow from simple foundations
- Representation matters — week 12 showed that MIDI (semantic) beats Base95 (statistical) for LLM audio generation; the choice of representation is the most important design decision
- ML foundations deepening — weeks 13–14 shift from AI tooling toward core ML concepts: feature engineering, the three learning paradigms, reward design; the [Bike Sharing Feature Pipeline](wiki/builds/bike-sharing-feature-pipeline.md) (week 13) and its [Part 2](wiki/builds/bike-sharing-feature-pipeline-part-2.md) (week 16) turned that theory hands-on across 5 measured stages — a counter-example to "one-hot is always correct" for tree models, and a finding that one interaction term (`workingday × is_rush_hour`) drove more accuracy than every other engineering decision in the pipeline combined, while a second, equally-plausible interaction (`temp × humidity`) turned out to be nearly worthless once checked against the data
- Security primitives deepening — weeks 6, 14, and 15 now cover the full stack: symmetric encryption, asymmetric encryption + signing, and continuous rekeying (PQXDH + Double Ratchet) for ongoing conversations, including forward secrecy and post-compromise security
- Agent infrastructure maturing — week 15 context engineering completes the picture: not just how agents communicate (protocols) but how they manage their own cognitive resources

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
