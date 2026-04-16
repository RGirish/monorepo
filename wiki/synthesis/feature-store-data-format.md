# What Data in a Feature Store Actually Looks Like

**Filed from:** Week 13 query — data format and structure inside a feature store
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Feature Stores](feature-stores.md), [Feature Store at Inference Time](feature-store-at-inference-time.md), [Embedding Models](../tools/embedding-models.md), [Vector Database](../builds/vector-db.md)

---

## The Canonical Unit: A Feature Row

Feature store data is **structured tabular data** — scalar values keyed by entity ID. Not vectors, not JSON documents, not code.

**Online store** (Redis, DynamoDB) — keyed by entity ID, returns the latest values:

```
user_id: 12345
────────────────────────────────────
avg_purchase_value_30d:    47.82
num_transactions_7d:       3
account_age_days:          412
days_since_last_login:     2
preferred_category:        "electronics"
fraud_risk_score:          0.03
```

A named bag of numbers and categoricals. Internally serialized as Protocol Buffers or a compact binary format for speed, but logically it is just a flat row keyed by entity ID.

**Offline store** (BigQuery, Parquet on S3) — same data with a timestamp column per row, enabling point-in-time correct joins for training:

```
user_id | event_timestamp      | avg_purchase_30d | num_txns_7d | fraud_risk_score
12345   | 2026-04-15 09:00:00  | 47.82            | 3           | 0.03
12345   | 2026-04-14 09:00:00  | 43.20            | 4           | 0.05
67890   | 2026-04-15 09:00:00  | 120.50           | 12          | 0.01
```

---

## What About Embeddings?

Embeddings can be stored as a feature — they appear as an array column:

```
user_id: 12345
user_embedding:  [0.23, -0.41, 0.87, 0.11, ...]   ← 128 floats
```

But embeddings are often stored separately in a **vector database** (optimized for similarity search over arrays), since feature stores are not designed for nearest-neighbor queries.

---

## What Is NOT Stored in a Feature Store

- **Transformation code** — how `avg_purchase_value_30d` is computed from raw transactions lives in the feature pipeline (Python/SQL), not in the store. Some systems store it as metadata for lineage, but the store holds computed results only.
- **Raw data** — that lives upstream in the data warehouse or data lake.
- **Model weights** — those are in the model registry.

---

## Schema Definition (Feast example)

Feature stores hold a schema definition as metadata — this is not the data itself:

```python
user_stats = FeatureView(
    name="user_stats",
    entities=["user_id"],
    features=[
        Feature("avg_purchase_value_30d", ValueType.FLOAT),
        Feature("num_transactions_7d",    ValueType.INT64),
        Feature("fraud_risk_score",       ValueType.FLOAT),
        Feature("preferred_category",     ValueType.STRING),
    ],
    ttl=timedelta(days=7),
)
```

This defines column names, types, and freshness TTL. The actual values come from running the pipeline.

---

## Summary

| What you might expect | What it actually is |
|---|---|
| Vectors / embeddings | Scalar numerics and categoricals (embeddings are a special case, often in a vector DB instead) |
| JSON documents | Flat structured records, binary-serialized (Protobuf, Avro) for speed |
| Code / transformation logic | Upstream in the pipeline; store holds computed results only |
| Unstructured binary | No — always schema-defined, typed columns |

---

## Related Synthesis

- [Feature Stores in ML](feature-stores.md) — what feature stores are and why they matter
- [Feature Store at Inference Time](feature-store-at-inference-time.md) — how the online store serves features during prediction
- [Weights vs. Embeddings vs. Features](weights-vs-embeddings-vs-features.md) — what artifact goes in which system
