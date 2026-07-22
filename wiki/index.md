# Wiki Index

Internal navigation catalog. Every wiki page listed with a relative link and one-line summary.

---

## Weeks

- [Week 01 — Jan 05](weeks/week-01-2026-01-05.md) — Beads coding agent memory system + bloom filter
- [Week 02 — Jan 12](weeks/week-02-2026-01-12.md) — Claude Code + TODO MCP server
- [Week 03 — Jan 19](weeks/week-03-2026-01-19.md) — Strands Agents + Ollama + Jarvis chatbot
- [Week 04 — Jan 26](weeks/week-04-2026-01-26.md) — AG-UI protocol + Jarvis TODO integration + two-phase commit
- [Week 05 — Feb 02](weeks/week-05-2026-02-02.md) — A2A protocol + Jarvis A2A server
- [Week 06 — Feb 09](weeks/week-06-2026-02-09.md) — Agent Client Protocol (ACP) + symmetric encryption
- [Week 07 — Feb 16](weeks/week-07-2026-02-16.md) — Embedding models + vector database
- [Week 08 — Feb 23](weeks/week-08-2026-02-23.md) — Ralph autonomous agent system + TCP three-way handshake
- [Week 09 — Mar 02](weeks/week-09-2026-03-02.md) — OpenClaw sandboxed AI coding + CRDT collaborative editor
- [Week 10 — Mar 09](weeks/week-10-2026-03-09.md) — Language modeling bigram model (makemore) + bigram language model
- [Week 11 — Mar 16](weeks/week-11-2026-03-16.md) — Language modeling neural net framework (makemore) + bigram neural net
- [Week 12 — Mar 23](weeks/week-12-2026-03-23.md) — LLM Wiki by Karpathy + LLM Music Producer (Base95 + MIDI-as-text)
- [Week 13 — Mar 30](weeks/week-13-2026-03-30.md) — Feature engineering + Bike Sharing Feature Pipeline (baseline, time-derived features, categorical encoding)
- [Week 14 — Apr 06](weeks/week-14-2026-04-06.md) — Multi-turn reinforcement learning + asymmetric encryption
- [Week 15 — Apr 13](weeks/week-15-2026-04-13.md) — Context engineering + Signal Protocol Chat (PQXDH, Double Ratchet)
- [Week 16 — Apr 20](weeks/week-16-2026-04-20.md) — Bike Sharing Feature Pipeline Part 2 (numeric transforms/interactions, feature selection)
- [Week 17 — Apr 27](weeks/week-17-2026-04-27.md) — Signal Protocol Chat Part 2 (real Firebase-backed networked chat)

---

## Tools

- [Beads](tools/beads.md) — Steve Yegge's coding agent memory system for persistent cross-session context
- [Claude Code](tools/claude-code.md) — Anthropic's terminal-based agentic coding CLI
- [Strands Agents](tools/strands-agents.md) — Python framework for building AI agents with tool calling
- [Ollama](tools/ollama.md) — Run LLMs locally with an OpenAI-compatible API
- [AG-UI Protocol](tools/ag-ui.md) — Standardized event protocol for streaming agent output to frontends
- [A2A Protocol](tools/a2a-protocol.md) — Open protocol for agent-to-agent task delegation and discovery
- [Agent Client Protocol](tools/agent-client-protocol.md) — Standard interface for client apps interacting with agents
- [Embedding Models](tools/embedding-models.md) — Convert text to dense vectors; cosine, dot product, and Euclidean similarity
- [Ralph](tools/ralph.md) — Geoffrey Huntley's structured autonomous agent workflow system
- [OpenClaw](tools/openclaw.md) — AI coding tool running securely inside Docker sandboxes
- [Language Modeling](tools/language-modeling.md) — Karpathy's makemore series: bigram → neural net, weeks 10–11
- [LLM Wiki](tools/llm-wiki.md) — Karpathy's comprehensive reference on LLM internals (architecture, training, inference)
- [Feature Engineering](tools/feature-engineering.md) — Transforming raw data into model-ready representations; representation learning and feature engineering in the GenAI era
- [Multi-turn Reinforcement Learning](tools/multi-turn-reinforcement-learning.md) — RL fundamentals, reward function design, RLHF pipeline, and multi-turn RL for LLMs
- [Context Engineering](tools/context-engineering.md) — Managing context as a finite resource for agents: context rot, just-in-time retrieval, compaction, sub-agents

---

## Builds

