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

No files are created for this — the human writes/talks through the AI learning directly in
conversation, and it gets filed at ingest time.

If a specific week number N is given, use it directly.

If no week number is given, determine the target week:
1. Run the Current week status workflow to identify the in-progress week (if any, from this
   conversation) and the last completed week
2. If a week is already **in progress** in this conversation (AI learning or build content for
   it has been discussed but not yet ingested): do not assume — ask the human "You have Week N
   in progress — should I add this AI learning to Week N, or start it as part of a new week?"
3. If no week is in progress: target the next week after the last completed one

Then look up the nominal start date for the target week from the Week Reference table below,
confirm the week number and date with the human, and invite them to start writing/talking
through the AI learning now.

### Start a week's build
Triggers: "start week N build" / "new build for week N" / "set up week N build" / "start a new build" / "new build"

No files are created for this — the human describes the build directly in conversation, which
kicks off the Build Sessions workflow below.

If a specific week number N is given, use it directly.

If no week number is given, determine the target week:
1. Run the Current week status workflow to identify the in-progress week (if any, from this
   conversation) and the last completed week
2. If a week is already **in progress** in this conversation: do not assume — ask the human "You
   have Week N in progress — should I add this build to Week N, or start it as part of a new week?"
3. If no week is in progress: target the next week after the last completed one

Then look up the nominal start date for the target week from the Week Reference table below,
confirm the week number and date with the human, and invite them to describe what they're building.

### Start both for a week
Triggers: "start week N" / "set up week N" / "begin week N" / "start a new week" / "new week"

If a specific week number N is given, use it directly. If no week number is given, apply the same
logic as above (check in-progress in this conversation, confirm with human if ambiguous, otherwise
use next week after last completed).

Confirm the week number and date, then invite the human to write/talk through both the AI learning
and the build — no files are created.

### Current week status
Triggers: "what week am I on" / "which week am I on" / "what week is this" / "where am I in the project"

Do NOT answer with the current calendar week number. Instead, determine the project week from the repo state.

A week is **truly complete** only when BOTH its `ai-topic:` and `build:` frontmatter fields in its
`wiki/weeks/` page are filled in with a real value — not empty, `tbd`, `none`, or similar placeholder.
An ingested page (a page existing in `wiki/weeks/`) is necessary but not sufficient for completeness —
always check its frontmatter, don't infer completeness from the page's existence alone.

1. Check `wiki/weeks/` for the highest-numbered ingested week page
2. Read that page's frontmatter — if both `ai-topic:` and `build:` are filled in, that week is **complete**;
   if either is a placeholder (`tbd`, `none`, empty), that week is **incomplete** even though it was ingested
3. Also scan all other ingested `wiki/weeks/` pages for placeholder `ai-topic:` or `build:` values — these
   are **outstanding** weeks (owed, not waived — see prior guidance on this)
4. Check this conversation for any week's AI learning or build content that's been discussed but not
   yet ingested, for a week beyond the last ingested one — that week is **in progress**. There's no
   file-based record of this; it only exists within the current conversation.
5. Report accordingly, combining all of the above into one nuanced answer rather than a single label:
   - State the current/next week using the same logic as before (in-progress-in-conversation →
     "in progress"; otherwise last ingested week + 1 is "next")
   - If the highest-numbered ingested week has a placeholder `ai-topic:` or `build:`, say so explicitly
     rather than calling it complete (e.g., "Week N was ingested but its build is still TBD")
   - If any other ingested weeks have outstanding placeholders, mention them too
   - If no weeks/ pages exist yet: "No weeks completed yet — Week 1 is next"

### Add to backlog
Triggers: "add to backlog: [idea]" / "backlog this: [idea]" / "I want to learn X" / "add build idea: [idea]"

1. Determine which section the idea belongs to (AI Learning Ideas or Build Ideas) from context
   — if unclear, ask
2. Append it to the appropriate section in `wiki/backlog.md`
3. Confirm what was added and to which section

---

## Build Sessions

When the human starts a build (any language, any week), do NOT implement the whole thing upfront.
The goal is learning-by-doing. Follow this approach:

1. **Orient first** — briefly explain what the build will demonstrate and the key concept(s) behind it (2–4 sentences max)
2. **Propose a step sequence** — break the build into 3–6 logical stages; show the plan and ask if it looks right before writing any code
3. **One stage at a time** — implement one stage, then stop. Before moving on, ask a question that makes the human think about *why* the code works the way it does, or what would happen if something changed. Wait for their response.
4. **Build on their answer** — acknowledge what they said, fill in any gaps, then proceed to the next stage
5. **Never skip ahead** — even if the next step is obvious, pause and check in

The questions should probe understanding of the underlying concept, not just the code mechanics.
Examples of good questions: "Why do you think we use the recipient's public key here rather than their private key?",
"What do you think would happen if we skipped the padding step?", "How would an attacker exploit this if we removed the signature?"

---

## Python Builds

Every Python build gets its own virtual environment. Never install packages into a global or
system interpreter.

When creating a new Python build:
1. Create the build directory
2. Create a venv inside it: `python3 -m venv .venv` (or `python3.11 -m venv .venv` if the build requires a specific version)
3. Install dependencies with `.venv/bin/pip install ...`
4. Always invoke Python and scripts via `.venv/bin/python` (or activate with `source .venv/bin/activate` before running)
5. Add `.venv/` to the build's `.gitignore` if one exists, or remind the human to do so

