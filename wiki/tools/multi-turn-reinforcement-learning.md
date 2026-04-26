# Multi-turn Reinforcement Learning and Evaluation

First covered: Week 14 (2026-04-06)

---

## The Three ML Paradigms

### Supervised Learning
Requires a ground-truth label for every training example. Breaks down when:
- Getting labeled data is impossible or requires a perfect oracle (e.g., labeling every chess position)
- The "correct" action depends on future state that isn't known at label time

### Unsupervised Learning
Finds statistical structure in raw data without labels. Breaks down when:
- You need to optimize toward a *goal* rather than find *patterns*
- Structure alone doesn't tell you which cluster or pattern *wins*

### Reinforcement Learning
The right tool when all three hold simultaneously:
- **Sequential decisions** — each action affects future options
- **Delayed feedback** — you won't know if an action was good until much later
- **No oracle** — you can't pre-specify correct behavior upfront

Classic examples where supervised/unsupervised fail but RL works: game playing, robot locomotion, RLHF for LLMs, ad bidding.

---

## Core Components

- **Agent** — the decision-maker (the LLM, the robot, the chess engine)
- **Environment** — responds to actions and produces new states
- **State (s)** — current snapshot of the situation
- **Action (a)** — choice taken by the agent
- **Reward (r)** — scalar signal after taking an action
- **Return (G)** — cumulative discounted reward: `G = r₁ + γr₂ + γ²r₃ + ...`

---

## The Reward Function

The reward function maps `(state, action, next_state) → scalar`. Designing it is where RL actually breaks in practice.

### Reward Hacking
The agent optimizes the *proxy* reward, not the intent. Classic example: boat racing agent drives in circles hitting boost pads instead of finishing the race — technically maximizing score. RLHF example: models become confidently wrong because humans rate fluent, confident answers higher than hedged correct ones.

> Goodhart's Law: "When a measure becomes a target, it ceases to be a good measure."

### Sparse Rewards
Reward arrives only at the end. Solutions:
- **Reward shaping** — add intermediate rewards, but reintroduces the design problem at finer grain
- **Curiosity-driven exploration** — reward novelty, not just goal achievement
- **Imitation learning** — bootstrap with demonstrations, then fine-tune with RL

### Discount Factor γ
- γ → 0: myopic agent, only cares about immediate reward
- γ → 1: far-sighted, values distant future equally
- Too low: sacrifices long-term gain; too high: training instability

### Multi-objective Rewards
Competing objectives (speed, efficiency, safety) combined into a weighted scalar encode value judgments. There is no objectively correct weighting — this is where ethics enters RL whether intended or not.

---

## Value Function and Credit Assignment

The **value function** V(s) estimates expected future return from state s under the current policy. It's not the reward function — it's a *learned* approximation of future reward built up over millions of episodes.

**The key insight:** A simple terminal reward + learned value function beats a complex shaped reward + shallow search. The reward function's job is just to define what winning means. The value function propagates that signal backward through time. AlphaZero beat Stockfish on this principle — no hand-crafted board evaluation, only win/loss signal.

**Credit assignment problem:** which of the 40 moves in a chess game deserve credit for the win? The value function solves this implicitly by learning position quality from outcome statistics.

---

## RLHF Pipeline

How GPT-4, Claude, Gemini etc. are aligned:

```
1. Supervised Fine-Tune (SFT)
   Train on high-quality demonstrations first

2. Train a Reward Model (RM)
   Show humans pairs of responses → "which is better?"
   Train a separate model to predict human preference scores

3. RL Fine-tune with PPO
   LLM generates responses
   Reward model scores them
   Policy updates to generate higher-scoring responses
   KL penalty prevents diverging too far from SFT model
```

The KL penalty is critical:
```
final_reward = reward_model_score - β · KL(RL_policy || SFT_policy)
```
Without it, the model reward-hacks into degenerate outputs that score well on the reward model but are gibberish to humans.

---

## Multi-turn RL

Multi-turn RL is the same problem as single-turn RL — the math is identical — but with every difficulty dimension amplified:

| Dimension | Single-turn | Multi-turn |
|-----------|------------|------------|
| Action space | One response | Sequence of responses; each response is 50k+ token choices |
| Environment | Stationary | Non-stationary — the user adapts to the model's behavior |
| Reward sparsity | Bad | Qualitatively worse — no natural terminal signal for many tasks |
| Evaluation | Hard | Evaluation collapse: the reward model can be gamed in ways that don't exist with ground-truth rewards |

**The conversation-chess mapping:**

| Chess | LLM conversation |
|-------|-----------------|
| Board state | Conversation history |
| Move | Next response |
| Game | Full conversation / task |
| Win/loss | Human preference / task success |
| Value function | "How good is this conversation going?" |

**The core problem:** reward is holistic (humans rate the full conversation) but training needs per-step signals. Credit assignment across 10 turns of conversation is harder than credit assignment across 40 chess moves.

---

## MTRL System Components

To build MTRL from scratch, you need all of:

| Component | Role | Minimal version |
|-----------|------|-----------------|
| Base model | The agent — must be fine-tunable | Small open-source model (Llama, Mistral) |
| Conversation simulator | Plays the environment, determines episode end | Static dataset of multi-turn conversations |
| Reward model | The reward function — trained on human preferences | GPT-4 as judge |
| Credit assignment | Distributes terminal reward across turns | Flat (same reward to all turns) |
| Training algorithm (PPO) | Updates policy from rollouts | TRL library (HuggingFace) |
| KL penalty / reference model | Prevents reward hacking and policy collapse | Built into TRL |
| Evaluation harness | Independent check — not the same as the reward model | Held-out set, human spot-checks |

The system loop:
```
SFT Model (frozen) ──────────────────────────────┐
                                                   │ KL penalty
SFT Model (trainable) → Conversation Simulator → Rollouts
                                ↓
                         Reward Model → Scores
                                ↓
                            PPO Update
                                ↓
                      Updated Policy (repeat)
                                ↓
                      Evaluation Harness (independent check)
```

---

## Frontier Research Directions

- **Constitutional AI (Anthropic)** — AI-generated critiques as the reward signal; reduces human labeling cost
- **Process Reward Models (PRMs)** — reward correct reasoning *steps*, not just final answers; forces correct chain-of-thought
- **Self-play** — model plays both sides; no humans needed but risks bizarre reward hacking

---

## Key Insight

> Multi-turn RL and evaluation are inseparable. You can't do MTRL without solving evaluation first, because evaluation *is* the reward function.

The through-line: reward design → credit assignment → evaluation → reward design again. Every solution creates the next problem one level up.

---

See also:
- [Week 14](../weeks/week-14-2026-04-06.md)
- [Feature Engineering](../tools/feature-engineering.md) — the supervised learning context in which RL is contrasted
- [LLM Wiki](../tools/llm-wiki.md) — broader LLM stack context
