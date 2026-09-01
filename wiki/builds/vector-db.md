# Vector Database

**Built in:** [Week 7](../weeks/week-07-2026-02-16.md)
**Code:** [databases/vector](https://github.com/RGirish/monorepo/tree/main/code/databases/vector)

---

## What It Is

A custom vector database implementation that stores embedding vectors alongside metadata and supports similarity search — the core primitive behind semantic search, RAG pipelines, and recommendation systems.

## Core Operations

### Insert
Store a vector (dense float array) with an associated document ID and optional metadata. Vectors are stored in memory indexed by ID.

### Similarity Search (Query)
Given a query vector, find the `k` most similar vectors in the database. The implementation supports two similarity metrics:

**Cosine Similarity:** Measures the angle between vectors, ignoring magnitude. Best for semantic similarity where scale doesn't matter.
```
similarity = dot(A, B) / (|A| × |B|)
```

**Dot Product Similarity:** Measures both direction and magnitude. Used when vectors are pre-normalized or when magnitude carries relevance information.
```
similarity = Σ(aᵢ × bᵢ)
```

### Delete
Remove a vector by ID.

## Architecture

The implementation uses a **flat index** (brute-force linear scan) — every query compares the query vector against all stored vectors. This is optimal for small datasets (< 100K vectors) and simple to implement. Production vector databases (Pinecone, Weaviate, Qdrant) use approximate nearest neighbor (ANN) algorithms like HNSW or IVF for scale.

## Why Build This

Building a vector DB from scratch makes the core data structure and query mechanics transparent. Production vector databases abstract away the similarity computation behind APIs — implementing it directly builds intuition for what's happening at query time and why cosine similarity is preferred over Euclidean distance for most text embedding use cases.

## Related Tools

- [Embedding Models](../tools/embedding-models.md) — produces the vectors this database stores and searches

## Related Concepts

- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — embeddings are the internal representation used in language models

## Related Tools

- [DuckDB](../tools/duckdb.md) — a different database-systems tradeoff: columnar/vectorized OLAP for analytical scans, vs. this build's in-memory flat index for similarity search