When working in an existing Python build, check for a `.venv/` directory first and use it.

---

## Wiki Operations

### Ingest
Triggers: "ingest week N" / "ingest weeks N and M" (for catch-up)

1. Look up the nominal start date for week N from the Week Reference table below
2. Ingest from the AI learning and/or build content discussed directly in conversation. Never block
   or ask for confirmation because one is missing — a missing build is pending by default (see step 5).
3. Create `wiki/weeks/week-NN-yyyy-mm-dd.md` — overview page with frontmatter, linking to tools/ and builds/ pages
4. Create or update the appropriate page in `wiki/tools/` for the AI topic covered
5. If a build happened this week, create a new page in `wiki/builds/` for it — named descriptively and distinctly.
   If no build happened, set `build: none` in the week's frontmatter and move on without asking — a missing build
   is pending by default, not a blocker to ingesting the AI learning. Do not flag it or ask about it during ingest;
   it'll surface naturally next time someone runs the Current week status workflow.
6. Create or update any `wiki/concepts/` pages for cross-cutting ideas that emerge
7. Remove from `wiki/backlog.md` any items matching what was just learned or built
8. Update `wiki/index.md` — add new pages, update summaries of modified pages
9. Append to `wiki/log.md` (see Log Format below)
10. Update `README.md` (see README below)
11. Run lint pass automatically (see Lint below)
12. Commit all changes from this ingest (wiki pages, README.md, and any new/changed files under `code/`) and push to the remote — an ingest is not complete until it's pushed

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
4. If the answer is a useful analysis or comparison worth keeping, file it as a `wiki/synthesis/` page — do not ask, just do it. Err on the side of filing more rather than less.

---

## Wiki Directory Structure

```
wiki/
├── index.md               ← internal catalog; LLM maintains
├── log.md                 ← append-only history; LLM maintains
├── backlog.md             ← human adds ideas; LLM removes completed items on ingest
├── __meta__/              ← wiki system design docs; ignore during normal operations
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

### synthesis/ — proactive, not on demand
LLM-generated analyses, comparisons, and decision guides. File proactively whenever a query
answer is worth keeping — err on the side of filing more rather than less. Do not ask the human
for permission; use judgement and file it.

---

## Naming Conventions

- All directories and filenames: kebab-case
- Week pages: `week-NN-yyyy-mm-dd.md` (nominal Monday date, zero-padded week number)
- Subject pages (tools/, builds/, concepts/, synthesis/): named by subject only — no week identifier
- If a similar subject-scoped page already exists, create a new distinctly named page — never overwrite

---

## README.md

Maintain as the public-facing portfolio index for GitHub visitors.

Contents:
- Brief description of the 2026 challenge
- Progress table: one row per completed week — week number, date, AI topic, build name, link to week page
- Highlights section (best build, most interesting topic, running themes) — update on every ingest, reflecting the most recent completed weeks
- Links into the wiki (tools, builds, synthesis)

Rules:
- Write for an external reader who has never seen this project
- Standard markdown links with relative paths only — no Obsidian wikilink syntax
- Scannable: tables and short bullets over prose
- The progress table must always include rows up to and including the current calendar week (use today's date to determine which project week that is, via the Week Reference table). Weeks that have not been ingested yet get placeholder values: `| NN | Mon DD | — | — | *(not started)* |`. This makes it immediately visible how many weeks are behind.

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
| 01   | 2026-01-05 | | 19   | 2026-05-11 | | 37   | 2026-09-14 |
| 02   | 2026-01-12 | | 20   | 2026-05-18 | | 38   | 2026-09-21 |
| 03   | 2026-01-19 | | 21   | 2026-05-25 | | 39   | 2026-09-28 |
| 04   | 2026-01-26 | | 22   | 2026-06-01 | | 40   | 2026-10-05 |
| 05   | 2026-02-02 | | 23   | 2026-06-08 | | 41   | 2026-10-12 |
| 06   | 2026-02-09 | | 24   | 2026-06-15 | | 42   | 2026-10-19 |
| 07   | 2026-02-16 | | 25   | 2026-06-22 | | 43   | 2026-10-26 |
| 08   | 2026-02-23 | | 26   | 2026-06-29 | | 44   | 2026-11-02 |
| 09   | 2026-03-02 | | 27   | 2026-07-06 | | 45   | 2026-11-09 |
| 10   | 2026-03-09 | | 28   | 2026-07-13 | | 46   | 2026-11-16 |
| 11   | 2026-03-16 | | 29   | 2026-07-20 | | 47   | 2026-11-23 |
| 12   | 2026-03-23 | | 30   | 2026-07-27 | | 48   | 2026-11-30 |
| 13   | 2026-03-30 | | 31   | 2026-08-03 | | 49   | 2026-12-07 |
| 14   | 2026-04-06 | | 32   | 2026-08-10 | | 50   | 2026-12-14 |
| 15   | 2026-04-13 | | 33   | 2026-08-17 | | 51   | 2026-12-21 |
| 16   | 2026-04-20 | | 34   | 2026-08-24 | | 52   | 2026-12-28 |
| 17   | 2026-04-27 | | 35   | 2026-08-31 | | | |
| 18   | 2026-05-04 | | 36   | 2026-09-07 | | | |

