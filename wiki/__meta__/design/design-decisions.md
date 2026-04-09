# Wiki System — Design Decisions Checklist

Use this before implementing a wiki system for a new project. Answer each question, then hand
this document alongside `wiki-system-spec.md` and `CLAUDE.md.template` to your LLM agent with
the instruction: "Implement a wiki system for my project using these specs and my answers below."

---

## 1. Purpose and Audience

- What is this wiki for? What knowledge does it accumulate over time?
- Who is the primary audience — just you, your team, or the public?
- Is this a personal reference, a public portfolio, an internal team knowledge base, or something else?
- Is there a natural "unit of work" that triggers an ingest? (e.g., a week, a sprint, a document, a meeting, a chapter)

---

## 2. Content Categories

- What are the distinct types of content this wiki will contain?
- For each category:
  - What does a single page in this category represent?
  - Is it unit-scoped (one page per ingest unit) or subject-scoped (one page per subject, updated across multiple ingests)?
  - How should pages in this category be named?
- Which category acts as the "container" or overview for each ingest unit?
- Do you want a `concepts/` directory for cross-cutting ideas that emerge across units?
- Do you want a `synthesis/` directory for on-demand analyses and comparisons?

---

## 3. Unit of Work

- What is the atomic unit that triggers an ingest?
- How is a unit identified? (e.g., a number, a date, a name, a combination)
- Is the unit time-based (e.g., weekly), event-based (e.g., per document), or milestone-based?
- Can multiple units be batched in one session (catch-up scenario)?
- If time-based: what is the start date of unit 1, and what is the cadence?

---

## 4. Scratch Files

- Do you want scratch files for live note-taking during active work? (recommended if you want to capture thoughts as they happen rather than writing them up at the end)
- If yes:
  - How many scratch files per unit? What do they each capture?
  - What is the naming convention? (e.g., `week-01-2026-01-05-ai-learning.md`)
- What happens to scratch files after ingest — do they stay permanently, get archived, or get deleted?

---

## 5. Backlog

- Do you want a `backlog.md` for capturing future ideas?
- What sections should it have? (e.g., "Learning Ideas", "Build Ideas", "Topics to Explore")
- Should the LLM automatically remove completed items during ingest? (recommended — keeps the backlog clean without manual maintenance)

---

## 6. Public Face

- Should there be a public-facing `README.md` at the project root?
- What should it contain? (e.g., progress table, highlights, links into the wiki)
- Who is the external reader? What do you want them to take away?
- Is the project public on GitHub? Does it serve as a portfolio?
- Important: README must use standard markdown links, not Obsidian wikilink syntax

---

## 7. Naming Conventions

- How should subject-scoped pages be named — by the subject name only, or with additional context?
- What should happen if a similar subject appears more than once? (update the existing page, or create a new distinctly-named page?)
- Any domain-specific naming patterns to enforce?

---

## 8. Existing Content (Backfill)

- Does content exist that predates the wiki and should be migrated in?
- Where does it currently live? (e.g., Google Doc, Notion, chat history, existing files)
- How much content is there?
- Recommended approach: set up the directory structure and CLAUDE.md first, then backfill so that all pages follow the same schema from the start

---

## 9. Tooling

- Will you use Obsidian to browse the wiki? (enables graph view, backlinks, Dataview queries)
- If yes: will you open the whole project root as the vault, or just the `wiki/` subdirectory?
- Do you want YAML frontmatter on pages for Dataview queries? If so, what fields?
- Is the wiki in a git repo? (strongly recommended — free version history and collaboration)

---

## 10. Additional Operations

- Beyond ingest, lint, query, and backlog: are there any domain-specific operations the LLM should support?
  Examples:
  - A weekly digest or summary email
  - A stakeholder-facing report generated from the wiki
  - A "what should I do next" recommendation based on backlog + recent ingests
  - Automatic tagging or categorization beyond what's described above
