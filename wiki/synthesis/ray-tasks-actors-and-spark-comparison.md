# Ray's Computing Model: Tasks, Actors, Scheduling — and When to Use Ray vs. Spark

**Filed from:** conversation exploring Ray fundamentals ahead of, and during, the week 20 build (a distributed data-processing pipeline)
**Related pages:** [Ray](../tools/ray.md), [Ray Word-Length Pipeline](../builds/ray-word-length-pipeline.md), [Concurrency and Atomicity](../concepts/concurrency-and-atomicity.md)

---

## The Two Primitives

Ray's entire programming model rests on two building blocks, both created by decorating normal Python with `@ray.remote`:

**Tasks** — stateless functions.
- Each call starts fresh; nothing persists between invocations, even if the same worker process happens to run two calls back to back.
- "Stateless" refers to memory, not to ordering: tasks *can* depend on each other. Passing one task's result (an `ObjectRef`, a future) as another task's argument creates a data dependency, and Ray won't schedule the downstream task until the upstream one resolves. Chaining tasks this way builds an implicit DAG at runtime — you don't have to declare the graph structure yourself.

**Actors** — stateful classes.
- `MyActor.remote()` spins up one dedicated process for that instance. Every subsequent method call on that handle runs in the same process and sees whatever state prior calls left behind — ordinary instance variables persist across calls the way they would in a normal long-lived Python object.
- Calls to one actor are also serialized (queued, run one at a time), so there's no race between them.
- State is private per instance, not shared globally: a second `MyActor.remote()` is a separate process with separate memory. Two actors never see each other's state unless you explicitly wire that up (e.g. both talking to a third actor that owns shared state).

**A common misconception worth correcting: the GIL is not what's limiting parallelism here.** The Global Interpreter Lock only serializes execution *within one process* across *threads*. Ray sidesteps it entirely — each task/actor gets its own separate OS process with its own separate interpreter, not a thread sharing one interpreter. That's exactly why Ray achieves real CPU parallelism in Python where plain `threading` couldn't. Confirmed empirically in the [Ray Word-Length Pipeline build](../builds/ray-word-length-pipeline.md): 10 concurrent tasks got a genuine ~5.7x wall-clock speedup, which a GIL-bound approach could never produce.

## How Scheduling Actually Works

Given a graph of tasks/actors with dependencies, Ray does automatically:
- **Dependency-driven execution order** — a task becomes eligible to run only once all its input `ObjectRef`s are resolved, and independent branches run in parallel with no explicit "wait for both" code required.
- **Locality-aware placement** — the scheduler prefers running a task on a node that already holds its input data locally, to avoid shipping large objects over the network, and load-balances across nodes with free resources (CPUs/GPUs/custom resources).

What it does *not* do: compute a globally optimal schedule ahead of time. Ray's scheduling is **decentralized and greedy/reactive** — each node runs its own scheduler ("raylet") making local placement decisions as tasks become ready. This is a deliberate contrast with Spark (below), which plans its whole DAG upfront.

**Empirical consequence — equal-sized chunks assume equal-speed workers.** In the [Ray Word-Length Pipeline build](../builds/ray-word-length-pipeline.md), a 10M-line file was split into `os.cpu_count()` (10) equal-sized chunks on an Apple M4 — which has 4 performance cores and 6 efficiency cores, not 10 uniform cores. The result was a 5.7x speedup, not 10x: `ray.get()` waiting on all 10 tasks is gated by the slowest one, and the chunks that landed on E-cores took longer despite being the same size. Ray's decentralized scheduler placed the tasks without being told anything about core speed — the mismatch was entirely in how the *work* was partitioned (uniformly) versus how the *hardware* was shaped (non-uniformly). This is a small-scale instance of why real distributed systems favor dynamic/adaptive partitioning over static equal splits.

## Fault Tolerance: Retries vs. Real Fixes

Ray distinguishes two failure categories:
- **System-level failures** (a worker process or node crashing) are retried automatically — `max_retries` defaults to 3, no configuration needed.
- **Application-level exceptions** (your own code raising an error) are *not* retried by default. Opting in requires `retry_exceptions=True` alongside `max_retries` on the task.

The critical nuance, demonstrated in the [Ray Word-Length Pipeline build](../builds/ray-word-length-pipeline.md): retries only help when the failure is **non-deterministic** — a flaky network call, a transient lock timeout, a node getting preempted. Retrying a task against permanently malformed input data (e.g. a JSON record missing an expected key) just reproduces the identical exception every time; the build's fault-injection test configured `max_retries=2, retry_exceptions=True` on a task processing one corrupted line, observed 3 total attempts (all logged by the raylet), and all 3 failed identically. The actual fix for bad data is defensive handling inside the task itself (catching the error per-record and skipping/logging it), not a retry policy — retries and input validation solve different problems and neither substitutes for the other.

## Ray vs. Spark vs. Dask

The core split: **Spark is a distributed data engine; Ray is a distributed Python runtime.**

| | Spark | Ray |
|---|---|---|
| Core abstraction | DataFrames/SQL — declare *what* transform you want | Arbitrary Python tasks/actors — no fixed data abstraction |
| Planning | Catalyst optimizer plans the whole DAG upfront (join order, partitioning) before running | Dynamic — DAG emerges at runtime as `ObjectRef`s get passed around; no upfront global plan |
| Runtime | JVM-based, Python is a wrapper (py4j) | Native Python |
| Task granularity/latency | Coarse-grained batch stages, ~100ms+ scheduling overhead per task | Fine-grained, sub-ms to low-ms scheduling |
| State | No real equivalent to actors — transformations are stateless by design | Actors give first-class stateful, long-lived workers |
| Best fit | SQL/DataFrame-shaped batch ETL over huge structured/semi-structured datasets, data warehousing | Dynamic/imperative control flow, ML training/tuning (Ray Train/Tune), RL (RLlib), model serving (Ray Serve), simulators, agentic pipelines |

**Dask** sits closer to Spark's use case but is Python-native — mostly a drop-in scale-out for pandas/numpy. It lacks Ray's actor model as a first-class concept and has a much thinner ML/serving ecosystem, so it's a good fit for "scale my existing pandas workflow" but not for stateful services or RL-style workloads.

## Decision Guide

| Situation | Recommendation |
|---|---|
| Huge structured/semi-structured dataset, SQL-shaped transforms (joins, aggregations, ETL) | Spark |
| Scaling an existing pandas/numpy workflow with minimal rewrite | Dask |
| Dynamic/imperative workload where the task graph isn't known in advance | Ray |
| Need stateful, long-lived workers (simulators, parameter servers, model replicas, RL environments) | Ray (actors) |
| ML training, hyperparameter search, RL, model serving, agentic pipelines | Ray (Train/Tune/RLlib/Serve) |
| Need low-latency, fine-grained task scheduling | Ray |
| Regulated/interpretable batch analytics at data-warehouse scale | Spark |
