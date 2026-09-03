# Redis Rate Limiter

**Built in:** [Week 19](../weeks/week-19-2026-05-11.md)
**Code:** [databases/redis-rate-limiter](https://github.com/RGirish/monorepo/tree/main/code/databases/redis-rate-limiter)

---

## What It Is

A hands-on introduction to Redis — first exploring it directly as a key/value cache via `redis-cli` (`SET`/`GET`/`EXPIRE`/`TTL`/`INCR`), then building three progressively more correct versions of a rate limiter in Python (`redis-py`) to learn Redis's atomicity guarantees and Lua scripting.

## Core Concepts

### TTL Sentinel Values
`TTL key` returns `-2` if the key doesn't exist, `-1` if it exists but has no expiry, or the seconds remaining. This is distinct from `GET` returning `nil` for a missing key — three different "nothing here" signals for three different situations.

### The Orphaned-Counter Race Condition
A naive fixed-window limiter does `INCR key` then conditionally `EXPIRE key window` when the count is `1`. `INCR` and `EXPIRE` are each atomic individually, but the *sequence* is not: if the client crashes between the two calls (an OOM kill, a deploy restart, a network blip), the key is left with a count but no TTL — `TTL` stays at `-1` forever, and the counter never resets. Demonstrated directly by issuing only the `INCR` half via `redis-cli` and watching the key sit at `TTL -1` indefinitely.

### Lua Scripting for Atomicity
Redis runs Lua scripts (`EVAL`) as a single indivisible unit under its single-threaded execution model — no other command, and no client-side crash, can be observed mid-script. This moves the atomicity boundary from "between two client-issued commands" (a gap a crash can land in) to "before or after one server-executed script" (no gap possible): either the whole script's effects exist, or none do.

```lua
-- KEYS[1] = rate limit key
-- ARGV[1] = window length in seconds
local current = redis.call("INCR", KEYS[1])
if tonumber(current) == 1 then
    redis.call("EXPIRE", KEYS[1], ARGV[1])
end
return current
```

### Sliding-Window Log via Sorted Sets
A fixed window has a boundary-burst flaw: N requests just before a window boundary plus N more just after both pass, allowing 2N requests in a much shorter span than the window implies. A sliding-window log fixes this by recording each request's timestamp as a member of a Redis sorted set (`ZADD`), pruning anything older than `now - window` on every call (`ZREMRANGEBYSCORE`), and counting what's left (`ZCARD`) — a continuously-recomputed rolling cutoff instead of a fixed reset point. Still wrapped in Lua for the same atomicity reason (prune-count-conditionally-add is itself a multi-step sequence).

A subtlety: the sorted-set member can't just be the timestamp — `ZADD` treats a duplicate member as a score *update*, not a new entry, so two requests landing in the same millisecond would silently collapse into one and undercount. The member needs a random suffix (`f"{now_ms}-{uuid4().hex[:6]}"`) to guarantee uniqueness; the score (used for the time-window math) can duplicate freely.

## Three Implementations

| File | Approach | Correctness |
|------|----------|-------------|
| `ratelimit_naive.py` | `INCR` + conditional `EXPIRE` from Python | Broken — orphaned-counter race on crash |
| `ratelimit_lua.py` | Same logic, moved into `rate_limit.lua`, called via `EVAL` | Fixed — atomic on the server |
| `ratelimit_sliding.py` | Sorted-set timestamp log in `sliding_window.lua` | Fixed + more accurate — no boundary bursts |

## Why It Matters

Redis's reputation as "just a cache" undersells it — the same primitives that make it fast (single-threaded execution, in-memory data structures) are what make Lua scripting such a clean fit for atomicity, without needing a separate transaction protocol. Rate limiting is one of the most common production uses of this pattern (API gateways, login attempt throttling, abuse prevention).

## See Also

- [Concurrency and Atomicity](../concepts/concurrency-and-atomicity.md) — how this compares to 2PC and CRDTs as approaches to the same underlying problem
- [Two-Phase Commit](two-phase-commit.md) — a different approach to multi-step atomicity, at the distributed-transaction level rather than single-node scripting
- [CRDT Collaborative Editor](crdt-collaborative-editor.md) — another build centered on avoiding races/conflicts under concurrency, via conflict-free merge semantics instead of locking or atomic execution
