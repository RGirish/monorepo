# Wiki Log

Append-only history of all wiki operations.

---

## [2026-08-09] ingest | week-17 AI learning — tabfm
Created: tools/tabfm.md
Updated: weeks/week-17-2026-04-27.md (frontmatter `ai-topic` field + AI Learning section, previously "tbd" — week's build was already ingested 2026-07-19), index.md, backlog.md (removed the completed TabFM item), README.md (progress table row, Highlights, running themes), log.md
Note: content for this entry was generated from the two source links (Google Research blog, GitHub README) plus a full in-chat discussion working through whether TabFM's zero-shot claim actually eliminates feature engineering — conclusion: it relocates the work to context-row curation (the `max_num_rows=100` cap forces retrieval, and naive nearest-neighbor retrieval reintroduces a lighter version of the same feature-engineering-like distance decisions, hence the MMR-style diversity fix). The human explicitly asked for this discussion thread to be pulled into the ingested page rather than writing scratch notes separately.
[lint] No orphans: tabfm.md has inbound links from week-17, index.md, and README.md, with outbound links to tools/feature-engineering.md, tools/embedding-models.md, and builds/vector-db.md — added reciprocal inbound links on feature-engineering.md and embedding-models.md's "Related" sections. No missing links found elsewhere. No new concept gap yet — in-context learning / retrieval-for-ML is a single-week topic so far; watching for recurrence before filing a concepts/ page (candidate: how ICL context selection compares to RAG chunk selection from context-engineering.md). No stale content found.

## [2026-08-08] ingest | week-16 AI learning — open-knowledge-format
Created: tools/open-knowledge-format.md
Updated: weeks/week-16-2026-04-20.md (frontmatter `ai-topic` field + AI Learning section, previously "tbd" — week's build was already ingested 2026-07-19), tools/llm-wiki.md and tools/context-engineering.md (reciprocal cross-links), index.md, backlog.md (removed the completed Open Knowledge Format item), README.md (progress table row, Highlights, running themes, plus placeholder rows for weeks 30–32 to keep the table current through today), log.md
Note: content for this entry was generated directly from the three source links (Google Cloud blog, GitHub repo, SPEC.md) rather than from a human-authored scratch file — the human explicitly opted out of writing scratch notes this week and asked for the content to be generated and ingested directly.
[lint] No orphans: open-knowledge-format.md has inbound links from week-16 and index.md, with outbound links to context-engineering.md and llm-wiki.md, both of which now link back. No missing links found elsewhere. No new concept gap — OKF is a single-week topic with no cross-cutting pattern yet; watching for recurrence (e.g., if a future week revisits agent-context formats). No stale content found: week-17's `ai-topic: tbd` is untouched and still accurately outstanding — this ingest only resolved week 16.

## [2026-07-19] correction | signal-protocol-chat network layer reassigned from week-15 to week-17 (Part 2)
The prior entry below (re-ingest | week-15 build — signal-protocol-chat gets a real network layer) mis-attributed this session's Firebase/networking work to week 15 by extending its existing build page in place. Correcting per explicit instruction: the human wanted it filed as a separate build, "Signal Protocol Chat (Part 2)," under week 17, with week 15 left exactly as it was.
Reverted: builds/signal-protocol-chat.md and weeks/week-15-2026-04-13.md back to their pre-network-layer content (the local single-device simulation only); index.md and README.md's week-15/Signal-Protocol-Chat lines reverted to their original wording.
Created: weeks/week-17-2026-04-27.md (ai-topic: tbd, build: signal-protocol-chat-part-2), builds/signal-protocol-chat-part-2.md (the Firebase relay, persistent storage, Firebase Anonymous Auth, and access-control content, moved here from the reverted week-15 build page almost verbatim).
Updated: builds/signal-protocol-chat.md (added a "Built in ... continued in Part 2" pointer and a See Also link, matching the bike-sharing-feature-pipeline Part 1/Part 2 precedent), index.md and README.md (new week-17 row/line and Part 2 build entry, weeks-in counters bumped to 17).
Left as-is: backlog.md — the two narrower follow-up items (pre-key replenishment + push notifications; safety-number verification) added in the reverted entry are still accurate regardless of which week's build they're attributed to, since the work itself did happen, just under a different week label.
[lint] No orphans: signal-protocol-chat-part-2.md has inbound links from week-17, signal-protocol-chat.md, index.md, and README.md, with outbound links back to Part 1 and cryptography.md. Verified no other page still describes the old (incorrect) week-15-includes-networking state after the revert.

## [2026-07-19] re-ingest | week-15 build — signal-protocol-chat gets a real network layer
Updated: builds/signal-protocol-chat.md (full rewrite: local two-pane demo retired, documents Firebase relay, persistent on-device session storage, Firebase Anonymous Auth identity, Firestore Security Rules access control, and the allowBackup hardening), weeks/week-15-2026-04-13.md (Build section rewritten to describe the real networked chat), backlog.md (removed the completed network-layer item; added two narrower items -- pre-key replenishment + push notifications, and safety-number-style identity verification), index.md, README.md, log.md
[lint] No orphans. signal-protocol-chat.md's new "Access Control" section doesn't introduce a new concept page -- it's scoped tightly to this build's specific Firebase/Firestore setup rather than a cross-cutting idea, so it stays local to the build page rather than forking concepts/cryptography.md. No stale content elsewhere: this build was the only page describing the old local-only architecture. Backlog now carries two smaller, honestly-scoped follow-ups instead of one large deferred item, consistent with how much of the original backlog item actually shipped.

## [2026-07-19] ingest | week-16 build — bike-sharing-feature-pipeline-part-2
Created: weeks/week-16-2026-04-20.md (ai-topic: tbd, build: bike-sharing-feature-pipeline-part-2), builds/bike-sharing-feature-pipeline-part-2.md
Updated: builds/bike-sharing-feature-pipeline.md (Built-in line + Related Builds link forward to Part 2 — factual now that Part 2 exists, not speculative), concepts/tree-ensemble-mechanics.md (new "Interaction Terms vs. Axis-Aligned Splits" and "Feature Importance" sections, Appears-in/Related-Builds updated for week 16), tools/feature-engineering.md (empirical nuance added to Binning and Derived-quantities/interaction-features sections, Related Builds updated), index.md, backlog.md (removed "Feature engineering pipeline for a Kaggle dataset" — fully realized across Part 1 + Part 2), README.md (progress table row, Highlights weeks-in counter, running themes), log.md
[lint] No orphans: week-16 page and the new build page have inbound/outbound links to each other and to tree-ensemble-mechanics.md and feature-engineering.md. Missing-link check: every page updated in this ingest that discusses interaction terms, feature importance, or binning-for-trees now cross-links to the concept/build page that goes deeper. No new concept gap: interaction-terms and feature-importance mechanics folded into the existing tree-ensemble-mechanics.md (2nd week appearing there) rather than spinning up a new concepts/ page, consistent with how that page was created proactively in week 13 anticipating recurrence. Stale content: none found — Part 1's page already described only completed work per prior session's correction, so no rework needed there beyond adding the forward link.

## [2026-07-13] ingest | week-15 build — signal-protocol-chat
Created: builds/signal-protocol-chat.md
Updated: weeks/week-15-2026-04-13.md (frontmatter `build` field + Build section, previously "tbd"), concepts/cryptography.md (new "Beyond a Single Exchange" section on forward secrecy, post-compromise security, and KEMs), builds/asymmetric-encryption.md and builds/symmetric-encryption.md (reciprocal See Also links), backlog.md (removed the completed Signal Protocol chat app idea; added a new item for the deferred network layer, persistence, and Play Store deployment work), index.md, README.md (progress table row + Highlights + running themes), log.md
[lint] No orphans: signal-protocol-chat.md has inbound links from week-15, cryptography.md, asymmetric-encryption.md, symmetric-encryption.md, and index.md, with outbound links back to all of them. No missing links found — every page that mentions Signal Protocol, forward secrecy, or PQXDH now links to signal-protocol-chat.md. Concept gap: forward secrecy / post-compromise security / KEMs now appear across cryptography.md and signal-protocol-chat.md (2 pages) — folded into the existing cryptography.md concept page rather than spinning up a new one, since it's a direct extension of the symmetric/asymmetric fundamentals already covered there. No stale content found elsewhere.

## [2026-07-13] ingest | week-13 build — bike-sharing-feature-pipeline (stages 1–3 of 6, in progress)
Created: builds/bike-sharing-feature-pipeline.md, concepts/tree-ensemble-mechanics.md
Updated: weeks/week-13-2026-03-30.md (frontmatter `build` field + Build section, previously "no build"), tools/feature-engineering.md (added model-family nuance to categorical encoding section, cross-linked new build/concept pages), index.md, README.md (progress table row + running themes; also added missing placeholder rows for weeks 28–29 to keep the table current through today), log.md
[lint] No orphans: both new pages have inbound links (week-13 → build page; build page + feature-engineering.md → concept page) and outbound links back. Stale content fixed: tools/feature-engineering.md previously stated one-hot encoding is the "best default" for nominal categoricals with no model-family caveat — corrected with a nuance paragraph, since this build's stage 3 result (one-hot underperforming naive codes on a tree model) directly contradicts the blanket claim. Concept gap watch: tree-ensemble-mechanics.md currently appears on only 1 week — created proactively since it's near-certain to recur on the backlogged supervised-learning build; will fold in cross-links if/when that happens. Backlog item "Feature engineering pipeline for a Kaggle dataset" intentionally left in place (not removed) — build is only 3 of 6 stages complete, continues in week 15.

---

## [2026-07-04] ingest | week-15 — context-engineering (AI learning only; build TBD)
Created: weeks/week-15-2026-04-13.md, tools/context-engineering.md
Updated: index.md, backlog.md (removed prompt/context engineering item), README.md, log.md
[lint] No orphans. context-engineering.md cross-links to claude-code.md, agent-protocols.md, and ralph.md — all inbound links valid. No concept gap: context engineering is self-contained in the tools/ page; no multi-week pattern yet to warrant a concepts/ page.

---

## [2026-04-26] ingest | week-14 — multi-turn-rl + asymmetric-encryption
Created: builds/asymmetric-encryption.md (full), concepts/cryptography.md
Updated: weeks/week-14-2026-04-06.md (build section completed), builds/symmetric-encryption.md (added links to asymmetric + cryptography concept), index.md, README.md, log.md
[lint] Orphan fixed: asymmetric-encryption.md was stub — now fully populated. Concept gap filled: symmetric-encryption (week 6) and asymmetric-encryption (week 14) had no shared concept page — created concepts/cryptography.md covering hybrid encryption, padding schemes, and TLS composition. Cross-links added: symmetric-encryption.md → asymmetric-encryption.md and cryptography.md.

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

## [2026-04-13] ingest | week-12 build — llm-music-producer (partial)
Created: builds/llm-music-producer.md
Updated: weeks/week-12-2026-03-23.md (added build section), index.md, backlog.md (removed item), README.md, log.md
[lint] No orphans. llm-music-producer links to llm-wiki (same week) — cross-link added. Build marked in-progress; will update on completion.

## [2026-04-16] query | feature store request-time vs entity features — clarifying "request-time" at training time
Filed as synthesis/feature-store-request-time-vs-entity.md. "Request-time" means computed from the event record itself (not entity history) — applies at both training (historical rows) and serving (live request). Two-dimensional view: precomputed vs on-demand × entity history vs event itself.

## [2026-04-16] query | feature store training/serving skew — how it's actually prevented
Filed as synthesis/feature-store-training-serving-skew.md. Covers: precomputed entity features run once so both training and serving read the same result; on-demand features use a registered transformation function called identically in both contexts. Root cause of skew is separate teams in separate codebases, not intent.

## [2026-04-16] query | feature store data format — what the data actually looks like
Filed as synthesis/feature-store-data-format.md. Covers the canonical feature row structure, online vs offline store formats, where embeddings fit, what is NOT stored (code, raw data, weights), and a Feast schema example.

## [2026-04-16] query | feature store at inference time — online store and entity features
Filed as synthesis/feature-store-at-inference-time.md. Covers request-time vs entity features, the offline/online store split, why querying source databases directly fails at scale, and how the feature store prevents training/serving skew.

## [2026-04-16] query | weights vs embeddings vs features — what gets stored where
Filed as synthesis/weights-vs-embeddings-vs-features.md. Clarifies the three distinct artifacts (weights, embeddings, features), what system stores each (model registry vs. feature store vs. vector DB), and how they connect in a typical ML pipeline.

## [2026-04-16] query | feature stores — relevance in feature learning and deep NN era
Filed as synthesis/feature-stores.md. Covers what feature stores are, training/serving consistency, point-in-time correctness, and why they remain relevant for embeddings and hybrid systems — not just hand-engineered features. Cross-links to vector-db, embedding-models, and feature-engineering.

## [2026-04-16] re-ingest | week-13 — feature-engineering (updated notes)
Updated: tools/feature-engineering.md (expanded feature learning section: hierarchical extraction, layer depth, scalability), weeks/week-13-2026-03-30.md (updated summary), log.md
[lint] No new orphans or concept gaps introduced.

## [2026-04-15] ingest | week-13 — feature-engineering (AI only; no build)
Created: weeks/week-13-2026-03-30.md, tools/feature-engineering.md
Updated: backlog.md (removed feature engineering), index.md, README.md, log.md
[lint] No orphans. feature-engineering.md cross-links to language-modeling.md, llm-wiki.md, and concepts/language-modeling-fundamentals.md — all valid inbound/outbound links. No new concept gap yet (first week covering feature engineering). Prompt/context engineering remains in backlog; noted connection to feature-engineering.md's RAG/context engineering section for future cross-linking when ingested.

## [2026-04-26] ingest | week-14 — multi-turn-reinforcement-learning + asymmetric-encryption (in progress)
Created: weeks/week-14-2026-04-06.md, tools/multi-turn-reinforcement-learning.md, builds/asymmetric-encryption.md (stub)
Updated: index.md, README.md, log.md
[lint] No orphans. asymmetric-encryption.md cross-links to symmetric-encryption.md (week 06 counterpart) — valid inbound link added. multi-turn-reinforcement-learning.md cross-links to feature-engineering.md (supervised learning context), llm-wiki.md, and week-14 page. RL is a new topic appearing for the first time; watching for recurrence to create a concepts/reinforcement-learning.md page. No concept gaps yet with only one week of RL coverage.

## [2026-06-29] query | feature engineering teaching session — classical techniques, deep learning vs classical, end-to-end architecture
Created: synthesis/deep-learning-vs-classical-for-tabular-data.md, synthesis/feature-engineering-end-to-end-architecture.md
Updated: tools/feature-engineering.md (added Classical Techniques section: one-hot vs ordinal encoding, scaling, log transforms, binning, derived quantities, decomposition), index.md, log.md
[lint] No orphans introduced. Both new synthesis pages cross-link to existing feature-engineering.md, feature-stores.md, and feature-store-at-inference-time.md. deep-learning-vs-classical.md and feature-engineering-end-to-end-architecture.md cross-link to each other. No new concept gaps.

## [2026-04-08] backfill lint | weeks 1–12 complete
[lint] Full backfill of 12 weeks complete. Verified: all pages reachable from index.md. All tool pages have at least one inbound link from a week or build page. All build pages linked from their corresponding week pages. Concepts (agent-protocols, model-context-protocol, language-modeling-fundamentals, jarvis-system) each have 2+ inbound links. No orphan pages detected. README.md updated with full progress table.

## [2026-04-13] ingest | week-12 — llm-wiki + llm-music-producer
Updated: builds/llm-music-producer.md (full rewrite — both Base95 and MIDI-as-text approaches, removed in-progress status), weeks/week-12-2026-03-23.md (build section updated to describe both pipelines), index.md (week 12 summary and builds entry updated), README.md (removed in-progress from week 12 row), log.md
[lint] No orphans. agentskills.io referenced in week-12 and builds/llm-music-producer.md — only one week, no concept gap yet. All cross-links valid: llm-music-producer.md → llm-wiki.md ✓, week-12 → both pages ✓. No stale content detected.
