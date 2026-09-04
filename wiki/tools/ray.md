# Ray

A general-purpose distributed computing framework for Python: write mostly-normal Python, and Ray schedules it across CPU cores (or machines) via two primitives. Everything in the wider Ray ecosystem (Ray Data, Ray Train, Ray Tune, Ray Serve, RLlib) is built on top of this same core.

## The Two Primitives

**Tasks** — stateless functions, marked `@ray.remote`. Each call starts fresh; nothing persists in memory between invocations, even across two calls on the same worker process. "Stateless" is about memory, not independence: a task's output (an `ObjectRef`, a future) can be passed as another task's input, and Ray won't schedule the downstream task until the upstream one resolves. Chaining tasks this way builds an implicit DAG at runtime — the dependency graph doesn't need to be declared upfront.

**Actors** — stateful classes, marked `@ray.remote`. `MyActor.remote()` spins up one dedicated process for that instance; every subsequent method call on that handle runs in the same process and sees state left behind by prior calls, the way a normal long-lived Python object would. Calls to one actor are also serialized — queued and run one at a time — so concurrent callers never race on the actor's internal state, no locking required. State is private per instance: a second `MyActor.remote()` is a separate process with separate memory, and two actors never see each other's state unless something explicitly wires that up.

**GIL note:** the Global Interpreter Lock does not limit parallelism across Ray tasks/actors, because each one runs in its own separate OS process with its own separate interpreter — not as threads sharing one process. That's precisely what lets Ray get real CPU parallelism out of Python where plain `threading` couldn't.

## Scheduling

Given a task graph, Ray automatically handles:
- **Dependency-driven execution order** — a task becomes eligible only once all its input `ObjectRef`s resolve; independent branches run in parallel with no explicit "wait for both" code.
- **Locality-aware placement** — prefers running a task on a node that already holds its input data locally (to avoid shipping large objects over the network), and load-balances across nodes with free resources.

This is **decentralized and greedy/reactive**, not a global optimizer: each node runs its own scheduler (a "raylet") making local placement decisions as tasks become ready, in contrast to a system like Spark that plans its whole DAG upfront. One practical consequence: splitting work into *equal-sized* chunks only gives close-to-linear scaling across *equally powerful* workers. On heterogeneous hardware — e.g. Apple Silicon's performance + efficiency core split — equal-sized chunks create stragglers on the slower cores, since a final `ray.get()` on all of them waits for the slowest. See the [Ray Word-Length Pipeline build](../builds/ray-word-length-pipeline.md) for a concrete measurement of this effect.

## Fault Tolerance

Ray retries **system-level** failures (a worker process or node crashing) automatically — `max_retries` defaults to 3 for these, no configuration needed. Retrying on exceptions *raised by your own code* is opt-in via `retry_exceptions=True`, and it only helps when the failure is non-deterministic (a flaky network call, a transient timeout) — retrying a task against permanently bad input data just reproduces the same exception every time. The fix for bad data is defensive handling in the code itself (e.g. catching and skipping a malformed record), not retries.

## When to Use Ray vs. Spark/Dask

See [Ray Tasks/Actors and Ray vs. Spark](../synthesis/ray-tasks-actors-and-spark-comparison.md) for the full comparison and decision guide. Short version: Spark is a distributed *data engine* (declarative DataFrame/SQL transforms, planned upfront); Ray is a distributed *Python runtime* (arbitrary imperative tasks/actors, dynamic DAGs) — reach for Ray when the workload is Python/ML-native, needs stateful long-lived workers, or needs fine-grained low-latency scheduling.

## See Also

- [Ray Word-Length Pipeline](../builds/ray-word-length-pipeline.md) — hands-on build: a parallel data-processing pipeline demonstrating tasks, an aggregating actor, and fault tolerance
- [Ray Tasks/Actors and Ray vs. Spark](../synthesis/ray-tasks-actors-and-spark-comparison.md) — deeper comparison and decision guide
- [Concurrency and Atomicity](../concepts/concurrency-and-atomicity.md) — how actor call serialization compares to 2PC, CRDTs, and Redis Lua scripting as strategies for the same underlying problem
- [DuckDB & Vectorized/Embedded OLAP Databases](duckdb.md) — a different distributed/parallel compute paradigm (declarative vectorized query execution vs. imperative task/actor scheduling), for contrast
