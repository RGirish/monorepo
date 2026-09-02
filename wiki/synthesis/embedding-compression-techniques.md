# Embedding Compression Techniques

A deep survey of the popular approaches to shrinking storage for large sets of embedding vectors, done while scoping [Week 18](../weeks/week-18-2026-05-04.md)'s build and grounded in current (2024–2026) vendor docs and papers rather than general prior knowledge. Only int8 scalar quantization was actually implemented (see [Embedding Vector Quantization](../builds/embedding-vector-quantization.md)); the rest of this page maps the wider landscape as a backlog for future weeks — see [Build Ideas](../backlog.md) for the specific follow-up builds this spawned.

---

## Technique Families

### 1. Scalar Quantization (float32 → int8 / int4 / float16 / binary)

**What it is:** a per-dimension linear mapping from float32 range to a smaller type. int8 uses a calibrated min/max (or quantile bounds, to exclude outliers) mapped onto `[-128, 127]`; float16/`halfvec` just drops mantissa bits from the native floating-point format; binary keeps only the sign bit.

- **float16/`halfvec`**: 2x compression. Not really a bucket-quantization scheme at all — no calibration, no shift, just a floating-point format with fewer precision bits. Training-free, ~lossless in practice.
- **int8**: 4x compression (`1536-dim × 4 bytes → 1536-dim × 1 byte`). Needs a calibration pass — computing min/max/quantiles over your dataset — to fix the scale and (for the asymmetric variant) a zero-point shift. Typically retains 99%+ recall on normalized embeddings; considered a "free" production default by most vendors. Implemented in this week's build — see [Embedding Vector Quantization](../builds/embedding-vector-quantization.md) for the full asymmetric (min/max + shift) vs. symmetric (zero-centered, no shift) distinction, and why the symmetric variant lets similarity search run directly on compressed int8 values via one scalar correction factor instead of dequantizing first.
- **int4**: same mechanism as int8, just 16 buckets instead of 256 — 8x compression, coarser rounding.
- **binary (1-bit)**: 32x compression (`1536-dim × 4 bytes → 192 bytes`). In practice implemented as sign-based thresholding (positive/negative, or above/below the mean) rather than a literal 2-bucket min/max mapping, since 2 buckets spanning the full min-max range would be far too crude. Training-free, but recall degrades substantially used alone — almost always paired with rescoring (see family 6 below).

**Implementations:** pgvector `halfvec`/`bit` types, Qdrant scalar/binary quantization, Azure AI Search, MongoDB Atlas Vector Search, Sentence-Transformers `quantize_embeddings()`.

