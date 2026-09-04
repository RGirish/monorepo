# Ray Word-Length Pipeline

**Built in:** [Week 20](../weeks/week-20-2026-05-18.md)
**Code:** [distributed-systems/ray-word-length-pipeline](https://github.com/RGirish/monorepo/tree/main/code/distributed-systems/ray-word-length-pipeline)

---

## What It Is

A first hands-on introduction to [Ray](../tools/ray.md), built as a distributed data-processing pipeline: read a large `.jsonl` file of `{"word": "..."}` records, add a `"length"` field to each, and compute the average word length across the whole file — first sequentially, then parallelized across Ray tasks, then with a stateful Ray actor for the aggregate stat, then with deliberate fault injection to explore Ray's retry semantics.

## The Six Stages

1. **Setup** — Python 3.11 venv, `ray` 2.58.0, and a generator (`generate_data.py`) producing 10,000,000 synthetic `{"word": "..."}` lines (random lowercase strings, length 1–15).
2. **Sequential baseline** (`baseline_sequential.py`) — read/parse/annotate/write line-by-line. **13.48s**.
3. **Parallel Ray tasks** (`parallel_ray_tasks.py`) — split the file into `os.cpu_count()` byte-range chunks (snapped to line boundaries), one `@ray.remote` task per chunk, each seeking directly to its own byte range so the driver never loads the file itself. **2.35s** — a 5.7x speedup.
4. **Stats actor** (`parallel_with_stats_actor.py`) — a `StatsActor` accumulating `total_count`/`total_length` as each task reports in, used to compute the average word length across the whole file: **8.0012** (matches the expected midpoint of the uniform 1–15 generator).
5. **Fault tolerance** (`fault_tolerance.py`) — a demo file with one line missing its `"word"` key, processed three ways: naive (that one chunk fails, others unaffected), `max_retries=2, retry_exceptions=True` (retries 3 times total, still fails — deterministic bad data isn't fixed by retrying), and per-line try/except (skips the bad line, keeps the rest of the chunk).
6. **Wrap-up** — see Findings below.

## Findings

### The bottleneck wasn't disk I/O
Isolating raw file I/O (read + rewrite, no JSON) took 0.79s of the 13.48s sequential run — under 6%. The actual cost was **Python-level JSON parse/serialize overhead**, called 10 million times each, not disk throughput. This mattered for the parallelization decision: a genuinely I/O-bound workload wouldn't parallelize well (workers would contend for the same disk), but a CPU/interpreter-overhead-bound one does, since it's spread across independent cores.

### 5.7x speedup, not 10x — heterogeneous cores as the reason
`os.cpu_count()` reported 10 on the Apple M4 test machine, so the file was split into 10 equal-sized chunks — but that CPU is **4 performance cores + 6 efficiency cores**, not 10 uniform cores. Equal-sized work on unequal-speed cores means the E-core chunks finish later, and `ray.get()` waiting on all chunks is gated by the slowest one. This is a concrete, small-scale instance of a general distributed-systems principle: static equal partitioning only gives linear scaling across *uniform* workers — real systems (Spark, Ray Data) favor dynamic/adaptive partitioning specifically to handle this.

### Actor state needed no locking
10 tasks calling `stats_actor.report_chunk.remote(...)` concurrently never raced, because Ray actors serialize their incoming method calls — one at a time, queued — so `self.total_count += count` never interleaves with another call. See [Concurrency and Atomicity](../concepts/concurrency-and-atomicity.md) for how this compares to 2PC, CRDTs, and Redis's Lua-script atomicity as different strategies for the same underlying problem.

### Retries fix transient failures, not bad data
Configuring `max_retries=2, retry_exceptions=True` made Ray retry the failing chunk twice (3 attempts total) — and it failed identically every time, since the corrupted line's `KeyError` is fully deterministic. Retries are the right tool for a worker crash, node preemption, or a flaky network call inside a task; they cannot fix a bug or malformed input, which needs actual error handling in the code (demonstrated by the per-line try/except variant, which processed the other 9 valid lines in the affected chunk instead of failing the whole chunk).

## See Also

- [Ray](../tools/ray.md) — the framework fundamentals (tasks, actors, scheduling, fault tolerance) learned through this build
- [Ray Tasks/Actors and Ray vs. Spark](../synthesis/ray-tasks-actors-and-spark-comparison.md) — conceptual deep dive and Ray vs. Spark/Dask decision guide, worked through before writing any code
- [Concurrency and Atomicity](../concepts/concurrency-and-atomicity.md) — the stats actor's lock-free correctness as a fourth instance of this cross-cutting pattern
