# Concurrency and Atomicity

Four builds, four different scales, four different strategies for the same underlying problem: how do you make a sequence of operations behave as one indivisible unit, or avoid needing that guarantee at all, when multiple things could happen at once?

## The Four Approaches

| Build | Scale | Strategy | How it works |
|-------|-------|----------|---------------|
| [Two-Phase Commit](../builds/two-phase-commit.md) (Week 4) | Distributed — multiple nodes | Coordination protocol | A coordinator collects votes from all participants before committing; all-or-nothing is enforced by a prepare/commit handshake, at the cost of blocking if the coordinator fails mid-protocol |
| [CRDT Collaborative Editor](../builds/crdt-collaborative-editor.md) (Week 9) | Distributed — multiple replicas | Conflict-free design | Sidesteps the coordination problem entirely — merge operations are designed to be commutative, associative, and idempotent, so concurrent edits converge to the same state regardless of arrival order, with no locking or voting needed |
| [Redis Rate Limiter](../builds/redis-rate-limiter.md) (Week 19) | Single-node — one Redis instance | Atomic server-side execution | Moves a multi-step sequence (`INCR` then `EXPIRE`, or prune-then-count-then-add) into a Lua script that Redis's single-threaded execution model runs as one indivisible unit — no coordination needed because there's only one thread of execution to interleave with |
| [Ray Word-Length Pipeline](../builds/ray-word-length-pipeline.md) (Week 20) | Single process per actor, many concurrent callers | Serialized mailbox | A Ray actor queues incoming method calls and executes them one at a time, so `self.total_count += count` from 10 concurrent tasks never interleaves — the same "only one thread of execution" trick as Redis's Lua scripting, but applied to one arbitrary stateful Python object rather than a whole server |

## The Common Thread

All three are answers to the same question — "what happens if something interrupts a multi-step operation partway through?" — but they diverge based on what's actually available to exploit:

- **2PC** assumes you *must* coordinate independent nodes with independent failure modes, so it pays the cost of an explicit voting protocol (and inherits its blocking-on-coordinator-failure weakness).
- **CRDTs** reframe the problem so coordination is never needed — by constraining the data structure and merge function up front, any interleaving order produces the same result.
- **Redis's Lua atomicity** is the cheapest of the three, but only because it operates within a single process (Redis's event loop) rather than across independently-failing machines — the same trick isn't available once state is actually distributed across nodes.
- **Ray's actor serialization** is the same "single thread of execution" trick as Redis, generalized from one server process to any stateful Python object — each actor instance is its own process with its own serialized call queue, so no locking is needed to protect its internal state, but (like Redis) this guarantee is local to one actor and doesn't extend across actors or nodes.

The naive Redis rate limiter (`INCR` + conditional `EXPIRE`, [see build](../builds/redis-rate-limiter.md#core-concepts)) is a small-scale echo of exactly the failure mode 2PC's prepare/commit split exists to prevent: a crash landing between two operations that were supposed to happen together. The fix looks different at each scale — a full coordination protocol for 2PC's multi-node case, a single `EVAL` call for Redis's single-node case — but the underlying vulnerability (a gap between two operations that a failure can land in) is the same shape both times.

## See Also

- [Cryptography Fundamentals](cryptography.md) — a related but distinct kind of "correctness under adversarial conditions" concern (confidentiality/integrity rather than concurrent-operation ordering)
