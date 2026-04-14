# CLAUDE.md

## Project Overview

A personal 2026 learning challenge: one new AI topic learned and one new piece of software built
every week. Weeks are numbered 1–52, each starting on a Monday.

- `wiki/` — LLM-maintained knowledge base tracking all learning and builds
- `code/` — all builds, organized by domain (data-structures/, gen-ai/, databases/, etc.)

The human's job: source material, direction, questions.
The LLM's job: all bookkeeping — filing, cross-referencing, maintaining consistency.

---

## Human-Driven Workflows

These are the tasks the human drives. Use natural language — the phrases below are examples,
not rigid commands.

### Start a week's AI learning
Triggers: "start week N AI learning" / "new AI learning for week N" / "set up week N learning" / "start a new AI learning" / "new AI learning"

If a specific week number N is given, use it directly.

If no week number is given, determine the target week from repo state first:
1. Run the Current week status workflow to identify the in-progress week (if any) and the last completed week
2. If a week is **in progress** (scratch files exist beyond the last ingested week): do not assume — ask the human "You have Week N in progress — should I add this AI learning to Week N, or start it as part of a new week?"
3. If no week is in progress: target the next week after the last completed one

Then:
1. Look up the nominal start date for the target week from the Week Reference table below
2. Create `wiki/scratch/week-NN-yyyy-mm-dd-ai-learning.md` with this header:
   ```
   # Week NN — AI Learning
   Topic:
   Started: <today's actual date>
   Week date: <nominal Monday date>

   ---

   ```
3. Tell the human the exact file path so they can open it and start writing freely

### Start a week's build
Triggers: "start week N build" / "new build for week N" / "set up week N build" / "start a new build" / "new build"

If a specific week number N is given, use it directly.

If no week number is given, determine the target week from repo state first:
1. Run the Current week status workflow to identify the in-progress week (if any) and the last completed week
2. If a week is **in progress** (scratch files exist beyond the last ingested week): do not assume — ask the human "You have Week N in progress — should I add this build to Week N, or start it as part of a new week?"
3. If no week is in progress: target the next week after the last completed one

Then:
1. Look up the nominal start date for the target week from the Week Reference table below
2. Create `wiki/scratch/week-NN-yyyy-mm-dd-build.md` with this header:
   ```
   # Week NN — Build
   What I'm building:
   Started: <today's actual date>
   Week date: <nominal Monday date>

   ---

   ```
3. Tell the human the exact file path so they can open it and start writing freely

### Start both for a week
Triggers: "start week N" / "set up week N" / "begin week N" / "start a new week" / "new week"

If a specific week number N is given, use it directly. If no week number is given, apply the same repo-state logic as above (check in-progress, confirm with human if ambiguous, otherwise use next week after last completed).

Run both the AI learning and build workflows above in sequence. Create both scratch files and confirm both paths.

### Current week status
Triggers: "what week am I on" / "which week am I on" / "what week is this" / "where am I in the project"

Do NOT answer with the current calendar week number. Instead, determine the project week from the repo state:

1. Check `wiki/weeks/` for the highest-numbered ingested week page — that week is **complete**
2. Check `wiki/scratch/` for any week files beyond the last ingested week — that week is **in progress**
3. Report accordingly:
   - If a scratch file exists beyond the last ingested week: "You're currently on Week N (in progress)"
   - If no scratch file exists beyond the last ingested week: "Week N is complete — Week N+1 is next"
   - If no weeks/ pages exist yet: "No weeks completed yet — Week 1 is next"

### Add to backlog
Triggers: "add to backlog: [idea]" / "backlog this: [idea]" / "I want to learn X" / "add build idea: [idea]"

1. Determine which section the idea belongs to (AI Learning Ideas or Build Ideas) from context
   — if unclear, ask
2. Append it to the appropriate section in `wiki/backlog.md`
3. Confirm what was added and to which section

---

## Wiki Operations

