# Feature Engineering End-to-End Architecture

**Filed from:** teaching session on feature engineering — synthesizing the full pipeline
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Feature Stores in ML](feature-stores.md), [Feature Store at Inference Time](feature-store-at-inference-time.md), [Deep Learning vs. Classical for Tabular Data](deep-learning-vs-classical-for-tabular-data.md)

---

## The Scenario: Fraud Detection at a Bank

A concrete end-to-end example that ties together classical FE, LLM-as-feature-engineer, offline/online stores, and real-time serving.

**Inputs available:**
- Structured transaction data and user history (tabular)
- Free-text customer support tickets (unstructured)

**Goal:** predict whether a transaction is fraudulent, in real time.

---

## The Full Pipeline

```
Raw data sources
      │
      ├── Transaction history (structured)
      │         │
      │         ▼
      │   Classical FE pipeline
      │   (domain-engineered features)
      │         │
      └── Support tickets (unstructured)
                │
                ▼
          LLM feature extraction
          (sentiment, fraud flags,
           urgency scores)
                │
                ▼
         Both feed into...
                │
         ┌──────▼──────┐
         │ Offline Store│  ← training snapshots, point-in-time correct
         └──────┬───────┘
                │ nightly sync
         ┌──────▼───────┐
         │ Online Store  │  ← latest features per user_id, Redis/DynamoDB
         └──────┬────────┘
                │
         Live transaction arrives
                │
         ┌──────▼────────────────────────┐
         │ Serving engine                 │
         │  - fetch user features (2ms)   │
         │  - compute request-time feats  │
         │    (transaction amount,        │
         │     is_foreign, time_of_day)   │
         │  - run fraud model             │
         └──────┬────────────────────────┘
                │
         approve / flag / reject
```

---

## Stage 1: Classical Feature Engineering (Structured Data)

Apply domain expertise to transaction history and user profile:

- `debt_to_income_ratio` — loan_amount / salary
- `avg_transaction_amount_30d` — rolling 30-day average spend
- `transaction_velocity_1h` — number of transactions in the last hour
- `days_since_account_opened` — account age
- `is_new_merchant` — boolean: has the user transacted with this merchant before?
- `zip_code_risk_score` — precomputed fraud rate by zip code

These are computed by a batch pipeline and written to the **offline store** keyed by `user_id`.

---

## Stage 2: LLM as Feature Engineer (Unstructured Data)

Customer support tickets contain signals classical FE can't easily capture. Run each ticket through an LLM to extract structured features:

```
prompt: "Given this support ticket, extract:
  - sentiment: positive / negative / neutral
  - urgency: 1–5
  - complaint_type: billing / technical / account / fraud_report / other
  - is_repeat_complaint: yes / no

Ticket: [ticket text]"
```

The LLM outputs structured rows that get written to the same offline store alongside the classical features. The model sees both as regular columns — it doesn't know or care which were hand-engineered and which were LLM-extracted.

This runs as part of the same nightly batch pipeline — the LLM is called offline, not at serving time. Latency is irrelevant here.

---

## Stage 3: Offline Store → Training Dataset

To train the fraud model, pull a point-in-time correct snapshot from the offline store:

- For each historical transaction labeled as fraud/not-fraud, retrieve the feature values that existed **on the day of that transaction** — not today's values
- This prevents data leakage: the model cannot see future account history when learning about a past event

The offline store is a data warehouse (BigQuery, S3 + Parquet). Queries run slowly — that's fine for a training job.

---

## Stage 4: Online Store → Real-Time Serving

A nightly sync populates the **online store** (Redis, DynamoDB) with the latest feature values per `user_id`. At serving time:

1. Transaction arrives: `{user_id: 12345, amount: $4,200, merchant: "unknown_electronics", country: "RU"}`
2. Fetch precomputed features from online store: `avg_transaction_amount_30d`, `is_repeat_complaint`, `transaction_velocity_1h`, etc. — ~2ms
3. Compute **request-time features** on the fly from the transaction itself: `is_foreign` (country ≠ home country), `amount_deviation` (how far above the user's average), `time_of_day` — ~5ms
4. Combine all features → run fraud model → return score

Total latency: ~10–20ms, well within the window needed to approve/decline a transaction.

---

## Stage 5: Monitoring

After deployment, continuously monitor:
- **Feature distribution drift** — are the features in the online store drifting from what the model was trained on? Catches silent degradation before it becomes a business problem.
- **Model performance metrics** — precision/recall on flagged transactions, false positive rate (legitimate transactions blocked)
- **Log features used per prediction** — necessary for debugging; without this log, reconstructing what the model saw for a disputed transaction is nearly impossible

---

## Key Design Decisions

| Decision | Choice | Why |
|---|---|---|
| Model type | XGBoost (classical) | Tabular dataset, regulatory explainability required, dataset size fits classical methods |
| Unstructured data | LLM extracts features offline | Preserves classical model's advantages while extracting signal from text |
| LLM invocation | Batch (offline), not at serving time | LLM latency (~500ms) is incompatible with real-time transaction approval |
| Feature store | Offline + online | Training needs historical snapshots; serving needs sub-millisecond lookup |

---

## Related Synthesis

- [Deep Learning vs. Classical for Tabular Data](deep-learning-vs-classical-for-tabular-data.md) — why XGBoost was chosen over a neural net here
- [Feature Stores in ML](feature-stores.md) — what feature stores are and why they exist
- [Feature Store at Inference Time](feature-store-at-inference-time.md) — online store mechanics, latency requirements
- [Feature Store: Preventing Training/Serving Skew](feature-store-training-serving-skew.md) — how the single feature definition prevents divergence
