# Embedding Compression Techniques

A survey of the popular approaches to shrinking storage for large sets of embedding vectors, done while scoping [Week 18](../weeks/week-18-2026-05-04.md)'s build. Only int8 scalar quantization was actually implemented (see [Embedding Vector Quantization](../builds/embedding-vector-quantization.md)); the rest of this page maps the wider landscape for future weeks.

---

## Technique Families

### 1. Scalar Quantization (float32 → int8 / int4 / float16 / binary)
Per-dimension linear mapping to a smaller numeric type.
- **float16/`halfvec`**: truncate mantissa bits. 2x compression, training-free, ~lossless.
- **int8**: calibrate min/max (or quantiles) per dataset, map to `[-128,127]`. 4x compression, needs a calibration pass, typically 99%+ recall retained. Implemented in this week's build — see [Embedding Vector Quantization](../builds/embedding-vector-quantization.md) for both the asymmetric (min/max + shift) and symmetric (zero-centered, no shift) variants, and why symmetric quantization lets similarity search run directly on compressed integers.
- **binary (1-bit)**: keep only the sign bit. 32x compression, training-free, but recall degrades substantially used alone.
- Implementations: pgvector `halfvec`/`bit`, Qdrant scalar/binary quantization, Sentence-Transformers `quantize_embeddings()`.

### 2. Product Quantization (PQ) / Optimized PQ (OPQ)
Split each vector into M sub-vectors, k-means each subspace into a codebook (typically 256 centroids), store only centroid indices. OPQ adds a learned rotation first to balance variance across subspaces before quantizing.
- Compression: 4–16x typical, up to 60x+ in aggressive configs, at a recall cost tuned via subvector count / `nprobe`.
- **Requires training**: codebooks (and OPQ's rotation) are fit via k-means on your own vectors.
- Implementations: `faiss.IndexIVFPQ`, `faiss.IndexHNSWPQ`, OpenSearch Faiss PQ engine.

### 3. Binary Quantization / Hashing (LSH, ITQ, RaBitQ)
- **LSH**: random-projection hashing, training-free, low accuracy-per-bit.
- **ITQ**: learns a rotation to minimize error when mapping to a binary hypercube — better than random LSH, needs fitting.
- **RaBitQ (2024)**: randomized per-dimension quantization with a *provable error bound* (PQ has none). 1536-dim → 192 bytes, no stored codebook. Adopted by Elasticsearch.

### 4. Dimensionality Reduction (pre-compression step)
- **PCA**: fit on your own corpus, project down. Needs a de-skew rotation afterward to re-spread variance evenly before quantizing (same problem OPQ solves for PQ).
- **Random projection**: training-free, weaker fidelity.
- **Autoencoders**: learned nonlinear bottleneck, needs training a network on the embedding distribution.

### 5. Matryoshka Representation Learning (MRL) — a different category entirely
Not a post-hoc compression algorithm — a **training-time property of the embedding model**. MRL models (OpenAI `text-embedding-3-*`, Nomic Embed) sum their training loss across multiple truncation lengths, frontloading signal into early dimensions, so you can simply slice `embedding[:256]` and get a usable smaller vector. **Only available if the model that generated your embeddings was MRL-trained** — it cannot be retrofitted onto arbitrary existing embeddings.

### 6. Composite pattern: Truncate → Quantize → Rerank
The state-of-the-art pattern vector DB vendors recommend: (1) Matryoshka-truncate if available, (2) quantize the result (int8 or binary), (3) keep full-precision vectors around cheaply, (4) search the compressed index with oversampling, then rerank candidates against full precision. Effects compound multiplicatively — e.g. int8 alone ≈ 64% storage reduction, Matryoshka truncation alone ≈ 57%, combined ≈ 78%. Qdrant's binary quantization + rescoring takes `text-embedding-3-large` from ~77% recall (binary only) to 97-99% with reranking.

---

## Training-Free vs. Requires Fitting on Your Data

| Training-free | Requires fitting/calibration |
|---|---|
| float16 cast | int8 scalar quantization (min/max or quantile calibration) |
| Sign-bit binary quantization | PQ / OPQ (k-means codebooks; OPQ also learns a rotation) |
| Matryoshka truncation (if source model supports it) | ITQ (learns rotation for hypercube mapping) |
| Random projection | PCA + de-skew rotation |
| RaBitQ (no stored codebook) | Autoencoders (full neural net training) |

## Sources

[Qdrant quantization](https://qdrant.tech/course/essentials/day-4/what-is-quantization/) · [Azure scalar/binary quantization](https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/search/vector-search-how-to-quantization.md) · [pgvector halfvec/bit](https://jkatz05.com/post/postgres/pgvector-scalar-binary-quantization/) · [Sentence-Transformers embedding quantization](https://sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html) · [Pinecone PQ explainer](https://www.pinecone.io/learn/series/faiss/product-quantization/) · [OpenSearch Faiss PQ](https://docs.opensearch.org/latest/vector-search/optimizing-storage/faiss-product-quantization/) · [RaBitQ paper](https://arxiv.org/abs/2405.12497) · [Elastic RaBitQ explainer](https://www.elastic.co/search-labs/blog/rabitq-explainer-101) · [Weaviate: OpenAI's Matryoshka embeddings](https://weaviate.io/blog/openais-matryoshka-embeddings-in-weaviate) · [Supabase: Matryoshka + Adaptive Retrieval](https://supabase.com/blog/matryoshka-embeddings) · [Towards Data Science: Quantization + Matryoshka for 80% cost reduction](https://towardsdatascience.com/649627-2/) · [Qdrant binary quantization + rescoring](https://qdrant.tech/articles/binary-quantization-openai/)

## Related Builds

- [Embedding Vector Quantization](../builds/embedding-vector-quantization.md) — the int8 implementation from this survey

## Related Tools

- [Embedding Models](../tools/embedding-models.md)
