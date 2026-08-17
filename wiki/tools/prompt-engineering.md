# Prompt Engineering

**Covered in:** [Week 18](../weeks/week-18-2026-05-04.md)

**Sources:**
- [Prompt engineering best practices for 2026 — Claude by Anthropic](https://claude.com/blog/best-practices-for-prompt-engineering)
- [What is prompt engineering—definition and best practices? — Educative](https://educative.io/blog/what-is-prompt-engineering)

---

## What It Is

Prompt engineering is the practice of designing instructions that reliably steer a model toward a desired output. The 2026 framing in both sources: it has shifted from "clever tricks" toward writing a clear spec — the same model can produce dramatically different quality results depending on how clearly intent, constraints, and format are specified.

---

## Key Ideas

### 1. Being Explicit and Specific

Modern models don't reward vagueness — state exactly what's wanted rather than trusting the model to infer it. Three sub-parts: **explicit** (ask directly for what you want, e.g. comprehensiveness), **context/motivation** (explain *why* a constraint exists, not just the rule itself), and **specificity** (constraints, audience/goal, structure, all stated up front).

Explaining the *why* behind a rule matters because the model has to generalize that rule to situations the prompt didn't explicitly cover. Given only the bare rule, the model infers its own justification — which can be wrong and misfire on edge cases. Given the real reason, the model generalizes correctly. Example: "don't use emoji" vs. "don't use emoji — this is a formal legal document." The bare rule leaves casual contractions untouched; the reasoned version correctly extends "formal tone" to everything else in the output too.

### 2. Examples (Zero-shot vs. Few-shot)

**Zero-shot** — instructions only, no examples; fine for simple, well-understood tasks. **Few-shot** — 1–3 input/output examples demonstrating the desired behavior. Anthropic's claim: demonstrations work better than descriptions for format requirements, and models pay close attention to the *details* in examples, not just their gist.

This creates a common self-inflicted bug: if a written instruction and an example contradict each other (e.g., "always respond in a numbered list" but the one example given is a bulleted list), the model doesn't cleanly pick one — the conflict introduces run-to-run nondeterminism, since examples are pattern-matched roughly as strongly as instructions are followed. Examples are part of the spec, not just illustration; a mismatch between instructions and examples is a bug to fix before it ships.

### 3. Chain-of-Thought (CoT) Reasoning

Forcing a model to externalize intermediate reasoning steps improves the final answer's accuracy, especially on multi-step problems. The mechanism: models generate autoregressively, one token at a time, each conditioned on everything before it. Without CoT, the model has to compress a potentially multi-step answer into a single "leap." With CoT, each reasoning token becomes grounding for the next, giving the model more computation steps before committing to an answer — the model equivalent of showing your work instead of blurting the answer. Current Claude models support **extended thinking** as a distinct mechanism for this, rather than relying purely on "think step by step" phrasing inline in the response text.

### 4. Output Control: Format Specification and Prefilling

**Format specification** — state the desired format explicitly and positively ("respond in JSON with keys X, Y, Z") rather than as a prohibition ("don't respond in prose").

**Prefilling** — write the *start* of the model's response yourself (e.g., open with `{` to force JSON), and the model generates only the continuation. Mechanically: the model is autoregressive and cannot revise tokens already in its own context — it can't tell the difference between a token it generated itself and one inserted by the developer. So the prefilled tokens are a genuine hard constraint (they can't be un-written), but everything generated *after* them is still ordinary probabilistic sampling: the model can still produce malformed continuations (bad JSON, unclosed braces) — deviating just requires a much less probable continuation, since it must stay coherent with what's already committed. Prefilling is therefore a strong probabilistic bias toward the format, not a deterministic guarantee — in production it's paired with parsing/validation on the receiving end, not relied on alone. (A genuine hard guarantee requires a different mechanism: constrained/grammar-based decoding that restricts the token vocabulary itself at each generation step.)

### 5. Prompt Chaining / Decomposition

Instead of one prompt handling an entire multi-step task, split it into separate calls where each step's output becomes the next step's input. Anthropic frames this explicitly as a **latency-for-accuracy tradeoff**.

Two benefits beyond what CoT-within-one-response gives:
- **Context isolation** — a later step doesn't need the intermediate reasoning tokens (or raw source material) from an earlier step once that step's distilled output is available; carrying it forward can dilute or confuse the next step's context and wastes context length.
- **Per-step checkpoints** — errors don't silently compound across an entire reasoning trace the way they can within one long CoT generation. Each step's output can be validated or corrected before it reaches the next step.

Example — a three-step chain for a legal risk memo: (1) extract liability/indemnification/termination clauses from a contract, (2) rank the extracted clauses by financial risk, (3) draft an executive summary from the risk ranking. Step 3 never sees the original contract — only step 2's distilled output.

### 6. Iteration and Evaluation — Don't Over-Engineer

Treat prompt design as a repeatable process: track correctness, run-to-run consistency, and cost via testing/evals — see [Agent Evaluation](agent-evaluation.md) for how this generalizes once the system being evaluated is a multi-step agent rather than a single prompt. Anthropic's closing principle is a check on everything above: start simple, add one technique at a time, and only add a technique when it demonstrably fixes a problem being hit. Match the technique to the specific failure symptom:

- **Inconsistent output across runs** (format/quality varies run to run) → the model lacks enough constraint to converge → add **examples** or **prefilling**
- **Wrong answers on complex, multi-step problems specifically** (not just inconsistent — consistently under-reasoned) → the model needs scratch space → add **CoT**
- **Errors compounding across a long, multi-part task** even with good CoT → need checkpoints → add **chaining**

Reaching for a heavier technique that doesn't match the actual symptom (e.g., CoT for a formatting problem) adds tokens without fixing anything.

---

## Broader Technique Landscape

Beyond the core techniques above, a wider set of named prompting/reasoning techniques exists. They divide cleanly by *what they require to run*:

**Single-prompt (just instruction design, one generation, no external code)**
- **Step-Back Prompting** — derive a general principle first, then apply it to the specific question
- **Self-Refine (weak form)** — draft → critique → revise within one continuous response

**Fixed multi-call pipeline (static sequence of calls, no dynamic branching — this is what prompt chaining above already is)**
- **Least-to-Most Prompting** — decompose into sub-problems, solve in increasing difficulty, each building on the last
- **Meta-prompting** — one call generates a prompt, a second call uses it
- **Self-Refine (proper form)** — separate draft/critique/revise calls

**Requires real orchestration (external code managing loops, tool execution, branching/backtracking, or aggregation across independent runs — where "agentic" starts)**
- **ReAct** — interleaves reasoning with real tool calls; needs a loop since tool results aren't knowable in advance
- **Program-of-Thought / PAL, ReWOO** — model writes/plans code or tool calls that get executed externally
- **Self-Consistency** — samples the same prompt multiple independent times, takes a majority vote; requires genuinely independent generations plus external aggregation, not one stream simulating multiple tries
- **Tree of Thought (ToT) / Graph of Thought (GoT)** — explore multiple reasoning branches (and, for GoT, let them merge/reference each other), with external search logic driving which branches to expand, prune, or merge
- **Reflexion** — persists learned feedback across separate task attempts over time, requiring external memory storage
- **Automatic Prompt Engineering (APE)** — an external eval harness generates and scores candidate prompts against real data
- **Multi-agent debate** — multiple separate model instances/threads exchange and critique each other's answers

The dividing line: a technique needs orchestration if it depends on (a) real-world information the model can't have in advance, (b) truly independent sampling for statistical robustness, or (c) control flow decided by something other than the model's own next-token prediction.

---

## Relationship to Context Engineering

[Context Engineering](context-engineering.md) explicitly frames itself as prompt engineering's natural evolution: prompt engineering optimizes a single discrete instruction, while context engineering manages what information exists in an agent's context window across an entire multi-turn session. See that page's [Relationship to Prompt Engineering](context-engineering.md#relationship-to-prompt-engineering) table for the direct comparison.

---

## See Also

- [Context Engineering](context-engineering.md) — the multi-turn, whole-context-window generalization of prompt engineering
- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — the autoregressive, next-token-conditioned-on-everything-before-it mechanism that explains why chain-of-thought and prefilling work the way they do
- [Agent Evaluation](agent-evaluation.md) — evaluation theory and technique for multi-step agents, building on the "iteration and evaluation" principle above