### Ingest
Triggers: "ingest week N" / "ingest weeks N and M" (for catch-up)

1. Look up the nominal start date for week N from the Week Reference table below
2. Read `wiki/scratch/week-NN-yyyy-mm-dd-ai-learning.md` and `wiki/scratch/week-NN-yyyy-mm-dd-build.md`
3. Create `wiki/weeks/week-NN-yyyy-mm-dd.md` — overview page with frontmatter, linking to tools/ and builds/ pages
4. Create or update the appropriate page in `wiki/tools/` for the AI topic covered
5. Create a new page in `wiki/builds/` for what was built — named descriptively and distinctly
6. Create or update any `wiki/concepts/` pages for cross-cutting ideas that emerge
7. Remove from `wiki/backlog.md` any items matching what was just learned or built
8. Update `wiki/index.md` — add new pages, update summaries of modified pages
9. Append to `wiki/log.md` (see Log Format below)
10. Update `README.md` (see README below)
11. Run lint pass automatically (see Lint below)

For catch-up ingests, process each week fully and sequentially before moving to the next.

### Lint (automatic after every ingest)
- **Orphan pages** — find pages with no inbound links; add cross-references from relevant pages
- **Missing links** — find pages that mention a subject with its own page but don't link to it; add the link
- **Concept gaps** — find themes appearing across 2+ pages without a `concepts/` page; create one
- **Stale content** — find claims superseded or contradicted by newer ingests; update or flag them
- Append a `[lint]` summary line to the current `wiki/log.md` entry

### Query
Triggers: any question about the wiki content

1. Read `wiki/index.md` to identify relevant pages
2. Read those pages
3. Synthesize a clear answer with citations (links to specific pages)
4. If the answer is a useful analysis or comparison worth keeping, offer to file it as a `wiki/synthesis/` page

---

## Wiki Directory Structure

```
wiki/
├── index.md               ← internal catalog; LLM maintains
├── log.md                 ← append-only history; LLM maintains
├── backlog.md             ← human adds ideas; LLM removes completed items on ingest
├── __meta__/              ← wiki system design docs; ignore during normal operations
├── scratch/               ← human writes freely; LLM reads on ingest; never modified by LLM
│   └── week-NN-yyyy-mm-dd-{ai-learning|build}.md
├── weeks/                 ← one page per unit; unit-scoped
├── tools/                 ← one page per AI topic/tool; subject-scoped
├── builds/                ← one page per thing built; subject-scoped
├── concepts/              ← cross-cutting ideas; subject-scoped; LLM creates proactively
└── synthesis/             ← analyses and decision guides; created on demand
```

---

## Content Categories

### weeks/ — unit-scoped
One page per week. Named `week-NN-yyyy-mm-dd.md` using the nominal Monday start date. Acts as
the container and overview: what AI topic was covered, what was built, brief summary of each,
links to the corresponding tools/ and builds/ pages.

Frontmatter (required):
```yaml
---
week: 7
date: 2026-02-16
ai-topic: cursor
build: bigram-language-model
tags: [ide, language-models]
---
```

### tools/ — subject-scoped
One page per AI topic, tool, framework, concept, or paper. Named by subject in kebab-case
(e.g., `claude-api.md`, `attention-is-all-you-need.md`). Updated if the same topic recurs in
a later week — add a new section for that week. Covers the AI learning goal only.

### builds/ — subject-scoped
One page per thing built. Named descriptively by subject in kebab-case. Builds can be anything —
AI or not (data structures, OS concepts, networking, etc.). No week identifier in the filename.
If something similar was built before, the name must be distinct and reflect what is new or
different (e.g., `bigram-language-model.md` vs `transformer-language-model.md`).

### concepts/ — subject-scoped
Cross-cutting ideas and patterns that emerge across multiple weeks. Created proactively by the
LLM when a concept appears across 2+ pages. Not limited to AI topics.

