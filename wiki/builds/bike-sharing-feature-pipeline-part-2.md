# Bike Sharing Feature Pipeline (Part 2)

**Built in:** [Week 16](../weeks/week-16-2026-04-20.md) — continues [Part 1](bike-sharing-feature-pipeline.md) ([Week 13](../weeks/week-13-2026-03-30.md))
**Code:** [machine-learning/feature-engineering](https://github.com/RGirish/monorepo/tree/main/code/machine-learning/feature-engineering)

---

## What It Is

Three more stages of feature engineering on the same [Bike Sharing Demand pipeline](bike-sharing-feature-pipeline.md), built forward from Part 1's best-performing feature set — time-derived/cyclical features (RMSLE 0.7365) — rather than Part 1's one-hot-encoded stage, which had measured slightly worse. Same evaluation setup throughout: `GradientBoostingRegressor`, 5-fold cross-validation, RMSLE.

## Numeric Transforms & Interactions (RMSLE = 0.6646)

Added four columns to Part 1's stage-2 feature set:
- `temp_band`, `humidity_band` — ordinal bins (`pd.cut` into 4 buckets each). Unlike `season`/`weather` (nominal, no real order), temperature and humidity bands genuinely are ordered, so integer codes are the correct encoding here, not just a tree-model workaround.
- `temp_humidity` — `temp × humidity`, an interaction meant to capture "hot and humid discourages riders more than either alone."
- `workingday_rush` — `workingday × is_rush_hour`, capturing that rush-hour demand spikes are conditional on it actually being a working day.

This produced the largest single jump in the entire pipeline (0.7365 → 0.6646). An ablation run — bins only vs. interactions only — isolated the cause precisely:

| Variant | RMSLE |
|---|---|
| Bins only | 0.7366 (no change vs. stage 2's 0.7365) |
| Interactions only | 0.6646 (identical to the full stage) |

The bins added nothing because a tree can already pick any threshold on the raw continuous `temp`/`humidity` columns — bucketing them into 4 fixed bands handed the model a strictly coarser version of information it already had. The interactions helped because a tree's splits are axis-aligned (one column at a time); a smooth multiplicative relationship like `temp × humidity` can only be approximated through many stacked splits, and this model's trees are capped at depth 3. Handing the product over as one column let a single split capture what would otherwise take many.

Digging one level further (via feature importances in the next stage) showed this result actually decomposes into one dominant feature: `workingday_rush` alone was the single most important feature in the whole model, while `temp_humidity` turned out to be nearly the least important. `temp_humidity`'s correlation with the actual target (`count`) is only 0.07 — far weaker than `temp` (0.40) or `humidity` (−0.32) individually — because `temp` and `humidity` move in *opposite* directions relative to ridership, so multiplying them together muddles the two signals rather than amplifying a "discomfort" effect. A plausible-sounding domain interaction still needs to be checked against the data, not just assumed.

## Feature Selection (RMSLE = 0.6647)

Trained the full stage-4 feature set (21 columns), read off `model.feature_importances_`, and dropped every column contributing less than 1% of total importance — 9 columns, including both `temp_band` and `humidity_band` (confirming the ablation result) and `temp_humidity`.

| Feature | Importance |
|---|---|
| `workingday_rush` | 0.2516 |
| `time_of_day` | 0.1525 |
| `hour_cos` | 0.1355 |
| `hour_sin` | 0.1029 |
| `year` | 0.0984 |
| `temp` | 0.0972 |
| `feel_temp` | 0.0612 |
| ... (14 more, each < 0.03) | |

Pruned RMSLE (0.6647) tied the full feature set (0.6646) within noise, using 12 columns instead of 21 — feature selection didn't buy accuracy here, but it did buy a simpler, equally-accurate model, which is a legitimate outcome in its own right.

## Summary

| Stage | Features | RMSLE |
|---|---|---|
| 1 — baseline | Raw fields, naive category codes | 0.7842 |
| 2 — time-derived features | + cyclical hour/month, weekend/rush-hour flags | 0.7365 |
| 3 — categorical encoding | One-hot instead of naive codes | 0.7415 |
| 4 — numeric transforms/interactions | + ordinal bins, `temp_humidity`, `workingday_rush` | 0.6646 |
| 5 — feature selection | Pruned to 12 columns by importance | 0.6647 |

Across the full pipeline, the single largest driver of accuracy wasn't the categorical-encoding fix or the time-feature work — it was one interaction term (`workingday_rush`) discovered by reasoning about the domain (rush hour only means something on a working day), not by applying a standard textbook technique. The one deliberately domain-motivated interaction that *didn't* pan out (`temp_humidity`) still needed an empirical check to catch, despite sounding equally plausible going in.

## Related Builds

- [Bike Sharing Feature Pipeline](bike-sharing-feature-pipeline.md) — Part 1: baseline, time-derived features, categorical encoding

## Related Tools

- [Feature Engineering](../tools/feature-engineering.md) — classical technique background (binning, interaction features)

## Related Concepts

- [Tree Ensemble Mechanics](../concepts/tree-ensemble-mechanics.md) — gradient boosting internals, feature importance mechanics, why trees can't reconstruct interactions from axis-aligned splits
