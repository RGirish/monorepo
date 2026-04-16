# Why Feature Stores Matter at Inference Time

**Filed from:** Week 13 query — role of the feature store during serving/inference
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Feature Stores](feature-stores.md)

---

## Two Kinds of Features at Inference Time

**Request-time features** are derivable from the incoming request itself — the text of a message, the image being classified, the transaction amount. These are computed on the fly; the feature store plays no role here.

**Entity features** are properties of some *entity* (a user, a product, a merchant) that require historical context that cannot be derived from a single incoming request. Examples:
- "Average purchase value for user 123 over the last 30 days"
- "Number of failed login attempts for this account in the last hour"
- "This merchant's fraud rate over the last 90 days"

These must be precomputed and stored somewhere that can be looked up fast — that is the feature store's **online store**.

---

## The Online Store vs. Offline Store

Most feature stores have two layers:

| Layer | Backend | Used for | Latency requirement |
|---|---|---|---|
| Offline store | Data warehouse (BigQuery, S3) | Training — historical feature values | High latency OK (batch) |
| Online store | Key-value store (Redis, DynamoDB) | Serving — latest feature value per entity | Must be low (sub-100ms) |

At inference time, the serving system:
1. Receives a request: "predict churn probability for user_id=123"
2. Looks up user 123's entity features from the **online store** (sub-millisecond key-value lookup)
3. Combines them with request-time features
4. Passes the full feature vector to the model
5. Returns the prediction

A batch pipeline (running continuously or on a schedule) keeps the online store current — it recomputes entity features and writes the latest values in.

---

## Why Not Just Query the Source Database Directly?

You could, but:
- **Latency** — aggregations like "30-day rolling average" computed from raw transaction rows on every request won't meet sub-100ms requirements
- **Training/serving skew** — if the serving code recomputes features differently from the training pipeline, the model sees a different distribution at inference than it was trained on. The feature store guarantees the *same transformation logic* produces the value in both contexts.
- **Reuse** — the same entity features serve many models and many requests without recomputation

---

## The Short Version

The feature store's online store is a precomputed lookup table: "for entity X, here is their current feature vector." It exists because many useful features require historical context that is too expensive to compute on each request, and too important to risk computing differently between training and serving.

---

## Related Synthesis

- [Feature Stores in ML](feature-stores.md) — broader overview of what feature stores are and why they matter
- [Weights vs. Embeddings vs. Features](weights-vs-embeddings-vs-features.md) — clarifying what artifact goes in which system
