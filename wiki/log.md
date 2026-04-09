# Wiki Log

Append-only history of all wiki operations.

---

## [2026-04-08] ingest | week-01 — beads + bloom-filter
Created: weeks/week-01-2026-01-05.md, tools/beads.md, builds/bloom-filter.md
Updated: index.md, log.md
[lint] No orphans. No concept gaps yet (only 1 week ingested).

## [2026-04-08] ingest | week-02 — claude-code + todo-mcp-server
Created: weeks/week-02-2026-01-12.md, tools/claude-code.md, builds/todo-mcp-server.md
Updated: index.md, log.md
[lint] No orphans. MCP appears for the first time; watching for recurrence to create concept page.

## [2026-04-08] ingest | week-03 — strands-agents + jarvis-chatbot
Created: weeks/week-03-2026-01-19.md, tools/strands-agents.md, tools/ollama.md, builds/jarvis-chatbot.md
Updated: index.md, log.md
[lint] No orphans. Jarvis appears for the first time; watching for recurrence. No concept gaps yet.

## [2026-04-08] ingest | week-04 — ag-ui + jarvis-todo-integration + two-phase-commit
Created: weeks/week-04-2026-01-26.md, tools/ag-ui.md, builds/jarvis-todo-integration.md, builds/two-phase-commit.md, concepts/model-context-protocol.md
Updated: tools/strands-agents.md (added week 4 section), index.md, log.md
[lint] MCP concept gap detected (weeks 2 and 4 both use MCP) → created concepts/model-context-protocol.md. Added MCP links to tools/claude-code.md and builds/todo-mcp-server.md. No orphans.

## [2026-04-08] ingest | week-05 — a2a-protocol + jarvis-a2a-server
Created: weeks/week-05-2026-02-02.md, tools/a2a-protocol.md, builds/jarvis-a2a-server.md, concepts/jarvis-system.md
Updated: index.md, log.md
[lint] Jarvis concept gap detected (weeks 3, 4, 5 all build on Jarvis) → created concepts/jarvis-system.md. Cross-linked jarvis builds to jarvis-system concept. No orphans.

## [2026-04-08] ingest | week-06 — agent-client-protocol + symmetric-encryption
Created: weeks/week-06-2026-02-09.md, tools/agent-client-protocol.md, builds/symmetric-encryption.md, concepts/agent-protocols.md
Updated: index.md, log.md
[lint] Agent-protocols concept gap detected (AG-UI week 4, A2A week 5, ACP week 6 form a clear pattern) → created concepts/agent-protocols.md. Added agent-protocols links to tools/a2a-protocol.md, tools/ag-ui.md, tools/agent-client-protocol.md, builds/jarvis-a2a-server.md. No orphans.

## [2026-04-08] ingest | week-07 — embedding-models + vector-db
Created: weeks/week-07-2026-02-16.md, tools/embedding-models.md, builds/vector-db.md
Updated: index.md, log.md
[lint] No orphans. No new concept gaps. Added cross-links between embedding-models and vector-db.

## [2026-04-08] ingest | week-08 — ralph + tcp-three-way-handshake
Created: weeks/week-08-2026-02-23.md, tools/ralph.md, builds/tcp-three-way-handshake.md
Updated: index.md, log.md
[lint] No orphans. No concept gaps. Added ralph ↔ beads cross-link (both address long-horizon agent problems).

## [2026-04-08] ingest | week-09 — openclaw + crdt-collaborative-editor
Created: weeks/week-09-2026-03-02.md, tools/openclaw.md, builds/crdt-collaborative-editor.md
Updated: index.md, log.md
[lint] No orphans. Added cross-link between crdt-collaborative-editor and two-phase-commit (contrasting distributed consistency approaches).

## [2026-04-08] ingest | week-10 — language-modeling + bigram-language-model
Created: weeks/week-10-2026-03-09.md, tools/language-modeling.md, builds/bigram-language-model.md
Updated: index.md, log.md
[lint] No orphans. Language modeling appears for the first time; watching for recurrence to create concept page.

## [2026-04-08] ingest | week-11 — language-modeling + bigram-neural-net
Created: weeks/week-11-2026-03-16.md, builds/bigram-neural-net.md, concepts/language-modeling-fundamentals.md
Updated: tools/language-modeling.md (added week 11 section), index.md, log.md
[lint] Language-modeling-fundamentals concept gap detected (weeks 10 and 11 both cover makemore fundamentals) → created concepts/language-modeling-fundamentals.md. Cross-linked both bigram builds and the language-modeling tool page to the new concept. No orphans.

## [2026-04-08] ingest | week-12 — llm-wiki (AI only; no build)
Created: weeks/week-12-2026-03-23.md, tools/llm-wiki.md
Updated: concepts/language-modeling-fundamentals.md (added week 12 reference), index.md, log.md
[lint] No orphans. Added llm-wiki ↔ language-modeling-fundamentals cross-link (LLM wiki is the broader context for the makemore fundamentals). No new concept gaps.

## [2026-04-08] backfill lint | weeks 1–12 complete
[lint] Full backfill of 12 weeks complete. Verified: all pages reachable from index.md. All tool pages have at least one inbound link from a week or build page. All build pages linked from their corresponding week pages. Concepts (agent-protocols, model-context-protocol, language-modeling-fundamentals, jarvis-system) each have 2+ inbound links. No orphan pages detected. README.md updated with full progress table.