- [Bloom Filter](builds/bloom-filter.md) — Probabilistic set membership data structure with tunable false positive rate
- [TODO MCP Server](builds/todo-mcp-server.md) — MCP server exposing TODO management as AI-callable tools
- [Jarvis Chatbot](builds/jarvis-chatbot.md) — Local personal AI assistant built with Strands Agents + Ollama
- [Jarvis TODO Integration](builds/jarvis-todo-integration.md) — Jarvis extended to consume the TODO MCP server
- [Two-Phase Commit](builds/two-phase-commit.md) — Distributed consensus protocol for atomic multi-node transactions
- [Jarvis A2A Server](builds/jarvis-a2a-server.md) — A2A protocol server added to Jarvis for agent-network participation
- [Symmetric Encryption](builds/symmetric-encryption.md) — Block cipher implementation with ECB, CBC, CTR modes
- [Vector Database](builds/vector-db.md) — Custom vector store with cosine and dot product similarity search
- [TCP Three-Way Handshake](builds/tcp-three-way-handshake.md) — Simulation of TCP connection establishment (SYN, SYN-ACK, ACK)
- [CRDT Collaborative Editor](builds/crdt-collaborative-editor.md) — Collaborative text editor using conflict-free replicated data types
- [Bigram Language Model](builds/bigram-language-model.md) — Count-based character bigram model trained on names dataset
- [Bigram Neural Net](builds/bigram-neural-net.md) — Same bigram model reformulated as a single-layer neural network in PyTorch
- [LLM Music Producer](builds/llm-music-producer.md) — Two LLM audio composition pipelines: Base95 frame payloads (noise output) and MIDI-as-text (musical output)
- [Asymmetric Encryption](builds/asymmetric-encryption.md) — RSA with OAEP encryption, PSS signing, four tamper/attack scenarios demonstrating each primitive
- [Bike Sharing Feature Pipeline](builds/bike-sharing-feature-pipeline.md) — Staged feature engineering on the Bike Sharing Demand dataset; baseline → time-derived/cyclical features → categorical encoding, RMSLE-measured at each stage
- [Signal Protocol Chat](builds/signal-protocol-chat.md) — Android E2E chat using the real libsignal library; PQXDH key agreement and Double Ratchet, demonstrating forward secrecy and post-compromise security
- [Bike Sharing Feature Pipeline (Part 2)](builds/bike-sharing-feature-pipeline-part-2.md) — Numeric transforms/interactions and feature-importance-based selection; isolates that one interaction term drove the pipeline's largest accuracy gain
- [Signal Protocol Chat (Part 2)](builds/signal-protocol-chat-part-2.md) — Real 2-person Android E2E chat over the internet, adding a Firebase-backed relay, persistent on-device session storage, and Firestore Security Rules as the actual access-control boundary to the Week 15 build

---

## Concepts

- [Agent Protocols](concepts/agent-protocols.md) — A2A, AG-UI, ACP: the three-layer standard for agent communication
- [Model Context Protocol](concepts/model-context-protocol.md) — MCP server/client pattern for tool access by AI agents
- [Language Modeling Fundamentals](concepts/language-modeling-fundamentals.md) — Tokenization, softmax, cross-entropy loss, the training loop
- [Jarvis System](concepts/jarvis-system.md) — Incremental build of a personal agent across weeks 3–5
- [Cryptography Fundamentals](concepts/cryptography.md) — Symmetric vs. asymmetric encryption, hybrid encryption, OAEP/PSS padding, how TLS composes both, forward secrecy/post-compromise security and KEMs
- [Tree Ensemble Mechanics](concepts/tree-ensemble-mechanics.md) — Gradient boosting internals, cross-validation, RMSLE, cyclical encoding, feature importance, interaction terms vs. axis-aligned splits, and why categorical encoding strategy is model-family-dependent

---

## Synthesis

- [Feature Stores in ML](synthesis/feature-stores.md) — What feature stores are, why they matter beyond hand-engineered features, and how they connect to embeddings and vector DBs
- [Weights vs. Embeddings vs. Features](synthesis/weights-vs-embeddings-vs-features.md) — Three distinct artifacts, what system stores each, and how they connect in a typical ML pipeline
- [Feature Store at Inference Time](synthesis/feature-store-at-inference-time.md) — Why precomputed entity features are needed at serving time and how the online store enables low-latency lookup
- [Feature Store Data Format](synthesis/feature-store-data-format.md) — What data in a feature store actually looks like: typed scalar rows, not vectors or code
- [Feature Store: Preventing Training/Serving Skew](synthesis/feature-store-training-serving-skew.md) — How precomputed results and registered transformation functions eliminate skew without storing code
- [Feature Store: Request-Time vs. Entity Features](synthesis/feature-store-request-time-vs-entity.md) — What "request-time" really means, and how on-demand features apply at both training and serving time
- [Deep Learning vs. Classical for Tabular Data](synthesis/deep-learning-vs-classical-for-tabular-data.md) — Decision guide: when classical methods (XGBoost + FE) beat deep learning on structured data, and when the gap closes
- [Feature Engineering End-to-End Architecture](synthesis/feature-engineering-end-to-end-architecture.md) — Full fraud detection pipeline: classical FE + LLM feature extraction + offline/online stores + real-time serving
