# LLM Wiki by Andrej Karpathy

**Author:** Andrej Karpathy
**Link:** [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
**Covered in:** [Week 12](../weeks/week-12-2026-03-23.md)

---

## What It Is

Karpathy's LLM wiki is a comprehensive, practitioner-oriented reference gist covering the full stack of large language model internals. It is dense and opinionated — written for someone who wants to understand *how* LLMs work at a mechanistic level, not just use them as black boxes.

## Coverage

### Architecture
- Transformer architecture: attention heads, MLP layers, residual connections
- Positional encodings (absolute, rotary, ALiBi)
- Layer normalization and why it matters for training stability
- KV cache and how it speeds up autoregressive inference

### Training
- Pretraining on large text corpora: data pipelines, tokenization, batch construction
- Fine-tuning: SFT (supervised fine-tuning), instruction tuning
- RLHF (reinforcement learning from human feedback) and its variants (PPO, DPO)
- Scaling laws: how model performance relates to compute, data, and parameters

### Inference
- Autoregressive generation: sampling character by character (or token by token)
- Sampling strategies: greedy, temperature, top-k, top-p (nucleus sampling)
- Quantization: reducing model precision (fp16, int8, int4) to reduce memory and improve speed
- Speculative decoding and other inference acceleration techniques

### Key Concepts
- Tokenization (BPE, SentencePiece) and vocabulary size tradeoffs
- Context window length and its engineering implications
- Emergent capabilities and why they arise at scale
- System prompts, RLHF alignment, and the difference between base and instruction-tuned models

## Why It Matters

This wiki ties together everything covered in the makemore series (weeks 10–11) and provides the bigger picture. The bigram model and neural net training loop from those weeks are the conceptual foundation for everything in this wiki — just scaled up enormously.

## Related Tools

- [Language Modeling](language-modeling.md) — the hands-on counterpart to this reference
- [Embedding Models](embedding-models.md) — embeddings are a core component of the transformer architecture
- [Open Knowledge Format](open-knowledge-format.md) — Google's spec formalizes the same markdown-as-knowledge-base pattern Karpathy describes for this wiki's own design

## Related Concepts

- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — cross-cutting concepts connecting makemore to the broader LLM stack
