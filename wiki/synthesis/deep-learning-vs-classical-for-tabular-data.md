# Deep Learning vs. Classical Methods for Tabular Data

**Filed from:** teaching session on feature engineering — when does deep learning win on tabular data?
**Related pages:** [Feature Engineering](../tools/feature-engineering.md), [Feature Stores in ML](feature-stores.md)

---

## The Surprising Reality

Deep learning dominates unstructured data (images, text, audio) so thoroughly that it's tempting to assume it's universally better. For tabular/structured data, the story is more complicated — classical methods (XGBoost, random forests + hand-engineered features) still win more often than not.

---

## Why Classical Methods Hold Up

**1. Tabular datasets are small by deep learning standards**
Most real-world tabular datasets have thousands to low millions of rows. Deep learning needs enormous volumes of data to discover good internal representations. XGBoost trained on 50k rows of loan data will almost always beat a neural net trained on the same data.

**2. Tabular data is heterogeneous**
Images are uniform — every pixel is the same type of input. Tabular data mixes continuous values (salary), integers (age), booleans (is_homeowner), and high-cardinality categoricals (employer) in the same row. Neural nets don't have a natural inductive bias for this mixture. Tree-based models handle it natively.

**3. Decision boundaries are often irregular**
Fraud detection rules look like: "IF salary < $40k AND loan_amount > $300k AND zip_code is in these 5 regions THEN high risk." Trees encode exactly this kind of rule. Neural nets can approximate it but need more data and tuning to get there.

**4. Interpretability requirements**
Finance, healthcare, and insurance often require regulatory explainability. "The model weighted debt-to-income ratio at 0.34" is explainable. "These 512 internal neurons fired" is not. Classical models win by default in regulated industries regardless of raw performance.

---

## The Gap Is Closing

Architectures designed specifically for tabular data have narrowed the gap significantly:

- **TabNet** (Google, 2019) — uses attention to select which features to focus on at each step, mimicking how trees split on features
- **TabTransformer** — applies transformer attention to categorical embeddings specifically
- **FT-Transformer** — treats each feature as a token and applies full transformer attention across all features

These architectures close the gap on larger datasets and sometimes outperform classical methods — but require more data and tuning to get there.

---

## Practical Decision Guide

| Situation | Recommendation |
|---|---|
| Unstructured data (images, text, audio) | Deep learning, almost always |
| Tabular data, 10M+ rows | Worth trying deep learning / TabNet |
| Tabular data, small/medium dataset | XGBoost + feature engineering |
| Regulated industry (finance, healthcare) | XGBoost + FE regardless of dataset size |
| Mixed system (tabular + text/images) | Hybrid: classical model + LLM as feature engineer |

---

## The Right Mental Model

"Advanced" doesn't mean "universally better." Deep learning dominance is real but domain-specific. The right tool depends on data type, data volume, and operational constraints. A model that explains its decisions and trains in seconds on a modest dataset often beats a black-box model that requires a GPU cluster.

---

## Related Synthesis

- [Feature Engineering End-to-End Architecture](feature-engineering-end-to-end-architecture.md) — how classical and LLM-based feature engineering combine in a production system
- [Feature Stores in ML](feature-stores.md) — the operational infrastructure that supports classical FE pipelines
