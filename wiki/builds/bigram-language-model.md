# Bigram Language Model

**Built in:** [Week 10](../weeks/week-10-2026-03-09.md)
**Code:** [gen-ai/language-models/bigram](https://github.com/RGirish/monorepo/tree/main/gen-ai/language-models/bigram)

---

## What It Is

A character-level bigram language model trained on a names dataset, implemented using count-based statistics. Given any character, the model predicts the probability distribution over the next character using learned bigram frequencies. It generates new names by sampling character by character until a stop token is reached.

## How It Works

### Training: Build the Count Matrix

```python
# Count every (prev_char, next_char) pair in the training corpus
for name in names:
    chars = ['.'] + list(name) + ['.']  # '.' is start/end token
    for ch1, ch2 in zip(chars, chars[1:]):
        ix1, ix2 = stoi[ch1], stoi[ch2]
        N[ix1, ix2] += 1
```

This produces a 27×27 matrix N (26 letters + start/end token) where `N[i][j]` is the number of times character `j` followed character `i` in the training data.

### Normalization: Convert to Probabilities

```python
P = N.float()
P = P / P.sum(dim=1, keepdim=True)  # normalize rows to sum to 1
```

Adding smoothing (e.g., `N + 1`) prevents zero-probability entries for unseen bigrams.

### Inference: Sample New Names

```python
out = []
ix = 0  # start with '.'
while True:
    p = P[ix]           # probability distribution over next chars
    ix = torch.multinomial(p, 1).item()  # sample
    if ix == 0: break   # hit end token
    out.append(itos[ix])
print(''.join(out))
```

### Evaluation: Cross-Entropy Loss

```python
log_likelihood = 0
n = 0
for name in names:
    chars = ['.'] + list(name) + ['.']
    for ch1, ch2 in zip(chars, chars[1:]):
        prob = P[stoi[ch1], stoi[ch2]]
        log_likelihood += torch.log(prob)
        n += 1
nll = -log_likelihood / n  # negative log-likelihood (lower is better)
```

## Results

The count-based model achieves a negative log-likelihood of approximately 2.45 nats on the training set. This is the baseline that the [neural network reformulation](bigram-neural-net.md) (week 11) is measured against — both converge to the same loss.

## Related Tools

- [Language Modeling](../tools/language-modeling.md) — theoretical background and both model implementations

## Related Concepts

- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — cross-cutting concepts
