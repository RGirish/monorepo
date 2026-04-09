# Embedding Models and Vector Similarity

**Covered in:** [Week 7](../weeks/week-07-2026-02-16.md)

---

## What Embedding Models Do

Embedding models convert text (or other data) into dense numerical vectors in a high-dimensional space where semantic relationships are preserved as geometric proximity. Two sentences with similar meaning produce vectors that are close together; unrelated sentences produce vectors that are far apart. This allows semantic reasoning to be performed using standard linear algebra.

Popular embedding models include OpenAI's `text-embedding-ada-002`, Sentence Transformers (open source), and Cohere's embedding API.

## Vector Similarity Algorithms

Three primary algorithms are used to measure similarity between vectors:

### Cosine Similarity
Measures the angle between two vectors, ignoring their magnitude.
- Range: -1 to 1 (1 = identical direction, 0 = orthogonal, -1 = opposite)
- **When to use:** When the magnitude of vectors shouldn't matter — e.g., comparing documents of different lengths
- Formula: `cos(θ) = (A · B) / (|A| × |B|)`

### Dot Product
Measures both direction and magnitude together.
- Range: unbounded (depends on vector norms)
- **When to use:** When vectors are already normalized (reduces to cosine similarity) or when magnitude carries meaning (e.g., relevance scoring)
- Formula: `A · B = Σ(aᵢ × bᵢ)`

### Euclidean Distance
Straight-line distance between two points in vector space.
- Range: 0 to ∞ (0 = identical)
- **When to use:** When absolute position in space matters, not just direction
- Formula: `d(A, B) = √Σ(aᵢ - bᵢ)²`

## Applications

- **Semantic search** — find documents by meaning, not just keyword overlap
- **RAG (Retrieval-Augmented Generation)** — retrieve relevant context chunks before LLM generation
- **Recommendation systems** — find items similar to a user's preferences
- **Clustering** — group semantically related content

## Related Builds

- [Vector Database](../builds/vector-db.md) — custom vector DB implementation using these similarity algorithms

## Related Concepts

- [Language Modeling](language-modeling.md) — embeddings appear inside language models as token representations
