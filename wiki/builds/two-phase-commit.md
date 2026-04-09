# Two-Phase Commit (2PC)

**Built in:** [Week 4](../weeks/week-04-2026-01-26.md)
**Code:** [distributed-systems/consensus/2-phase-commit/main.py](https://github.com/RGirish/monorepo/blob/main/code/distributed-systems/consensus/2-phase-commit/main.py)

---

## What It Is

An implementation of the two-phase commit (2PC) protocol — a distributed consensus algorithm for coordinating transactions across multiple participant nodes so that all nodes either commit or abort as a unit.

## The Protocol

2PC involves two roles: a **coordinator** that initiates and manages the transaction, and **participants** that each hold a piece of the transaction's work.

### Phase 1: Prepare
1. Coordinator sends a `PREPARE` message to all participants
2. Each participant checks whether it can commit (acquires locks, validates constraints)
3. Each participant responds with `VOTE_COMMIT` or `VOTE_ABORT`

### Phase 2: Commit or Abort
- If **all participants voted COMMIT**: coordinator sends `COMMIT` to all; participants apply changes and release locks
- If **any participant voted ABORT**: coordinator sends `ABORT` to all; participants roll back changes and release locks

```
Coordinator          Participant A         Participant B
    |                      |                     |
    |------- PREPARE ----->|                     |
    |------- PREPARE ----------------->|         |  (sent to both)
    |                      |                     |
    |<----- VOTE_COMMIT ---|                     |
    |<----- VOTE_COMMIT -------------------|     |
    |                      |                     |
    |------- COMMIT ------>|                     |
    |------- COMMIT ------------------>|         |
```

## Properties

- **Atomicity** — all participants commit or none do
- **Consistency** — preserves data invariants across all nodes

## Known Limitations

- **Blocking on coordinator failure** — if the coordinator crashes after sending PREPARE but before sending COMMIT/ABORT, participants are stuck holding locks indefinitely. This is why 3PC and Paxos-based approaches exist.
- **Not partition-tolerant** — cannot make progress if the coordinator and participants are partitioned from each other

## Related Builds

- [CRDT Collaborative Editor](crdt-collaborative-editor.md) — an alternative approach to distributed consistency using CRDTs instead of coordination protocols
