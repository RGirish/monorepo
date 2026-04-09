# LLM-Operated Wiki System — Requirements Specification

## Concept

An LLM-maintained persistent knowledge base that sits between you and your raw sources. Instead
of re-deriving knowledge from scratch on every query (as RAG does), the LLM incrementally builds
and maintains a structured wiki — updating pages, cross-referencing concepts, flagging
contradictions, and keeping everything consistent as new content arrives.

The human's job: source material, direction, questions.
The LLM's job: all bookkeeping — summarizing, filing, cross-referencing, maintaining consistency.

---

## Architecture

Three layers:

**Raw sources / scratch** — your input material. The LLM reads from these but never modifies them.
Could be documents, notes, transcripts, scratch files, or anything else depending on the domain.

**The wiki** — a directory of LLM-generated and LLM-maintained markdown files. The LLM owns this
layer entirely. It creates pages, updates them when new content arrives, maintains cross-references,
and keeps everything consistent.

**The schema** — a CLAUDE.md file that tells the LLM how the wiki is structured, what conventions
to follow, and what workflows to execute. This is the key file that makes the LLM a disciplined
wiki maintainer rather than a generic chatbot.

---

## Directory Structure

```
<project-root>/
├── README.md                        ← public face; LLM maintains
│
├── wiki/
│   ├── CLAUDE.md                    ← schema; defines LLM behavior for this wiki
│   ├── index.md                     ← internal catalog; LLM creates + maintains
│   ├── log.md                       ← append-only history; LLM creates + maintains
│   ├── backlog.md                   ← future ideas; YOU add; LLM removes completed items
│   │
│   ├── __meta__/                    ← wiki system documentation; not operational
│   │   └── design/                  ← spec files, templates, decision records
│   │
│   ├── scratch/                     ← live note-taking during active work; YOU write freely
│   │   └── <unit-id>-<type>.md
│   │
│   ├── <category-1>/                ← project-specific content category
│   ├── <category-2>/                ← project-specific content category
│   ├── concepts/                    ← cross-cutting ideas; LLM creates + maintains
│   └── synthesis/                   ← LLM-generated analyses; created on demand
│
└── <source-material-or-code>/       ← raw sources; not modified by the wiki system
```

---

## Roles and Responsibilities

| Who | What | When |
|-----|------|-------|
| You | CLAUDE.md, stub README, directory structure | Once at setup |
| You | Scratch files — create empty, write freely | During each unit of work |
| You | Backlog — append ideas freely | Anytime |
| You | Source material / code — commit when ready | When work is done |
| You | Queries | Anytime |
| LLM | All wiki pages — creates, updates, cross-links | On ingest |
| LLM | Removes completed items from backlog | On ingest |
| LLM | Lint pass | Automatically on every ingest |
| LLM | Files valuable query answers as synthesis/ pages | On demand |

---

## Operations

### Ingest
The core operation. Triggered when you tell the LLM to process a new unit of content.

The LLM:
1. Reads scratch files and/or provided source material
2. Creates or updates pages in the appropriate content category directories
3. Creates or updates `concepts/` pages for any cross-cutting ideas that emerge
4. Names pages descriptively by subject — if something similar exists, the name reflects what is new or different
5. Removes completed items from `backlog.md`
6. Updates `index.md` — adds new pages, updates summaries of modified pages
7. Appends an entry to `log.md`
8. Updates `README.md`
9. Runs a lint pass automatically

### Lint (automatic on every ingest)
- Fix orphan pages — pages with no inbound links
- Add missing cross-references — concepts mentioned that have their own page but are not linked
- Create concept pages — concepts that appear across multiple pages but lack their own page
- Flag stale claims — content superseded or contradicted by newer ingests
- Append a lint summary to the current log entry

### Query (on demand)
- You ask questions against the wiki at any time
- LLM reads `index.md` to identify relevant pages, reads those pages, synthesizes an answer with citations
- Valuable answers (comparisons, analyses, patterns) get filed as `synthesis/` pages

### Backlog
- You append ideas to `backlog.md` at any time — no structure required
- LLM removes items matching what was just ingested, during every ingest

### Backfill (one time, if prior content exists)
- Provide existing notes/documents and ask the LLM to backfill retroactively
- No scratch files needed for past content
- Run after the directory structure and CLAUDE.md are in place so backfilled pages follow the same schema as future content
- Process units sequentially for best quality

---

## Content Page Design Principles

**Unit-scoped pages** — one page per unit of work (e.g., one page per week, one per project).
Acts as a container/overview that links to subject-scoped pages.

**Subject-scoped pages** — one page per subject (tool, concept, build, entity). Named by subject,
not by unit. Updated across multiple ingests if the subject recurs. If something similar was covered
before, the name should be distinct and reflect what is new or different.

**Concepts pages** — cross-cutting ideas that emerge across multiple units. The LLM creates these
proactively as themes emerge, even without being explicitly asked.

**Synthesis pages** — analyses, comparisons, and decision guides generated on demand. Saved
permanently so explorations compound rather than disappearing into chat history.

---

## Index and Log

**index.md** — content-oriented. A catalog of every wiki page with a one-line summary, organized
by category. The LLM reads this first when answering queries to identify relevant pages before
drilling in.

**log.md** — chronological. Append-only record of every ingest, query, and lint pass. Each entry
uses a consistent prefix for parseability:

```
## [yyyy-mm-dd] <operation> | <description>
```

---

## Naming Conventions

- All directories and filenames: kebab-case
- Scratch files: `<unit-id>-<content-type>.md`
- Unit-scoped pages: `<unit-id>.md`
- Subject-scoped pages: named by subject only, no unit identifier in the filename
- If a new page covers something similar to an existing page, the name must be distinct and
  reflect what is different — never overwrite an existing page with unrelated content

---

## Tooling Notes

- The wiki is a git repo of markdown files — version history and collaboration come for free
- Obsidian works well as a viewer — graph view, backlinks, and Dataview queries over frontmatter
- Public README + wiki in a GitHub repo doubles as a portfolio
- At larger scale (100+ pages), consider a local markdown search tool for hybrid BM25/vector search
  (e.g., [qmd](https://github.com/tobi/qmd)) instead of relying solely on index.md
