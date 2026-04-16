# Weights vs. Embeddings vs. Features — What Gets Stored Where

**Filed from:** Week 13 query — clarifying embeddings vs. model weights vs. features
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Embedding Models](../tools/embedding-models.md), [Feature Stores](feature-stores.md), [Vector Database](../builds/vector-db.md)

---

## The Three Artifacts

**Model weights** are the parameters *inside* a trained model — the numbers learned during training that define how the network transforms inputs. They live inside the model itself and are not served to other systems directly. You deploy the model as a whole; the weights are an implementation detail of that model.

**Embeddings** are the *output* of running data through a trained model (or a specific layer of one). When you pass a sentence through a sentence-transformer, the dense vector it returns is an embedding. Embeddings are computed *from* the model using its weights, but they are a separate artifact — a representation of a specific piece of data, not the model itself.

**Features** are any derived representation of raw data fed into a model — including embeddings, but also hand-engineered values (one-hot encodings, normalized numerics, lag features, etc.).

**Analogy:** weights are the recipe; embeddings are a dish cooked using that recipe. You store dishes in the fridge (feature store / vector DB); the recipe lives in a recipe book (model registry).

---

## What Gets Stored Where

| System | Stores | Serves |
|---|---|---|
| Feature store | Engineered features, precomputed embeddings | Training pipelines, inference services |
| Vector database | Embeddings (optimized for similarity search) | RAG systems, recommenders |
| Model registry | Model weights + metadata | Deployment, rollback, A/B testing |

Models go in **model registries** (MLflow, Hugging Face Hub, Vertex AI Model Registry), which handle versioning, lineage, deployment, and A/B testing of model artifacts. Feature stores and model registries are complementary but separate systems.

---

## How They Connect in Practice

A typical ML pipeline ties all three together:

1. Raw data → **feature store** (engineered features or precomputed embeddings)
2. Feature store → training pipeline → trained model → **model registry**
3. At inference: feature store serves features + model registry serves the model → prediction

Embeddings feel like they "belong" to the model because they are produced by it — but once computed, they become data artifacts that need the same versioning and serving guarantees as any other feature. That is why they end up in feature stores and vector DBs, not model registries.

---

## Related Synthesis

- [Feature Stores in ML](feature-stores.md) — broader context on what feature stores are and why they remain relevant beyond hand-engineered features
