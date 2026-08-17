# Agent Evaluation

**Covered in:** [Week 19](../weeks/week-19-2026-05-11.md)

**Sources:**
- [Agent Evaluation: A Detailed Guide — Cameron Wolfe, Deep (Learning) Focus](https://cameronrwolfe.substack.com/p/agent-evals)
- [LLM Evaluation Framework: Trajectories vs. Outputs — LangChain](https://www.langchain.com/resources/llm-evaluation-framework)
- [Agent Evaluation — Metrics, Strategies & Examples — Langfuse cookbook](https://langfuse.com/guides/cookbook/example_pydantic_ai_mcp_agent_evaluation)
- [Strands Agents Evals SDK docs](https://strandsagents.com/docs/user-guide/evals-sdk/) — used as a case study for how the theory below gets implemented concretely; see [Strands Agents](strands-agents.md#week-19--evals-sdk) for the framework-specific mapping

---

## What It Is

Evaluating an autonomous agent — something that takes a task and decides for itself how many steps to take, which tools to call, and in what order — rather than evaluating a single LLM completion against a reference answer. The central problem: an agent can reach the objectively correct final answer via an unreliable, unsafe, or wildly inefficient path, and destination-only scoring is completely blind to that. Everything below follows from taking the *path*, not just the endpoint, seriously.

---

## Why Agent Eval Is a Different Problem

A normal LLM eval sends one prompt, gets one completion, scores it against a reference. An agent is stochastic at every decision point — it can take a different number of steps, call different tools, or even reach a different final answer on the same input across runs. A grader that only checks "is the final answer correct" misses:

- **Inefficiency** — hundreds of unnecessary tool calls and backtracking on the way to a correct answer, with real cost/latency consequences
- **Unsafe process** — calling a destructive or unauthorized tool along the way and getting lucky with the outcome
- **Brittle process** — a hallucinated intermediate result that happened to get "corrected" by luck; the same input tomorrow may not be so lucky

---

## Trajectory vs. Outcome Evaluation

**Outcome evaluation** scores the final answer. **Trajectory evaluation** scores the sequence of tool calls — which tools, in what order, with what arguments — against an expected path. Neither replaces the other; they answer different questions.

### Sequence-matching strategies

When comparing an actual trajectory to an expected one, three strictness levels exist:

- **Exact-sequence match** — actual calls must equal the expected list exactly, same order, nothing extra
- **Ordered-subset match** — expected calls must all appear in the right relative order, but extra calls in between are fine
- **Unordered-set match** — expected calls must all appear somewhere, order doesn't matter

The right strictness depends on the domain, not a fixed default. Read-only, order-independent tools tolerate unordered-set or ordered-subset matching. Exact-sequence match is warranted when tools have **hard state dependencies** — e.g. `reserve_item → charge_card → confirm_order` — where reordering produces a genuine correctness bug (charging before reserving) even though every individual call was safe and the full set of expected calls appears.

### Per-call vs. per-sequence granularity

Trajectory matching operates on the *whole sequence's shape*. A separate, finer-grained layer checks *individual calls*:
- **Tool-selection accuracy** — was this one call justified given available tools and prior context, independent of the overall sequence
- **Tool-parameter accuracy** — are this call's argument values actually grounded in conversation history, or fabricated

A trajectory can pass a sequence-match check while an individual call inside it has hallucinated arguments — sequence-shape and per-call-fidelity are independent failure modes, so real systems check both.

---

## LLM-as-Judge

The dominant pattern for evaluating anything that can't be reduced to a deterministic rule ("was this explanation actually helpful," "was the tone appropriate"): a capable model grades another model's output against an explicit rubric.

### Decomposition and graduated scales

Two design choices materially improve judge reliability, not just detail:

1. **Score multiple orthogonal dimensions separately** (accuracy, coherence, tone, safety) instead of asking for one holistic score. A single scalar forces the judge to silently invent and apply an unstated weighting between incommensurable qualities (correct-but-curt vs. warm-but-wrong could both land at 6/10 for different reasons) — that hidden aggregation function is where most judge variance comes from. Decomposed dimensions remove the hidden weighting.
2. **Use a graduated, anchored scale** (e.g. 0.0/0.5/1.0 with a description at each level) rather than binary pass/fail. Binary forces an arbitrary threshold on what's actually a continuous quality gradient — an 80%-helpful run and a 20%-helpful run both just become "fail." An anchored scale gives the judge a concrete reference point at each level, which is what reduces run-to-run variance.

### Distinct judge categories, not just more rubrics

Not every LLM-as-judge check is a quality opinion:
- **Safety-classification gates** (harmfulness, refusal, stereotyping) are binary content-safety checks, not graduated quality judgments — partial credit doesn't make sense for "did it say something dangerous."
- **Faithfulness / grounding checks** verify a response against conversation history for hallucination, closer to RAG-style grounding verification than a quality rubric.
- **Multi-agent interaction judging** — in systems with multiple agents handing off to each other, a judge can score the handoffs themselves (dependencies, message flow) across a sequence of interactions, conceptually closer to trajectory evaluation than single-turn output scoring.

---

## Deterministic Checks Layered with LLM Judges

LLM judges are flexible but slow and relatively expensive per call. Deterministic, code-based checks (exact match, substring match, "was tool X called," "does state variable Y equal Z") are near-instant and free, but only catch what can be fully specified in advance.

The natural layering mirrors the software testing pyramid: many cheap deterministic checks run constantly (dev-time, every commit, every CI run); costlier LLM-judge checks run less often (scheduled, or on-demand). This extends into the deployment environment too — deterministic checks are cheap enough to run **inline on every live request** as real-time guardrails (blocking a call before it executes), while LLM judges are too expensive to run on 100% of production traffic and instead run on a **sampled subset**, after the fact, as an audit layer rather than a gate. Same cost logic, extended from dev-time into runtime: deterministic checks scale to "every run, real-time, prevention"; LLM judges scale to "some runs, after the fact, diagnosis."

---

## Building Eval Sets & Ground Truth

Test cases pair an input with an expected output and/or expected trajectory. Two ways to build the set:

- **Manual annotation** — a human writes realistic tasks and their correct answers/tool sequences
- **Synthetic/automated generation** — an LLM drafts candidate cases from a spec (tool definitions, docs), which a human then reviews and prunes

Relying entirely on synthetic generation has two specific failure modes, not just "lower quality":

1. **Typical-case bias** — a generating LLM produces the median case, not the tail. Real failures cluster in the tail (weird phrasing, conflicting instructions, adversarial input, domain-specific edge cases from real incidents) — exactly what synthetic generation under-samples.
2. **Circularity** — if the case-generating model shares blind spots with the model powering the agent (same family, similar training), it won't think to generate the case that exposes its own weakness. Eval scores look great while missing the failure mode that actually matters.

The practical pattern: synthetic generation for volume and breadth, human review specifically for the tail and adversarial cases the generator wouldn't think to write.

---

## Production Monitoring & Observability

Everything above is *offline* eval — a fixed test suite run before shipping. Teams that eval thoroughly pre-launch and then stop monitoring commonly see quality degrade within 30–60 days, even with zero code changes, from two mechanisms:

- **Input distribution drift** — the population of users and their query patterns shift out from under a system validated against a snapshot; new user segments or new usage patterns for existing users go untested.
- **Silent dependency drift** — the LLM provider refreshes the model behind a version tag, an upstream tool/API changes its schema or data freshness, an external index goes stale — none of which shows up as a diff in your own code.

Both are caught the same way: instrumenting live traffic with trace/span-based observability (the same substrate used for offline trajectory scoring), sampling a slice through LLM judges, and watching for score drift over time as your production traffic distribution diverges from your static eval set.

### Diagnosis vs. scoring

A related but distinct capability: instead of producing a *score*, an LLM can read a trace and produce a *diagnosis* — classifying the failure type, tracing the causal chain (a root cause propagating into downstream symptoms), and recommending a specific fix (prompt change, tool-description change). Same underlying mechanism as an LLM judge, different output contract: "why did this fail and what should change" rather than "how good was this." This is the natural complement to drift monitoring — monitoring tells you quality is degrading, diagnosis tells you why.

---

## Adversarial (Red-Team) Evaluation

A genuinely different category from everything above: instead of a fixed test input scored against a rubric, the input itself is a **closed-loop attacker** that reads the agent's response and adapts its next move. This flips the premise from "does the agent behave well on realistic inputs" to "can an adaptive adversary force it to misbehave at all" — optimization *against* the agent's defenses, not measurement of static behavior.

Published attack techniques with this adaptive character include gradual escalation with backtracking on refusal, iterative prompt refinement against judge feedback, and hiding a harmful request among benign ones in a single scaffolded query. Attack success is itself scored by an LLM judge, typically with a deliberately conservative breach threshold (partial engagement counts as a breach, not just full compliance).

---

## Fault-Injection (Chaos) Testing

Borrowed from systems engineering (the Chaos Monkey lineage), applied to agent tool calls: deliberately break the *environment* underneath the agent — a tool call times out, a response comes back truncated or corrupted — and measure resilience, not correctness on a clean run. This is orthogonal to red-teaming: red-teaming attacks via malicious *input*, chaos testing attacks via broken *infrastructure*.

This requires its own evaluators, since "failure happened" becomes a controlled independent variable rather than something the test setup is trying to avoid:
- **Goal success** — strict binary; partial completion still scores zero
- **Partial completion** — the graduated counterpart; continuous fraction of sub-goals achieved even if the overall task failed
- **Failure communication** — does the agent transparently report a tool failure, or fabricate a result to paper over it
- **Recovery strategy** — does a retry show any sophistication (backoff, fallback, escalation) versus blindly repeating the same failed call

---

## Simulation as Input Generation

Everything above assumes a completed trace already exists to score. Simulation solves the upstream problem: how do you *get* a realistic multi-turn trace, or a trace involving a tool that doesn't exist yet or is unsafe to call in a test?

- **User simulation** — an LLM plays a persona (traits, goals, communication style) across a real multi-turn conversation with the agent, deciding turn-by-turn what to say and when its goal is satisfied. This produces dynamic, realistic multi-turn traces rather than scripted ones — structurally similar to red-teaming's adaptive loop, but optimizing for realistic cooperative behavior instead of breach.
- **Tool simulation** — real tool signatures are registered, but execution is replaced by an LLM generating schema-valid fake responses, with shared state tracked across calls for consistency. Used when the real API doesn't exist yet, is unsafe to call in a test, or needs to be deterministic/controllable for the eval.

---

## Summary: The Full Technique Landscape

| Category | Answers | Input type |
|---|---|---|
| Trajectory / outcome scoring | Did it do the right thing, the right way? | Fixed realistic case |
| LLM-as-judge (decomposed, graduated) | How good was this, on which dimensions? | Fixed realistic case |
| Deterministic checks | Did a specific, pre-specifiable thing happen? | Fixed realistic case |
| Production monitoring + diagnosis | Is quality drifting, and why? | Live traffic |
| Red-teaming | Can an adversary break this? | Adaptive, adversarial |
| Chaos testing | Is this resilient when its environment breaks? | Adaptive, environmental |
| Simulation | How do I even get a realistic trace to score? | Generated upstream of scoring |

The first three assume you already have a trace and are asking how good it is. Red-teaming and chaos testing turn failure into a deliberately injected independent variable. Simulation solves the prior problem of producing a trace at all.

---

## See Also

- [Strands Agents](strands-agents.md#week-19--evals-sdk) — case study: how this framework's `evals-sdk` implements nearly every technique above concretely
- [Prompt Engineering](prompt-engineering.md#6-iteration-and-evaluation--dont-over-engineer) — the single-prompt-level precursor to this: evals as the feedback loop for iterating on a prompt, before agent-level trajectory concerns exist at all
- [Context Engineering](context-engineering.md) — production agents evaluated here are also managing context; evaluation and context management are two sides of running an agent reliably over long sessions
