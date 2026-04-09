# Bigram Model — Neural Network Framework

**Built in:** [Week 11](../weeks/week-11-2026-03-16.md)
**Code:** [gen-ai/language-models/bigram/makemore.ipynb](https://github.com/RGirish/monorepo/blob/main/code/gen-ai/language-models/bigram/makemore.ipynb)

---

## What It Is

A reformulation of the [count-based bigram language model](bigram-language-model.md) using a single-layer neural network trained via gradient descent. The model learns the same character-pair probabilities as the count-based version, but discovers them through backpropagation rather than counting — establishing the neural network training loop as the universal pattern for learning from data.

## The Key Insight

The count matrix from week 10 is **mathematically equivalent** to a linear neural network layer:

| Count-based | Neural network |
|-------------|----------------|
| `P[i][j] = N[i][j] / N[i].sum()` | `logits = one_hot(x) @ W; probs = softmax(logits)` |
| Count → normalize | Random init W → optimize via gradient descent |
| One pass | Many passes (epochs) |
| Converges to: same probabilities | Converges to: same probabilities |

Both approaches minimize the same cross-entropy loss and converge to the same result.

## Implementation (PyTorch)

```python
import torch
import torch.nn.functional as F

# Training data: X = input chars (one-hot), Y = target next chars
W = torch.randn((27, 27), requires_grad=True)

for step in range(100):
    # Forward pass
    xenc = F.one_hot(X, num_classes=27).float()  # one-hot encode inputs
    logits = xenc @ W                              # linear layer: (N, 27) @ (27, 27)
    loss = F.cross_entropy(logits, Y)              # softmax + NLL in one call

    # Backward pass
    W.grad = None
    loss.backward()

    # Update weights
    W.data += -50 * W.grad  # gradient descent

print(f'loss: {loss.item():.4f}')
```

## Why This Matters

This is the canonical "from scratch" introduction to the neural network training loop. Every deep learning model — from this single-layer net to GPT-4 — uses the same pattern:
1. Forward pass (compute predictions)
2. Loss computation (measure error)
3. Backward pass (compute gradients)
4. Weight update (reduce error)

The bigram model is small enough to reason about completely, making it the ideal vehicle for internalizing this loop before scaling up to more complex architectures.

## Notebook: makemore.ipynb

The implementation lives in a Jupyter notebook that walks through the derivation interactively, showing intermediate shapes, visualizations of the weight matrix, and generated sample names at each stage.

## Related Builds

- [Bigram Language Model](bigram-language-model.md) — the count-based version this reformulates

## Related Tools

- [Language Modeling](../tools/language-modeling.md) — covers both implementations in context

## Related Concepts

- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — the cross-cutting concepts this build demonstrates