### synthesis/ — on demand
LLM-generated analyses, comparisons, and decision guides. Created when a query answer is worth
keeping permanently rather than disappearing into chat history.

---

## Naming Conventions

- All directories and filenames: kebab-case
- Scratch files: `week-NN-yyyy-mm-dd-{ai-learning|build}.md`
- Week pages: `week-NN-yyyy-mm-dd.md` (nominal Monday date, zero-padded week number)
- Subject pages (tools/, builds/, concepts/, synthesis/): named by subject only — no week identifier
- If a similar subject-scoped page already exists, create a new distinctly named page — never overwrite

---

## README.md

Maintain as the public-facing portfolio index for GitHub visitors.

Contents:
- Brief description of the 2026 challenge
- Progress table: one row per completed week — week number, date, AI topic, build name, link to week page
- Highlights section (best build, most interesting topic, running themes) — update every 4–5 ingests
- Links into the wiki (tools, builds, synthesis)

Rules:
- Write for an external reader who has never seen this project
- Standard markdown links with relative paths only — no Obsidian wikilink syntax
- Scannable: tables and short bullets over prose

---

## wiki/index.md

Internal navigation catalog. Every wiki page listed with a relative link and one-line summary,
organized by category: Weeks, Tools, Builds, Concepts, Synthesis. Updated on every ingest.
Read this first when answering any query.

---

## Log Format

Append-only. Never modify existing entries.

```
## [yyyy-mm-dd] ingest | week-NN — <AI topic> + <build name>
Created: <list of new pages>
Updated: <list of modified pages>
[lint] <brief summary of lint findings and fixes>

## [yyyy-mm-dd] query | <question summary>
<one sentence on what was synthesized and whether it was filed as a synthesis/ page>
```

---

## Week Reference

Week 1 starts on 2026-01-05. Each subsequent week starts on the following Monday.
Week numbers are fixed labels — the date in a filename is always the nominal Monday start date,
not the date the work was actually done.

| Week | Start date | | Week | Start date | | Week | Start date |
|------|------------|-|------|------------|-|------|------------|
| 01   | 2026-01-05 | | 19   | 2026-05-04 | | 37   | 2026-09-07 |
| 02   | 2026-01-12 | | 20   | 2026-05-11 | | 38   | 2026-09-14 |
| 03   | 2026-01-19 | | 21   | 2026-05-18 | | 39   | 2026-09-21 |
| 04   | 2026-01-26 | | 22   | 2026-05-25 | | 40   | 2026-09-28 |
| 05   | 2026-02-02 | | 23   | 2026-06-01 | | 41   | 2026-10-05 |
| 06   | 2026-02-09 | | 24   | 2026-06-08 | | 42   | 2026-10-12 |
| 07   | 2026-02-16 | | 25   | 2026-06-15 | | 43   | 2026-10-19 |
| 08   | 2026-02-23 | | 26   | 2026-06-22 | | 44   | 2026-10-26 |
| 09   | 2026-03-02 | | 27   | 2026-06-29 | | 45   | 2026-11-02 |
| 10   | 2026-03-09 | | 28   | 2026-07-06 | | 46   | 2026-11-09 |
| 11   | 2026-03-16 | | 29   | 2026-07-13 | | 47   | 2026-11-16 |
| 12   | 2026-03-23 | | 30   | 2026-07-20 | | 48   | 2026-11-23 |
| 13   | 2026-03-30 | | 31   | 2026-07-27 | | 49   | 2026-11-30 |
| 14   | 2026-04-06 | | 32   | 2026-08-03 | | 50   | 2026-12-07 |
| 15   | 2026-04-13 | | 33   | 2026-08-10 | | 51   | 2026-12-14 |
| 16   | 2026-04-20 | | 34   | 2026-08-17 | | 52   | 2026-12-21 |
| 17   | 2026-04-27 | | 35   | 2026-08-24 | | | |
| 18   | 2026-05-04 | | 36   | 2026-08-31 | | | |

