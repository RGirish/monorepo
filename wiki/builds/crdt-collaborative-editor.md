# CRDT Collaborative Text Editor

**Built in:** [Week 9](../weeks/week-09-2026-03-02.md)
**Code:** [data-structures/crdt](https://github.com/RGirish/monorepo/tree/main/code/data-structures/crdt)

---

## What It Is

A collaborative text editor that uses CRDTs (Conflict-free Replicated Data Types) to allow multiple clients to edit the same document concurrently without coordination or locking. Each client can make changes independently, and all replicas eventually converge to the same state when changes propagate.

## The Core Problem

In a distributed collaborative editor, two users might simultaneously insert or delete characters at the same position. A naive approach using character indices breaks down: if user A inserts at position 3 and user B deletes at position 3, the right outcome depends on the order the operations are processed — but in a distributed system, there's no global order.

## What Makes CRDTs Work

CRDTs solve this by designing data structures where merge operations are:
- **Commutative** — `merge(A, B) = merge(B, A)` (order doesn't matter)
- **Associative** — `merge(merge(A, B), C) = merge(A, merge(B, C))`
- **Idempotent** — `merge(A, A) = A` (applying the same op twice has no extra effect)

When these properties hold, all replicas converge to the same state regardless of message delivery order.

## Implementation: Sequence CRDT

The text editor uses a **sequence CRDT** for ordered text:
- Each character gets a **unique identifier** — typically `(site_id, logical_clock)` — that is stable and globally unique
- Characters are ordered by their identifiers, not by array index
- **Insert** creates a new character with a new ID positioned between two existing IDs
- **Delete** tombstones a character (marks it deleted) rather than removing it immediately

Because IDs are stable, inserts and deletes from different clients can be applied in any order and produce the same final document.

## CRDT vs. Operational Transformation

| | CRDT | Operational Transformation (OT) |
|--|------|----------------------------------|
| Approach | Design state so merges always converge | Transform operations to account for concurrent edits |
| Complexity | Manageable | Notoriously complex to get right |
| Adoption | Yjs, Automerge, Logoot | Google Docs (historically) |
| Consistency guarantee | Mathematical, provable | Depends on transformation correctness |

## Related Builds

- [Two-Phase Commit](two-phase-commit.md) — a contrasting approach to distributed consistency using coordination
- [Redis Rate Limiter](redis-rate-limiter.md) — a much smaller-scale concurrency problem (single-node race conditions) solved with atomic server-side scripting instead of conflict-free merges

## See Also

- [Concurrency and Atomicity](../concepts/concurrency-and-atomicity.md) — how this compares to the 2PC and Redis Lua approaches to the same underlying problem
