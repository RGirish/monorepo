# Feature Stores in Machine Learning

**Filed from:** Week 13 query — feature engineering + feature stores
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Embedding Models](../tools/embedding-models.md), [Vector Database](../builds/vector-db.md)

---

## What Is a Feature Store?

A feature store is a centralized system for storing, versioning, sharing, and serving features — the engineered representations of raw data that ML models consume. It's a database specifically designed for ML features, with extra concerns around consistency, freshness, and reproducibility.

Core responsibilities:
- **Compute once, reuse many times** — a feature computed for one model is available to all other models
- **Training/serving consistency** — the exact same feature logic runs at training time and at inference time (a notoriously hard problem to get right)
- **Point-in-time correctness** — when training, you can only use features that were available *before* a given event, not computed using future data (a form of leakage prevention)
- **Versioning** — track how feature definitions change over time

Well-known examples: Feast (open source), Tecton, Databricks Feature Store, Vertex AI Feature Store.

---

## Are Feature Stores Only for Hand-Engineered Features?

No. They remain relevant in the deep learning / feature learning world — the *what* being stored shifts, but the operational problem remains.

**Still very relevant:**
- **Hybrid systems** — XGBoost and similar models run alongside GenAI in production (fraud detection, recommendations, ads ranking). These still need hand-engineered features, and feature stores are the backbone.
- **Embeddings as features** — deep networks produce embeddings (dense vectors learned from raw data). These embeddings are increasingly *stored in feature stores* and served to downstream models. Train a deep NN once; everything else consumes its output from the store.
- **Preprocessed inputs** — even end-to-end deep models need raw data in a normalized, cleaned, consistently-formatted form. Feature stores manage this preprocessing pipeline.
- **RAG systems** — chunk embeddings and metadata are essentially features for retrieval. Managing them in a feature store (or vector DB, a specialized cousin) is the same concept.

**Less relevant for pure deep learning:**
- If a model ingests raw pixels/audio/text directly and learns its own internal representations, you don't need to store intermediate features externally. The feature store problem is largely internal to the model in that case.

---

## The Key Insight

Feature stores solve an *operational* problem, not just a modeling one: **how do you ensure the same transformation of data is applied consistently across training, evaluation, and production inference?** That problem exists regardless of whether features were hand-crafted or learned — as soon as preprocessed inputs or derived representations are shared across systems or teams, a feature store earns its keep.

The modern framing: feature stores are evolving to handle both traditional engineered features *and* embeddings from deep models — converging with vector databases.

---

## Connection to This Project

- The [vector database](../builds/vector-db.md) built in Week 7 is a specialized cousin of a feature store — it stores and serves learned embeddings (produced by [embedding models](../tools/embedding-models.md)) for similarity search.
- [Feature engineering](../tools/feature-engineering.md) notes a central feature store as a key component of any feature engineering platform.
