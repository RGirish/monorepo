# Tree Ensemble Mechanics

**Appears in:** [Week 13](../weeks/week-13-2026-03-30.md) · [Week 16](../weeks/week-16-2026-04-20.md)

---

## Overview

Concepts that surfaced while building the [Bike Sharing Feature Pipeline](../builds/bike-sharing-feature-pipeline.md) ([Part 1](../builds/bike-sharing-feature-pipeline.md), [Part 2](../builds/bike-sharing-feature-pipeline-part-2.md)) — not feature engineering itself, but the model mechanics and evaluation methodology needed to measure it. These are general ML fundamentals, independent of any one dataset, and likely to recur whenever a tree-based model shows up again (e.g. the backlogged supervised-learning build).

---

## How Gradient Boosting Trains

A single decision tree is a nested if/else chain ending in a predicted number per leaf — fast, but crude. Gradient boosting builds many small trees **sequentially**, where each new tree's job is to predict the *errors* (residuals) still left by the trees before it:

1. Tree 1 predicts the target roughly → some error remains per row.
2. Tree 2 is trained to predict *that error*, not the raw target.
3. Combined prediction = Tree 1's guess + a fraction of Tree 2's correction.
4. Tree 3 targets whatever error is still left after 1+2. Repeat (~100 rounds by default in scikit-learn's `GradientBoostingRegressor`).

This is the same shape as an iterative error-correction loop: each pass shrinks the residual rather than solving everything in one shot. `model.fit()` runs this whole sequential-tree-building process and stores the resulting trees; `model.predict()` just runs a new row through all of them and sums their contributions — no further learning happens at predict time.

## Categorical Encoding Is Model-Family-Dependent

The common advice "always one-hot your categoricals" is aimed at models that treat feature values as **magnitudes** — linear regression, KNN, neural nets — where an arbitrary integer code like `season=3` would wrongly be read as "3× more season" than `season=0`.

Tree-based models never do that arithmetic. A tree only asks threshold questions (`code > 1.5?`), so an arbitrary ordering across categories doesn't bias it the way it would a linear model. In the bike-sharing build, replacing naive integer codes with one-hot encoding for `season`/`weather`/`time_of_day` actually made a gradient-boosted model *slightly worse* (RMSLE 0.7365 → 0.7415) — a concrete counter-example to treating one-hot as a universal default.

### Fragmentation

The mechanism behind that result: one-hot encoding turns a single N-way categorical decision into N separate binary columns. A tree that could previously isolate a category group with one split (e.g. `code ≤ 1` peeling off two categories at once from a naive-coded column) may now need several sequential splits across several one-hot columns to reconstruct the same grouping.

This matters because of a **fixed split budget per tree** — `GradientBoostingRegressor`'s default max depth is only 3 levels (8 leaves per tree). Splitting one categorical decision across 4 columns means those columns are now competing for the same small, shallow budget against every other feature in the dataset. Critically, this isn't a data-*volume* problem — more training rows don't loosen a fixed tree-depth constraint. The actual levers are tree depth and number of boosting rounds (more model capacity), not more examples.

## Cyclical (Wraparound) Encoding

Applies to any periodic feature — hour-of-day, day-of-week, month-of-year, wind direction in degrees. Plain integers break at the wraparound point: hour 23 and hour 0 are one hour apart in reality but maximally far apart as raw numbers (difference of 23), forcing a model to learn "near midnight" as two disconnected rules instead of one continuous one.

Fix: map the value onto a circle and use its (x, y) coordinates — `sin(2π·hour/24)` and `cos(2π·hour/24)`. Hour 23 and hour 0 now sit close together in (sin, cos) space. Two columns are required, not one, because a single coordinate is ambiguous (e.g. two different hours can share the same `sin` value); both together uniquely locate one point on the circle.

## Interaction Terms vs. Axis-Aligned Splits

A tree's splits look at one column at a time (`temp > 68?`, then `humidity > 70?`), which carves the data into axis-aligned rectangular regions. A genuinely multiplicative relationship — like "hot AND humid discourages riders more than either alone" — is a smooth, diagonal boundary in feature space, and approximating a diagonal with only horizontal/vertical cuts takes many stacked splits (a "staircase"). With a shallow tree (depth 3, 8 leaves), there's very little budget for that staircase.

Handing the model the literal product (`temp × humidity`) as one column lets a single threshold split capture what would otherwise take many splits to approximate. In the bike-sharing build, this is why interaction terms produced the single largest RMSLE improvement in the whole pipeline (0.7365 → 0.6646), while binning the same continuous variables into buckets did essentially nothing — a tree can already threshold a continuous column at any value it wants, so a fixed-width bucketed version is strictly less informative than what it already had access to.

The catch: a plausible-*sounding* interaction still needs empirical verification. `temp × humidity` sounds like a reasonable "discomfort index," but its correlation with the actual target turned out to be only 0.07 — far weaker than `temp` (0.40) or `humidity` (−0.32) individually — because the two inputs move in *opposite* directions relative to the target, so multiplying them muddles the signal rather than amplifying it. Meanwhile a different interaction in the same build, `workingday × is_rush_hour`, captured a real conditional relationship (rush-hour demand spikes only make sense on working days) and became the single most important feature in the model. Domain reasoning identifies interaction *candidates*; only checking against the data tells you which ones actually work.

## Feature Importance

`model.feature_importances_` (scikit-learn) measures how much error-reduction each column was actually responsible for, summed across every split in every tree, normalized so all columns sum to 1. A column with importance ≈ 0 wasn't necessarily uninformative on its own — it means the trees never found it *useful to split on*, given everything else already available.

This has a specific consequence for correlated features: gradient boosting is greedy and sequential (see "How Gradient Boosting Trains" above) — each split is chosen to reduce whatever error is *still left* after every earlier split. If two columns carry overlapping information, whichever one gets used first "claims" the importance for that shared signal, and the other has little residual error left to explain by the time it's considered. Importance therefore reflects each feature's *marginal, sequential* contribution to reducing error — not a standalone measure of how correlated it is with the target. (Note this isn't about literal chronological order of columns in a DataFrame — trees evaluate every candidate column at every split regardless of position — it's about which feature's split threshold happens to best match the current residual pattern at each step of the boosting process.)

## Cross-Validation

Evaluating on one train/test split risks reporting a score that's really just luck of which rows landed in "test." `KFold(n_splits=5)` instead splits the dataset into 5 equal chunks and runs 5 experiments, each holding out a different chunk as validation while training on the rest, then averages the 5 scores. Same instinct as running a test suite across multiple random seeds instead of trusting a single run — it tells you a score is a stable property of the features/model, not an artifact of one lucky split. Using the same `random_state` across every stage means the same 5 splits are reused each time, so a score change is attributable to the feature change, not to different data landing in different folds.

## RMSLE (Root Mean Squared Log Error)

Built up piece by piece:
- **Error**: `predicted - actual` for one row.
- **Log**: take `log(1 + value)` of both before comparing, so the metric penalizes *relative* miss rather than absolute miss — a 5-unit miss on a true value of 10 is a much bigger mistake than a 5-unit miss on a true value of 400. Matters most when the target is skewed (many small values, a few large spikes), as bike rental counts are.
- **Squared**: prevents positive and negative errors from canceling, and penalizes large misses disproportionately more than small ones.
- **Mean**: average the squared-log-error across all rows.
- **Root**: undoes the squaring so the final number is back on a scale similar to the log-error itself.

Lower is better; the number is only meaningful as a comparison point between stages/models, not in isolation.

---

## Related Builds

- [Bike Sharing Feature Pipeline](../builds/bike-sharing-feature-pipeline.md) — Part 1: where the encoding/fragmentation concepts were applied and the one-hot vs. naive-encoding result was observed
- [Bike Sharing Feature Pipeline (Part 2)](../builds/bike-sharing-feature-pipeline-part-2.md) — Part 2: where the interaction-term and feature-importance concepts were applied

## Related Tools

- [Feature Engineering](../tools/feature-engineering.md) — general categorical encoding guidance this page adds a model-family nuance to
