# Bike Sharing Feature Pipeline

**Built in:** [Week 13](../weeks/week-13-2026-03-30.md) (stages 1–3) · [Week 15](../weeks/week-15-2026-04-13.md) (stages 4–6, planned)
**Code:** [machine-learning/feature-engineering](https://github.com/RGirish/monorepo/tree/main/code/machine-learning/feature-engineering)
**Status:** in progress — 3 of 6 stages complete

---

## What It Is

A feature engineering pipeline built directly against the backlog idea "engineer features manually and measure model lift at each step." A gradient-boosted tree model is retrained from scratch at each stage on the same rows, with only the feature set changing, so the RMSLE delta between stages is attributable to that stage's engineering decision alone — not to noise or a different train/test split (the same 5-fold cross-validation setup, same random seed, is reused throughout).

## Dataset

[Bike Sharing Demand](https://www.openml.org/search?type=data&id=42712) (via `sklearn.datasets.fetch_openml`, no Kaggle auth required) — ~17,400 hourly records from a Washington D.C. bike-share system. Each row: time context (`year`, `month`, `hour`, `weekday`, `holiday`, `workingday`), weather (`season`, `weather`, `temp`, `feel_temp`, `humidity`, `windspeed`), and ride counts (`casual`, `registered`, `count`). Target: `count`, predicted from time/weather context alone.

This OpenML copy already splits `year`/`month`/`hour`/`weekday` into separate columns rather than shipping one raw `datetime` string — so "date decomposition" wasn't available as a stage; the pipeline instead uses those pre-split columns as the input to derived/cyclical time features (stage 2).

**Leakage note:** `casual` and `registered` are dropped before any stage runs. `casual + registered = count` exactly — leaving them in would let the model learn a trivial identity instead of anything about weather/time, and neither column exists at real inference time anyway.

## Stages

### Stage 1 — Baseline (RMSLE = 0.7842)

Raw fields only, with categorical columns (`season`, `holiday`, `workingday`, `weather`) converted to arbitrary integer codes purely so the model can consume them — no engineering beyond what's required to run at all. This is the number every later stage is measured against.

### Stage 2 — Time-derived features (RMSLE = 0.7365, best result)

Added on top of stage 1:
- `is_weekend` — derived from `weekday` (the two weekday values that are always `workingday=False`)
- `is_rush_hour` — `hour` in {7,8,9,17,18,19}
- `time_of_day` — `hour` bucketed into night/morning/afternoon/evening
- `hour_sin`/`hour_cos` and `month_sin`/`month_cos` — replaced raw `hour`/`month` integers with their (x, y) position on a 24-hour / 12-month circle

The cyclical encoding fixes a real problem: as plain integers, hour 23 and hour 0 are one hour apart in reality but maximally far apart on the number line (difference of 23), forcing the model to learn "near midnight" as two disconnected rules instead of one. Mapping hour onto a circle puts them geometrically close again. Two columns (sin *and* cos) are required because either one alone is ambiguous — e.g. `sin` gives the same value for two different times of day, so both coordinates together are needed to pin down a unique point on the circle.

### Stage 3 — Proper categorical encoding (RMSLE = 0.7415, slightly worse)

Replaced the naive integer codes for nominal categoricals (`season`, `weather`, `time_of_day`) with one-hot encoding; binary columns (`holiday`, `workingday`) were left as 0/1 since there's no false ordering to fix on a 2-value column. This is the textbook "correct" way to encode categoricals — and it made the score slightly worse here, not better.

This is a real, useful result, not a bug: one-hot encoding's benefit is aimed at models that treat feature values as magnitudes (linear regression, KNN, neural nets), where an arbitrary code like `season=3` would wrongly imply "3× more season" than `season=0`. Gradient-boosted trees never do that arithmetic — they only ask threshold questions — so the naive codes were already "good enough," and one-hot introduced a **fragmentation** cost instead: splitting one 4-way categorical decision into 4 separate 0/1 columns competes for the same fixed, shallow split budget (`GradientBoostingRegressor`'s default tree depth is 3) against every other feature. Full mechanism in [Tree Ensemble Mechanics](../concepts/tree-ensemble-mechanics.md).

## Results

| Stage | Features | RMSLE |
|---|---|---|
| 1 | Raw fields, naive category codes | 0.7842 |
| 2 | + time-derived/cyclical features | **0.7365** |
| 3 | + one-hot categorical encoding | 0.7415 |

Best result so far is stage 2. Stages 4–6 (numeric transforms/interactions, feature selection, wrap-up) continue in Week 15.

## Related Tools

- [Feature Engineering](../tools/feature-engineering.md) — classical technique background (encoding, scaling, binning); this build is the hands-on application

## Related Concepts

- [Tree Ensemble Mechanics](../concepts/tree-ensemble-mechanics.md) — how gradient boosting trains, why encoding strategy is model-family-dependent, fragmentation, cross-validation, RMSLE
