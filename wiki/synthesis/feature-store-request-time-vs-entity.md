# Feature Store: Request-Time vs. Entity Features

**Filed from:** Week 13 query — clarifying "request-time" features and how they apply at training time
**Related pages:** [Feature Stores](feature-stores.md), [Feature Store at Inference Time](feature-store-at-inference-time.md), [Feature Store: Preventing Training/Serving Skew](feature-store-training-serving-skew.md)

---

## The Confusion

"Request-time" features sounds like it only applies at inference time. But these features are also used at training time — which seems contradictory.

---

## What "Request-Time" Actually Means

"Request-time" means **computed from the event data itself, rather than from entity history**. The distinction is the *source* of the input data, not the context (training vs. serving).

- **Entity feature**: `avg_purchase_30d` for user 123 — requires looking up historical aggregates for that user. Cannot be computed from a single transaction record alone.
- **Request-time / on-demand feature**: `amount_normalized = amount / 1000.0` — computable from the transaction record itself, no history needed.

---

## How Training Uses Request-Time Features

At training time you have a dataset of historical events. For each one, you need to compute what the feature *would have been* at that moment. The on-demand function runs over each historical event record exactly as it runs over a live request:

```
Training:  historical transaction row  →  same function  →  amount_normalized
Serving:   live incoming request       →  same function  →  amount_normalized
```

The input source differs (historical rows vs. live request), but the function is identical. Registering it once in the feature store ensures both contexts call the same code.

---

## The Two-Dimensional View

A cleaner way to think about feature types:

| | Precomputed (batch) | Computed on-demand |
|---|---|---|
| **Source: entity history** | `avg_purchase_30d` — stored in online store, looked up at serving time | Less common — too slow to aggregate history on the fly |
| **Source: the event itself** | Rarely useful — no point batch-computing something derivable from the event | `amount_normalized`, `is_foreign` — computed fresh each time from the event record |

Request-time features live in the bottom-right: derived from the event record, computed fresh. At serving, that event is the live request. At training, that event is a historical row. Same computation, different time.

---

## Related Synthesis

- [Feature Stores in ML](feature-stores.md) — broader overview
- [Feature Store at Inference Time](feature-store-at-inference-time.md) — online store, entity lookup, latency
- [Feature Store: Preventing Training/Serving Skew](feature-store-training-serving-skew.md) — how the feature store enforces consistent computation
