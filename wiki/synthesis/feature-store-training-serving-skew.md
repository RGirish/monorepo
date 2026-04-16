# How Feature Stores Actually Prevent Training/Serving Skew

**Filed from:** Week 13 query — if feature stores don't store code, how do they prevent skew?
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Feature Stores](feature-stores.md), [Feature Store at Inference Time](feature-store-at-inference-time.md)

---

## The Question

If a feature store only stores computed values (not transformation code), how does it prevent training and serving from computing features differently?

---

## Part 1: For Precomputed Entity Features, the Code Doesn't Run Twice

For batch-computed entity features (e.g., `avg_purchase_30d`), the feature store prevents skew not by sharing code — but by ensuring **the code runs exactly once, and both training and serving read the same precomputed result**.

```
Batch pipeline runs → computes avg_purchase_30d → writes to feature store
                                                         ↓
Training reads from feature store ──────────────────────┘
Serving reads from feature store  ──────────────────────┘
```

Neither training nor serving recomputes the feature. There is only one computation. No opportunity for divergence.

**Without a feature store:**
```
Training pipeline  → computes avg_purchase_30d in Pandas/Python
Serving code       → recomputes avg_purchase_30d in Java/Go
```
Two implementations, two opportunities to diverge. This is where skew lives.

---

## Part 2: For On-Demand / Request-Time Features, You Register the Logic Once

For features that must be computed fresh from the incoming request, modern feature stores (Tecton, Feast) let you register a **transformation function** once. The store calls the same function at both training time and serving time.

```python
@on_demand_feature_view(...)
def transaction_features(transaction: Dict) -> Dict:
    return {
        "amount_normalized": transaction["amount"] / 1000.0,
        "is_foreign": transaction["country"] != "US",
    }
```

- At training time: the store calls this function over historical events to build the training dataset
- At serving time: the store calls the same function on the incoming request

Same definition, same execution path — skew eliminated at the source.

---

## The Root Cause of Skew (Without a Feature Store)

The old problem was not that people intended to compute things differently — it was that training and serving were maintained by different teams in different codebases, often in different languages. The feature store imposes a single registration point for feature logic, making divergence structurally hard rather than just culturally discouraged.

---

## Summary

| Feature type | How skew is prevented |
|---|---|
| Precomputed entity features | Code runs once; both training and serving read the stored result |
| On-demand request-time features | Transformation function registered once; store calls it in both contexts |

---

## Related Synthesis

- [Feature Stores in ML](feature-stores.md) — broader overview of what feature stores are
- [Feature Store at Inference Time](feature-store-at-inference-time.md) — online store, entity lookup, latency requirements
- [Feature Store Data Format](feature-store-data-format.md) — what the stored data actually looks like
