# DuckDB & Vectorized/Embedded OLAP Databases

**Covered in:** [Week 20](../weeks/week-20-2026-05-18.md)

**Sources:**
- [AWS to acquire DuckLabs](https://www.aboutamazon.com/news/company-news/aws-ducklabs)
- [AWS buys DuckLabs to bring DuckDB's embeddable analytics to more enterprises — SiliconANGLE](https://siliconangle.com/2026/08/26/aws-buys-ducklabs-to-bring-duckdbs-embeddable-analytics-to-more-enterprises/)
- [AWS buys DuckLabs, the people behind the popular in-process OLAP database — The Register](https://www.theregister.com/databases/2026/08/26/aws-buys-ducklabs-the-people-behind-the-popular-in-process-olap-database/5292590)
- [AWS: DuckDB will provide 'connective tissue' across the data estate — The Register](https://www.theregister.com/databases/2026/09/01/aws-duckdb-will-provide-connective-tissue-across-the-data-estate/5293304)
- [Best Analytics Database for LLM & AI Agents — MotherDuck](https://motherduck.com/learn/best-analytics-db-llm-ai-agents/)
- [Build an AI Agent with DuckDB as Its Brain — DuckDB Lab](https://duckdblab.org/en/post/duckdb-ai-agent-brain/)
- Interactive first-principles Q&A session working through storage, execution, and parallelism mechanics from scratch

---

## What It Is

DuckDB is an **embedded (in-process), columnar, vectorized OLAP database** — often described as "SQLite for analytics." No server process, no network protocol: it loads as a library directly into your application's process (`import duckdb; con = duckdb.connect()`), and executes analytical SQL queries against in-memory data, local files (Parquet/CSV/JSON), or remote sources (S3) with no separate infrastructure to provision. Created by Hannes Mühleisen and Mark Raasveldt, commercialized through DuckLabs (Amsterdam).

**Context (Aug 2026):** AWS announced it is acquiring DuckLabs — the commercial company, not the open-source project. DuckDB itself stays MIT-licensed and independently governed by the nonprofit DuckDB Foundation, with its creators still steering technical direction. AWS's stated framing is that DuckDB becomes "connective tissue" across its data estate — a fast embeddable query layer sitting on top of S3/Iceberg/etc., not a Redshift replacement.

---

## Row vs. Columnar Storage

Row stores (Postgres, MySQL) keep each row's fields physically together — ideal for OLTP, where a transaction typically reads/writes one whole entity (a single order, a single customer) and benefits from one contiguous disk access plus simple row-level locking/MVCC.

Column stores (DuckDB, ClickHouse, Parquet) group each column together instead. An analytical query like `SELECT AVG(price) WHERE region = 'US'` then reads *only* the columns it needs, skipping every other field entirely — and because values within one column tend to be far more similar to each other than values across a row, columnar data compresses much better too.

The tradeoff is real, not incidental: writing a single row into a column store means touching N separate column segments instead of one contiguous location, which is why row stores remain the right choice for write-heavy, single-entity OLTP workloads. DuckDB deliberately optimizes only for the analytical side and doesn't try to be good at fine-grained transactional updates.

This is also why DuckDB reads Parquet files so natively: Parquet is itself a columnar file format, so querying a `.parquet` file isn't a conversion step, it's a direct fit.

---

## Vectorized Execution: Three Ways to Run a Query

Three execution strategies, in order of what DuckDB deliberately avoided and what it does instead:

**Volcano / iterator model** (classic row-store execution): a query becomes an **operator chain** — small, narrowly-scoped units (`Scan`, `Filter`, `Join`) wired together like stations on an assembly line, each handing its output to the next. Concretely, for `SELECT price FROM orders WHERE region = 'US'`, execution looks like:
```
consumer calls Filter.next()
  → Filter calls Scan.next() to get a row
  → Filter checks: is region == 'US'?
    → no: call Scan.next() again, repeat
    → yes: return this row up to consumer
```
repeated once per row, potentially tens of millions of `next()` calls chained through the tree for a large table.

This is expensive for two compounding reasons. First, because the operator tree is built from generic, polymorphic types at runtime (the engine doesn't know at compile time whether it's calling into a `Scan`, `Filter`, or `Join`), each `next()` call is a **virtual function call**: rather than jumping straight to known code, the CPU dereferences a pointer through a **vtable** (a per-object lookup table of function addresses) to find out where to jump. Second, modern CPUs pipeline many instructions in flight and speculatively execute ahead of a conditional, betting on which way it will go, to keep that pipeline full — hardware branch predictors get quite good at guessing *direct* branches (`if/else`), but an *indirect* jump through a vtable pointer is much harder to predict a target for, and every misprediction forces the CPU to discard speculative work and stall. Multiplied across millions of rows, this adds up.

The resulting loop shape is also too irregular for the compiler to **vectorize** — i.e., to emit SIMD instructions that process several values in one instruction. A simple loop like `for (i = 0; i < n; i++) result[i] = a[i] + b[i];` is easy for a compiler to turn into SIMD; a loop full of virtual dispatch and per-row conditional logic is not.

**Full query compilation (JIT)** (e.g., early Impala/HyPer): compile each query into custom machine code at runtime that fuses all operators into one tight loop, eliminating per-row dispatch overhead entirely. Very fast *execution*, but the compilation step itself adds latency before the query starts — a bad trade for short, ad-hoc, interactive queries where compilation could take longer than running the query.

**Vectorized batch execution** (DuckDB, tracing back to the academic X100/Vectorwise line of research): operators keep the classic pull-based shape, but pass a **batch ("vector") of ~1024–2048 values** at a time instead of one row. A filter operator is called ~1000x fewer times overall, and each call crunches a tight, predictable, SIMD-friendly loop over the batch — most of the CPU efficiency of compiled execution, with none of the upfront compilation cost, using generic operator code that's compiled once, ahead of time.

**Why ~1024–2048, not the whole column?** It's a CPU cache-sizing decision, not an arbitrary constant. Modern CPUs have a small, very fast **L1 cache** (~32–48KB per core) sitting between the CPU and much slower main memory. A batch of 1024 `double` values is ~8KB — comfortably cache-resident even with a few columns in flight. Processing an entire multi-million-row column at once would blow far past cache capacity, forcing constant evictions and round-trips to RAM — reintroducing the exact stalling vectorization exists to avoid. Bigger batches amortize per-batch overhead further but buy almost nothing once cache is already full; ~1024–2048 is the empirical sweet spot.

**Note that vectorization alone isn't DuckDB's differentiator** — ClickHouse, Snowflake, and BigQuery all use vectorized execution too; it's a well-established technique dating to the mid-2000s X100/Vectorwise research. Older row-store engines (Postgres, MySQL, Oracle) haven't retrofitted it wholesale not because it's not worth it, but because it requires being designed in from the ground up — rewriting a mature engine's storage/executor foundation is a different order of undertaking than adding a feature (partial retrofits do exist, e.g. Postgres extensions like Citus/pg_analytics, but the core engine stays row-oriented). And SQLite — the other half of DuckDB's "SQLite for analytics" tagline — solves the *embedded deployment* problem but is itself row-oriented internally, tuned for OLTP-shaped access, not analytical scans. DuckDB's actual differentiator is that nobody had previously put a real columnar/vectorized analytical engine and SQLite's zero-server, zero-config deployment model into the *same* artifact (see below).

---

## Embedded / In-Process Architecture

DuckDB has no server process — it's a library loaded directly into your application's address space, same deployment story as SQLite. Compare to a client-server database (even over `localhost`): every query still crosses a real boundary — `send()`/`recv()` syscalls (context switches into the kernel), the OS copying data into/out of socket buffers, the server process being scheduled, and results being **serialized** into a wire protocol on the way out and **deserialized** back into usable objects on the way in. This serialization step is a real tax specifically for analytics: Postgres's wire protocol, for instance, is row-oriented, so a server holding results as efficient internal columnar batches still has to convert them into row-shaped wire messages, and the client converts them back. For an OLTP query returning a handful of rows this is trivial; for an analytical query returning millions of rows into a DataFrame, that serialization/copy tax can dominate total query time.

The deepest reason this matters: two separate processes have **separate address spaces** — a pointer in one process is meaningless in another, so data *must* be copied across that boundary, no way around it. Being in-process removes the boundary entirely: DuckDB can hand back a result as an **Apache Arrow buffer**, a pointer directly into memory your own process already owns — zero serialization, zero copying. This is also why the result can flow straight back into an AI agent's reasoning loop without paying a tax on every tool call.

---

## Parallelism: Morsel-Driven Execution

To use multiple CPU cores on one machine, DuckDB (following "morsel-driven parallelism," from HyPer research) avoids statically splitting the table into N equal chunks for N threads — because real query cost is rarely uniform across rows (a filter might match 90% of one chunk and 2% of another), and with static partitioning, the *slowest* thread determines total query time while faster threads sit idle.

Instead, DuckDB splits the table into many small **morsels** (~100K rows) placed in a shared work queue. Each thread pulls a morsel, fully processes it (scan → filter → project, using vectorized batches internally), then grabs the next available morsel — dynamic load balancing via work-stealing, based on actual completed work rather than an upfront guess. Two nested granularities: **morsels** (~100K rows, the unit of cross-thread parallelism) containing many **vectors** (~1024–2048 rows, the unit of vectorized execution within a thread).

**Pipeline breakers:** operators like `Filter` process each morsel independently and pass it straight along. `GROUP BY` and `JOIN` cannot — they need to see data across many (or all) morsels before producing correct output. For `GROUP BY`, each thread builds its own local hash table while processing its assigned morsels (no cross-thread coordination needed during this phase), typically **hash-partitioned by group key** so the eventual merge can also run in parallel — thread A merges partitions 0–15 across every thread's local table, thread B merges 16–31, etc. But there's still a hard **synchronization barrier**: no merging can start until *every* thread finishes all its assigned morsels, so a skewed workload leaves fast threads idle, waiting on the slowest one, before the next pipeline stage can proceed.

---

## Where DuckDB Stops Scaling

Running out of CPU cores doesn't break DuckDB — it degrades *gracefully*, just cycling more morsels through fewer available threads, taking longer without failing. The real hard limits are different:

- **In-memory working-set size for pipeline breakers.** A hash join's build side, a `GROUP BY`'s hash table, a sort buffer — these need to fit in RAM for the vectorized/morsel design's cache-speed assumptions to hold. When they don't, DuckDB spills to disk: an order-of-magnitude cliff, not a gentle slowdown, since disk-based random access defeats the entire cache-locality premise. (DuckDB can still stream simple scans over data larger than RAM directly from S3/Parquet — it's specifically join/aggregation *build-side* state that must fit in memory.)
- **Finite single-machine resources.** One box has a ceiling on RAM/disk/cores; distributed systems (ClickHouse cluster mode, Snowflake, BigQuery) scale by adding machines instead, at the cost of having to shuffle data across the network for the same kind of `GROUP BY`/`JOIN` merge — the network becomes the new synchronization barrier.
- **Single-writer concurrency**, orthogonal to data size entirely — like SQLite, one process writes at a time, so a workload needing many concurrent writers (a multi-tenant OLTP backend) is a wall this architecture doesn't address regardless of how small the data is.

The trigger for going distributed is **working-set-per-operator exceeding one machine's RAM**, or **needing many concurrent writers** — not raw data volume or core count on their own.

---

## Why It Fits Agentic/AI Workloads

Every property above compounds into a good fit for how AI agents actually work:

- **Ephemeral, zero-config instances** — `duckdb.connect(':memory:')` inside a single tool call, no infrastructure to provision or tear down, viable even when an agent spins up hundreds of these per session.
- **Zero-copy result handoff** — because it's in-process, results return as Arrow/DataFrame objects with no serialization tax, which matters when a tool call's latency gates how fast an agent can iterate.
- **Direct querying of Parquet/S3, no ETL step** — an agent handed a data lake can point DuckDB straight at it.
- **Graceful degradation on bad agent-generated SQL** — an agent's own (possibly inefficient) query just runs slow on one machine, rather than risking a shared multi-tenant cluster.
- **MotherDuck** extends the same properties to a *hosted*, persistent instance an agent can self-provision via one API call, for when state needs to outlive a single process.

This is the concrete mechanism behind AWS's "connective tissue" framing for the DuckLabs acquisition: DuckDB isn't positioned to replace distributed warehouse-scale systems, but to sit as the fast, embeddable layer between an agent (or any application) and wherever the data actually lives.

---

## See Also

- [Vector Database](../builds/vector-db.md) — a different database-systems build in this repo (in-memory flat-index similarity search rather than columnar OLAP), for contrast in what "database" means depending on the workload it's built for
- [Feature Engineering](feature-engineering.md) — the data-transformation side of the pipeline that a fast query layer like DuckDB often feeds into
