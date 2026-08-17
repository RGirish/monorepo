# Language Modeling Fundamentals

**Appears in:** [Week 10](../weeks/week-10-2026-03-09.md) · [Week 11](../weeks/week-11-2026-03-16.md) · [Week 12](../weeks/week-12-2026-03-23.md)

---

## Overview

The makemore series (weeks 10–11) and Karpathy's LLM wiki (week 12) collectively build a ground-up understanding of how language models work. This page captures the key concepts and how they connect.

---

## Core Concepts

### Tokenization

Tokenization converts raw text into a discrete sequence of tokens that a model can process. The choice of tokenization scheme involves a tradeoff between vocabulary size and sequence length:
- **Character-level** (used in makemore) — small vocabulary (27), longer sequences, simple
- **BPE (Byte Pair Encoding)** — medium vocabulary (~50K), balances compression and granularity
- **Word-level** — large vocabulary, short sequences, but poor handling of rare/new words

### Probability Distribution over Next Token

A language model's fundamental job is: given a sequence of previous tokens, predict a probability distribution over all possible next tokens. Better models assign higher probability to the actual next token.

### Softmax

Converts raw model outputs (logits — unconstrained real numbers) into a valid probability distribution:

```
softmax(z)ᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)
```

Properties: all outputs are in (0, 1), outputs sum to 1. Temperature scaling (`softmax(z/T)`) controls sharpness — low T → more deterministic, high T → more random.

### Cross-Entropy Loss

The standard loss function for language modeling. Measures how surprised the model is by the actual next token:

```
loss = -log(p(correct_next_token))
```

- Perfect prediction: loss = 0 (probability 1.0 assigned to correct token)
- Random prediction for 27-class problem: loss ≈ ln(27) ≈ 3.3 nats
- Bigram model achieves: ~2.45 nats (better than random, worse than large LLMs)

Cross-entropy is the average of this over all positions in the training data.

### The Neural Network Training Loop

The universal pattern for training any neural network:

```
for each batch:
    logits = model.forward(X)           # predict
    loss = cross_entropy(logits, Y)     # measure error
    model.zero_grad()
    loss.backward()                     # compute gradients
    optimizer.step()                    # update weights
```

This loop is identical for a single-layer bigram model and for GPT-4 — only the model architecture and scale differ.

### Backpropagation

The algorithm that computes gradients of the loss with respect to all model parameters via the chain rule. PyTorch's autograd engine handles this automatically via `loss.backward()`, but understanding backprop manually (as Karpathy covers) is essential for debugging and architectural intuition.

---

## The Count → Neural Net Equivalence (Key Insight from Weeks 10–11)

The biggest conceptual payoff of the makemore series is seeing that the count-based bigram model and the neural network formulation are mathematically identical:

| | Count-based | Neural network |
|--|-------------|----------------|
| Representation | N[i,j] = frequency matrix | W = weight matrix |
| Normalization | Divide rows by sum | Softmax |
| Learning | One-pass counting | Gradient descent |
| Result | Same P(j\|i) | Same P(j\|i) |

This equivalence shows that neural networks are not magic — they're gradient-descent-optimized function approximators that can recover the same statistical patterns a statistician would compute by hand, plus much more when given richer architectures.

---

## Path to Modern LLMs

The bigram model → neural net path is the first step on a longer progression:

```
Bigram model          (week 10–11: single previous character)
     ↓
MLP language model    (next: fixed context window, all tokens as input)
     ↓
RNN / LSTM           (variable-length context, sequential processing)
     ↓
Transformer          (attention over full context window, parallel)
     ↓
LLM (GPT, Claude...) (transformer + scale + RLHF)
```

Week 12's LLM wiki covers the full stack at the top of this hierarchy.

---

## Related Tools

- [Language Modeling](../tools/language-modeling.md) — detailed notes on the makemore series
- [LLM Wiki](../tools/llm-wiki.md) — Karpathy's broader LLM reference
- [Prompt Engineering](../tools/prompt-engineering.md) — applies the autoregressive, next-token-conditioned-on-everything-before-it mechanism described above to explain why chain-of-thought and prefilling work

## Related Builds

- [Bigram Language Model](../builds/bigram-language-model.md) — count-based implementation
- [Bigram Neural Net](../builds/bigram-neural-net.md) — neural network reformulation
