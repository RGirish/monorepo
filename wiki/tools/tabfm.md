# TabFM — Zero-Shot Foundation Model for Tabular Data

**Covered in:** [Week 17](../weeks/week-17-2026-04-27.md)

Sources: [Google Research blog](https://research.google/blog/introducing-tabfm-a-zero-shot-foundation-model-for-tabular-data/), [google-research/tabfm README](https://github.com/google-research/tabfm)

---

## What It Is

TabFM applies in-context learning (ICL) — the same mechanism that lets an LLM follow a few examples in a prompt without fine-tuning — to tabular classification and regression. Instead of training a model per dataset (the standard XGBoost/LightGBM workflow: feature engineering, then hyperparameter tuning, then a training run), TabFM treats the training table itself as the "prompt": pass the training rows plus a query row, get a prediction back in a single forward pass, with no retraining or tuning per task.

## Architecture

Three mechanisms make "read the whole dataset as context" tractable:

1. **Alternating attention** — attends across both columns (features) and rows (examples), so feature interactions are picked up automatically rather than requiring hand-engineered interaction terms.
2. **Row compression** — individual rows are compressed into dense embeddings before the expensive attention step.
3. **Efficient ICL layer** — the Transformer operates on the compressed embeddings, not raw values, keeping the "whole table as context" approach computationally feasible.

## Training Data

Trained entirely on hundreds of millions of **synthetic** datasets generated from structural causal models — no real-world tabular data at all. The stated reason: diverse, high-quality, licensable tabular datasets are scarce, unlike text or images.

## Benchmarks and Deployment

Evaluated on TabArena (38 classification + 13 regression datasets, 700–150,000 rows), reported via Elo-style ratings against tuned tree ensembles. Two variants: plain **TabFM** (zero-shot, no tuning) and **TabFM-Ensemble** (adds cross-features, SVD features, and calibration on top). Shipping path is Google BigQuery's `AI.PREDICT` SQL command — no ML expertise required to call it.

## Practical Usage (from the repo)

Scikit-learn-shaped API:

```python
from tabfm import TabFMClassifier
clf = TabFMClassifier(model=model)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
```

Pandas DataFrame input (mixed numeric/categorical), JAX or PyTorch backend. Defaults: `max_num_features=500`, `max_num_rows=100` — the context passed at inference is capped, not the full training set. Code is Apache-2.0; **pretrained weights are non-commercial licensed**, so production use of Google's released weights requires a separate commercial agreement (rewriting the architecture and training your own weights would not carry this restriction).

## Discussion: Does Zero-Shot Really Replace Feature Engineering?

The headline claim — alternating attention discovers feature interactions automatically, eliminating manual feature engineering — is weaker than it first appears:

- **The Ensemble variant undercuts the pitch.** TabFM-Ensemble adds cross-features and SVD features back on top of raw TabFM to be competitive, which is automated feature engineering bolted back on. That TabFM needed it is evidence that raw in-context attention alone doesn't fully substitute for engineered features. See [Feature Engineering](feature-engineering.md) for the manual techniques (interaction terms, encoding strategy) TabFM is implicitly competing against.
- **`max_num_rows=100` reframes the value proposition.** TabFM doesn't eliminate the training-time optimization problem, it moves it to inference time and shrinks its scope: not "engineer good features from the full dataset once," but "select a good sample of ≤100 rows as context, per query." Naive random sampling wastes the budget on irrelevant rows.
- **Nearest-neighbor context selection reintroduces the same problem it's meant to avoid.** Picking the 100 rows most similar to the query row (retrieval-augmented ICL, structurally identical to what the [Vector Database](../builds/vector-db.md) build does) requires a distance metric over mixed numeric/categorical columns — which means normalizing ranges and encoding categoricals, i.e., a lighter version of the same feature engineering being skipped.
- **Pure nearest-neighbor context can be too local.** If the query row sits in a sparse region of feature space, its 100 nearest neighbors may share a narrow bias (one time period, one category) and lose the global signal a broader sample would carry — especially costly for regression, where context should span the target's range.
- **Maximal Marginal Relevance (MMR)** is the standard fix from the RAG literature: retrieve a larger candidate pool via ANN search, then greedily select down to budget while penalizing redundancy with already-chosen rows, balancing relevance against diversity.

**Net take:** TabFM's zero-shot framing is real (no per-dataset training run), but "no work required" is oversold — the work relocates from feature engineering (once, offline, over the full dataset) to context curation (per query, at inference time, over a capped sample), and doing that well is a non-trivial retrieval problem in its own right.

## Related Tools

- [Feature Engineering](feature-engineering.md) — the manual work (interaction terms, encoding) TabFM's alternating attention aims to replace, and the Ensemble variant's evidence that it doesn't fully succeed
- [Embedding Models](embedding-models.md) — similarity metrics and retrieval, the same operations needed to select TabFM's in-context rows

## Related Builds

- [Vector Database](../builds/vector-db.md) — nearest-neighbor retrieval over stored vectors; structurally the same operation as picking TabFM's context rows
