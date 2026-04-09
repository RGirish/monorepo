# Language Modeling — Makemore Series

**Source:** Andrej Karpathy's "makemore" series
**Video:** [youtube.com/watch?v=PaCmpygFfXo](https://www.youtube.com/watch?v=PaCmpygFfXo)
**Covered in:** [Week 10](../weeks/week-10-2026-03-09.md) · [Week 11](../weeks/week-11-2026-03-16.md)

---

## Overview

The makemore series by Andrej Karpathy teaches language modeling by building character-level models from scratch — starting from pure statistics and progressing through neural network formulations. "Makemore" generates more things like the training examples (names, words) by learning the statistical patterns in sequences of characters.

---

## Week 10 — Count-Based Bigram Model

### What Is a Bigram Model

A bigram model predicts the next character in a sequence based only on the previous character. Despite its simplicity, it captures local statistical patterns surprisingly well. The model is a 27×27 matrix (26 letters + start/end token) where entry `[i][j]` represents the probability that character `j` follows character `i`.

### Building It

1. **Count matrix** — iterate over the training corpus, count how often each (prev_char, next_char) pair occurs
2. **Softmax normalization** — divide each row by its sum to get a valid probability distribution
3. **Sampling** — to generate a new name, start at the start token and repeatedly sample the next character from the current row until the end token is drawn
4. **Loss** — cross-entropy loss measures how surprised the model is by the actual next characters; lower is better

### Key Formula

```
P(next_char | prev_char) = count(prev_char, next_char) / sum_over_all_chars(count(prev_char, *))
```

---

## Week 11 — Neural Network Reformulation

### The Key Insight

The count-based bigram model is mathematically equivalent to a single-layer neural network:
- One-hot encode the current character (27-dimensional vector)
- Multiply by a 27×27 weight matrix W
- Apply softmax to get probabilities

The count matrix from week 10 and the learned weight matrix from the neural net converge to the same values — but the neural net gets there through gradient descent rather than counting.

### The Neural Network Training Loop

```
for step in range(num_steps):
    # Forward pass
    logits = X_one_hot @ W         # linear layer
    probs = softmax(logits)        # convert to probabilities
    loss = cross_entropy(probs, Y) # measure prediction error

    # Backward pass
    W.grad = None
    loss.backward()                # compute gradients

    # Weight update
    W.data -= learning_rate * W.grad  # gradient descent step
```

### Why This Matters

The neural net formulation establishes the template for all subsequent, more powerful models. Swap in a deeper network, use more context than just the previous character, and you have a path toward full transformer language models.

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Tokenization** | Converting raw text to discrete tokens (characters here, subwords in LLMs) |
| **Softmax** | Converts logits (raw scores) to a probability distribution summing to 1 |
| **Cross-entropy loss** | Measures how much the predicted distribution diverges from the true next token |
| **Gradient descent** | Iteratively adjusts weights in the direction that reduces loss |
| **Backpropagation** | Algorithm for computing gradients of the loss w.r.t. all weights |

## Related Builds

- [Bigram Language Model](../builds/bigram-language-model.md) — count-based implementation (week 10)
- [Bigram Neural Net](../builds/bigram-neural-net.md) — neural network reformulation (week 11)

## Related Concepts

- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — cross-cutting concepts from both weeks
- [LLM Wiki](llm-wiki.md) — broader LLM reference covering these fundamentals in more depth
