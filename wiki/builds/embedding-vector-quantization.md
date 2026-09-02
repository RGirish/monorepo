# Embedding Vector Quantization

**Built in:** [Week 18](../weeks/week-18-2026-05-04.md)
**Code:** [databases/vector-quantization](https://github.com/RGirish/monorepo/tree/main/code/databases/vector-quantization)

---

## What It Is

Two implementations of int8 scalar quantization for compressing embedding vectors — the simplest member of the broader embedding-compression technique family (which also includes product quantization, binary quantization/hashing, dimensionality reduction, and Matryoshka Representation Learning; see the [Embedding Compression Techniques](../synthesis/embedding-compression-techniques.md) survey for the full landscape). The goal: shrink a corpus of document embeddings for storage, without meaningfully harming similarity-search results.

## Why Quantization Works At All

An embedding is a list of float32 numbers (4 bytes each). int8 quantization maps each float onto one of only 256 integer buckets, which is inherently lossy — but similarity search (cosine/dot-product) sums signal across all dimensions at once (1536, in the demo). Individual per-dimension rounding errors are small, bounded, and effectively random in sign, so they average out across the dot product rather than compounding. The result: a 4x storage reduction with negligible impact on nearest-neighbor rankings.

## Asymmetric Quantization

`asymmetric_quantization.py` implements the textbook version: calibrate using the actual `vmin`/`vmax` of the dataset, map that range onto the full `[-128, 127]` int8 range using a scale **and** a shift (the data's minimum doesn't sit at zero, so a zero-point offset is required).

```python
scale = (vmax - vmin) / 255
quantized = round((x - vmin) / scale - 128)
```

On a 1000×1536 synthetic dataset (normalized to unit vectors, mimicking real embedding-model output): 6000 KB → 1500 KB (4x), max per-element error `≈ scale/2` (the theoretical rounding bound), and **10/10 top-10 nearest neighbors preserved** after dequantizing and re-ranking.

A worked five-value trace (`walkthrough.py`) makes the mechanism concrete: each float is shifted to a non-negative range, divided by `scale` into "bucket units," recentered by `-128` into int8's actual range, and only then rounded — the rounding step is the sole point of information loss; every other step is algebraically reversible.

## Symmetric Quantization — and Why Real Vector DBs Use It

`symmetric_quantization.py` implements the variant vector databases actually favor: calibrate using `max(|vmin|, |vmax|)` instead of the raw min/max, mapping a *zero-centered* range onto int8. No shift needed — real `0.0` maps exactly to integer `0` by construction:

```python
scale = max_abs / 127
quantized = round(x / scale)
```

Because there's no additive shift, the quantized integers are a pure scaled-down copy of the originals. That means a dot product computed **directly on the raw int8 values** (widened to `int32` to avoid overflow — `127 × 127 × 1536 ≈ 24.7M`, well inside `int32` but not `int8`) has an exact linear relationship to the true dot product:

```
real_dot_product ≈ int_dot_product(a_q, b_q) × scale_a × scale_b
```

This is the practical payoff: search can run **entirely on compressed integers**, with a single scalar correction applied only at the end — never reconstructing full-precision vectors for comparison. The demo confirms it: querying a vector against itself gives `true=1.000000` vs. `approx=1.000708` (normalized vectors have unit self-similarity), and top-10 rankings computed purely from `int32` dot products match the full-precision ranking exactly (10/10).

The tradeoff is a small amount of wasted range when the data isn't perfectly symmetric around zero — in the demo, the negative extreme (`-0.1244`) was larger in magnitude than the positive extreme (`0.1188`), so quantized values only reached `[-127, 121]`, never using the full positive headroom.

## Related Tools

- [Embedding Models](../tools/embedding-models.md) — produces the vectors this build compresses

## Related Builds

- [Vector Database](vector-db.md) — the flat-index similarity search this compression technique would sit in front of at scale