**Sources:** [Qdrant quantization](https://qdrant.tech/course/essentials/day-4/what-is-quantization/) · [Azure scalar/binary quantization](https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/search/vector-search-how-to-quantization.md) · [pgvector halfvec/bit — Jonathan Katz](https://jkatz05.com/post/postgres/pgvector-scalar-binary-quantization/) · [Neon halfvec](https://neon.com/blog/dont-use-vector-use-halvec-instead-and-save-50-of-your-storage-cost) · [Sentence-Transformers embedding quantization](https://sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html) · [HF blog on binary/scalar quantization](https://huggingface.co/blog/embedding-quantization)

---

### 2. Product Quantization (PQ) and Optimized PQ (OPQ)

**What it is:** split each vector into M sub-vectors; run k-means per subspace to build a codebook (typically 256 centroids, i.e. 8 bits per subvector); store only the centroid index per subspace instead of the raw values. OPQ first learns a rotation of the input space to balance variance evenly across subspaces before applying PQ, which reduces quantization distortion — typically +2 to +6 recall points over plain PQ at the same code size, because unrotated data often has variance concentrated unevenly across dimensions, which wastes some subspaces' codebook capacity.

**Compression:** 4–16x is commonly quoted; aggressive configurations reach 32–97% size reduction. One cited example: 1 billion × 1536-dim vectors compressed from a much larger raw footprint down to ~96GB — a 63x reduction — at 90–95% recall. `IndexIVFPQ` can be tuned more aggressively still, but recall can drop to ~50% if over-compressed; the practical knobs are subvector count and `nprobe` (how many IVF clusters get searched per query).

**Requires training:** yes — codebooks are learned via k-means on a representative sample of your own vectors; OPQ additionally learns a rotation matrix. This is a meaningfully bigger commitment than scalar quantization's one-pass calibration: you need enough representative data to fit good codebooks, and the codebooks become a fixed asset that has to be retrained if the embedding distribution shifts significantly.

**Implementations:** `faiss.IndexPQ`, `faiss.IndexIVFPQ`, `faiss.IndexHNSWPQ` (factory strings like `"IVF1024,PQ96x8"`), OpenSearch's Faiss PQ engine.

**Sources:** [Pinecone PQ explainer](https://www.pinecone.io/learn/series/faiss/product-quantization/) · [OpenSearch Faiss PQ docs](https://docs.opensearch.org/latest/vector-search/optimizing-storage/faiss-product-quantization/) · [FAISS IVF/PQ settings](https://medium.com/@Modexa/10-faiss-ivf-pq-settings-you-shouldnt-ignore-97725f87ff0b)

---

### 3. Binary Quantization / Hashing (LSH, ITQ, RaBitQ)

- **LSH (Locality-Sensitive Hashing / random projection hashing)**: training-free, uses randomized projections to map vectors into a binary hypercube. Classic and simple, but comparatively low accuracy per bit compared to learned methods, since the projections aren't adapted to the actual data distribution.
- **ITQ (Iterative Quantization)**: learns a rotation of zero-centered data specifically to minimize the error introduced when mapping onto a binary hypercube — a "learned" alternative to random LSH. Requires training (the rotation is fit to your data). Historically documented as more effective on image data than on text/NLP retrieval.
- **RaBitQ (2024, SIGMOD)**: a randomized quantization scheme that gives each dimension its own bit, but crucially comes with a **theoretical error bound** — unlike PQ, which has none and can fail unpredictably on certain datasets. A 1536-dim vector compresses to 192 bytes with no stored codebook at all, and the scheme still supports accurate distance estimation with provable guarantees. It's increasingly cited as the modern, principled successor to ad hoc binary quantization, and has been adopted/discussed by Elasticsearch. An "Extended RaBitQ" variant generalizes the same idea into a general scalar-quantization scheme, not just 1-bit.

**Sources:** [RaBitQ paper (arXiv)](https://arxiv.org/abs/2405.12497) · [RaBitQ ACM SIGMOD](https://dl.acm.org/doi/abs/10.1145/3654970) · [Elastic RaBitQ explainer](https://www.elastic.co/search-labs/blog/rabitq-explainer-101) · [Extended RaBitQ](https://dev.to/gaoj0017/extended-rabitq-an-optimized-scalar-quantization-method-83m) · [ITQ embedding compression paper](https://arxiv.org/pdf/2001.05314) · [learned LSH + quantization retrieval](https://medium.com/@gopikwork/latency-optimized-embedding-retrieval-with-learnable-lsh-and-quantization-9deaa025e0d3)

---

### 4. Dimensionality Reduction (PCA, random projection, autoencoders) as a pre-compression step

- **PCA**: post-hoc, no embedding-model retraining needed — fit PCA on your own embedding corpus, project to fewer dimensions. Recent research (2025–2026) finds PCA matches fancier nonlinear methods (Kernel PCA, UMAP, Isomap) for this purpose while being far cheaper to fit. Caveat: PCA concentrates variance in its early components, which then quantizes unevenly under per-dimension scalar quantization (the early, high-variance components need a wider bucket range than the later, low-variance ones) — fixed by applying a random orthogonal rotation *after* PCA to spread variance evenly before quantizing, mirroring exactly what OPQ does for PQ.
- **Random projection**: training-free, weaker fidelity than PCA but zero fit cost.
- **Autoencoders**: a learned encoder/decoder with a bottleneck latent layer; more flexible/nonlinear than PCA but requires training a neural net on your embedding distribution, plus reconstruction-quality tuning. Recent sparse-autoencoder variants (e.g. "CompressAE") compress dense embeddings into sparse high-dimensional codes without touching the original embedding model.
- **Composability:** dimensionality reduction and quantization are explicitly studied together as a two-stage pipeline (reduce dimension first, then scalar/binary/PQ-quantize the reduced vectors) — this is an active 2025–2026 research area, not just a heuristic combination.

**Sources:** ["When Is 0.1% Enough?" — combined dim-reduction + quantization (arXiv 2606.01074)](https://arxiv.org/html/2606.01074v1) · [Optimization of embeddings storage for RAG via quantization + dim reduction (arXiv 2505.00105)](https://arxiv.org/pdf/2505.00105) · [PCA-RAG](https://arxiv.org/html/2504.08386v1) · [CoRECT compression-eval framework](https://arxiv.org/html/2510.19340v1)

---

### 5. Matryoshka Representation Learning (MRL) — a training-time property, not a post-hoc algorithm

**Key distinction:** MRL is baked into the embedding model's *training* — the loss is computed and summed across multiple truncation lengths (e.g. 768/512/256/128/64 dims), forcing the model to frontload the most important signal into the earliest dimensions. This means you can simply slice `embedding[:k]` after the fact and get a usable, still-meaningful embedding — no codebook, no calibration, nothing to fit yourself. It's fundamentally different from every technique above, all of which are *post-hoc* compressors applied to an already-fixed embedding.

**The catch:** you only benefit from this if the embedding model that generated your vectors was actually trained with MRL — OpenAI's `text-embedding-3-small/large` (via the `dimensions` API parameter) and several open models like Nomic Embed. It cannot be retrofitted onto arbitrary existing embeddings; if your source vectors weren't produced by an MRL-trained model, this technique simply isn't available to you.

**Reported numbers:** `text-embedding-3-large` truncated to 256 dims still beats the older `ada-002` at its full 1536 dims on MTEB benchmarks; general MRL models truncated to 64 dims retain roughly 98% of full-dimensionality performance.

**Sources:** [Weaviate: OpenAI's Matryoshka embeddings](https://weaviate.io/blog/openais-matryoshka-embeddings-in-weaviate) · [Supabase: Matryoshka + Adaptive Retrieval](https://supabase.com/blog/matryoshka-embeddings) · [Zilliz MRL explainer](https://zilliz.com/blog/matryoshka-representation-learning-method-behind-openai-text-embeddings) · [MongoDB/Voyage AI Matryoshka](https://www.mongodb.com/company/blog/technical/matryoshka-embeddings-smarter-embeddings-with-voyage-ai) · [SMEC: rethinking MRL for compression (arXiv 2510.12474)](https://arxiv.org/pdf/2510.12474)

---

### 6. Composite / State-of-the-Art Pattern: Truncate → Quantize → Rerank

This is the pattern vector-DB vendors now explicitly recommend, and it's the practical destination all the families above feed into:

1. **Truncate** (if using an MRL model) to a smaller dimension — e.g. 1536 → 256 or 128.
2. **Quantize** the truncated vector — int8 or binary — for the bulk of the index.
3. **Store full-precision (or less-quantized) vectors** alongside, cheaply, for reranking.
4. **Search** with oversampling (retrieve `k × oversample_factor` candidates cheaply using the compressed index), then **rerank** that candidate set against the full-precision vectors to recover accuracy.

**Concrete numbers found:**
- Quantization alone (float32→int8): ~63.7% storage reduction. Matryoshka truncation alone: ~56.6% reduction. **Combined** (128-dim Matryoshka + int8): ~77.9% reduction — a ~4.5x density increase. The effects compound multiplicatively, not just additively. ([Towards Data Science, "Scaling Vector Search: Quantization and Matryoshka Embeddings for 80% Cost Reduction"](https://towardsdatascience.com/649627-2/))
- Qdrant binary quantization + rescoring: OpenAI `text-embedding-3-large` (3072d) recall goes from ~76–77% (binary only, no rerank) to 97–99% with rescoring + oversampling; `ada-002` (1536d) hits 0.98 recall@100 with 4x oversampling; Cohere `embed-english-v2.0` (4096d) hits 0.98 recall@50 with 2x oversampling. ([Qdrant binary quantization article](https://qdrant.tech/articles/binary-quantization-openai/), [Qdrant rescoring docs](https://qdrant.tech/course/essentials/day-4/rescoring-oversampling-indexing/))
- pgvector explicitly recommends this pattern: use `bit` (binary) as a fast prefilter, then rerank candidates against full-precision `vector`/`halfvec` columns, since binary alone "degrades significantly" standalone. ([pgvector quantization — Jonathan Katz](https://jkatz05.com/post/postgres/pgvector-scalar-binary-quantization/))
- A cited experimental community project ("turboquant-pro") claims 27x compression at 99.8% recall@10 combining PCA + Matryoshka + a custom quantizer with reranking — illustrative of how far composability can push ratios, though it's a smaller/less-vetted project rather than an established vendor benchmark. ([GitHub](https://github.com/ahb-sjsu/turboquant-pro))

---

### A noted gap: Residual Vector Quantization (RVQ / RQ-VAE)

Multi-stage *residual* quantization is a distinct family from single-stage PQ: rather than one k-means pass per subvector, RVQ quantizes a vector, computes the residual (original minus its quantized approximation), then quantizes *that residual* with a second codebook, and can repeat for further stages — progressively refining the approximation. This shows up more in generative and recommender-system embedding contexts (e.g. RQ-VAE for discrete token generation) than in classic ANN search, and wasn't verified in depth during this survey — worth a dedicated follow-up search if pursued as a build.

---

## Training-Free vs. Requires Fitting on Your Data

| Training-free (apply directly) | Requires fitting/calibration on your corpus |
|---|---|
| float16 / `halfvec` cast | int8 scalar quantization (needs min/max or quantile calibration) |
| Sign-bit binary quantization | PQ / OPQ (k-means codebooks; OPQ also learns a rotation) |
| Matryoshka truncation (slice, but only if source model was MRL-trained) | ITQ (learns rotation for hypercube mapping) |
| Random projection | PCA (fit components on your data) + the de-skew rotation step |
| RaBitQ (randomized, no stored codebook — effectively training-free per-vector) | Autoencoders (full neural net training) |

## Sources

[Qdrant quantization](https://qdrant.tech/course/essentials/day-4/what-is-quantization/) · [Azure scalar/binary quantization](https://github.com/MicrosoftDocs/azure-ai-docs/blob/main/articles/search/vector-search-how-to-quantization.md) · [pgvector halfvec/bit — Jonathan Katz](https://jkatz05.com/post/postgres/pgvector-scalar-binary-quantization/) · [Neon halfvec](https://neon.com/blog/dont-use-vector-use-halvec-instead-and-save-50-of-your-storage-cost) · [Sentence-Transformers embedding quantization](https://sbert.net/examples/sentence_transformer/applications/embedding-quantization/README.html) · [HF blog on binary/scalar quantization](https://huggingface.co/blog/embedding-quantization) · [Pinecone PQ explainer](https://www.pinecone.io/learn/series/faiss/product-quantization/) · [OpenSearch Faiss PQ docs](https://docs.opensearch.org/latest/vector-search/optimizing-storage/faiss-product-quantization/) · [FAISS IVF/PQ settings](https://medium.com/@Modexa/10-faiss-ivf-pq-settings-you-shouldnt-ignore-97725f87ff0b) · [RaBitQ paper](https://arxiv.org/abs/2405.12497) · [RaBitQ ACM SIGMOD](https://dl.acm.org/doi/abs/10.1145/3654970) · [Elastic RaBitQ explainer](https://www.elastic.co/search-labs/blog/rabitq-explainer-101) · [Extended RaBitQ](https://dev.to/gaoj0017/extended-rabitq-an-optimized-scalar-quantization-method-83m) · [ITQ embedding compression paper](https://arxiv.org/pdf/2001.05314) · [learned LSH + quantization retrieval](https://medium.com/@gopikwork/latency-optimized-embedding-retrieval-with-learnable-lsh-and-quantization-9deaa025e0d3) · ["When Is 0.1% Enough?" (arXiv 2606.01074)](https://arxiv.org/html/2606.01074v1) · [Optimization of embeddings storage for RAG (arXiv 2505.00105)](https://arxiv.org/pdf/2505.00105) · [PCA-RAG](https://arxiv.org/html/2504.08386v1) · [CoRECT compression-eval framework](https://arxiv.org/html/2510.19340v1) · [Weaviate: OpenAI's Matryoshka embeddings](https://weaviate.io/blog/openais-matryoshka-embeddings-in-weaviate) · [Supabase: Matryoshka + Adaptive Retrieval](https://supabase.com/blog/matryoshka-embeddings) · [Zilliz MRL explainer](https://zilliz.com/blog/matryoshka-representation-learning-method-behind-openai-text-embeddings) · [MongoDB/Voyage AI Matryoshka](https://www.mongodb.com/company/blog/technical/matryoshka-embeddings-smarter-embeddings-with-voyage-ai) · [SMEC (arXiv 2510.12474)](https://arxiv.org/pdf/2510.12474) · [Towards Data Science: Quantization + Matryoshka for 80% cost reduction](https://towardsdatascience.com/649627-2/) · [Qdrant binary quantization + rescoring](https://qdrant.tech/articles/binary-quantization-openai/) · [Qdrant rescoring/oversampling docs](https://qdrant.tech/course/essentials/day-4/rescoring-oversampling-indexing/) · [turboquant-pro (community project)](https://github.com/ahb-sjsu/turboquant-pro)

## Related Builds

- [Embedding Vector Quantization](../builds/embedding-vector-quantization.md) — the int8 scalar quantization implementation from this survey

## Related Tools

- [Embedding Models](../tools/embedding-models.md)
