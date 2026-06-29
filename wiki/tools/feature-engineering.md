# Feature Engineering

**Covered in:** [Week 13](../weeks/week-13-2026-03-30.md)

---

## What It Is

Feature engineering is the process of taking raw data, identifying the information most relevant to a prediction task, and converting it into a representation that machine learning models can work with effectively. The goal is to bridge the gap between raw inputs and the patterns a model needs to learn.

## Core Idea

Raw data rarely comes in a form models can directly exploit. Feature engineering involves:
- Understanding what aspects of the data carry signal for the target
- Transforming those aspects into numeric representations (e.g., one-hot encoding, normalization, log transforms)
- A trial-and-error process: engineer a feature, measure lift, iterate

Feature types vary by data modality — tabular, text, audio, images, and video each require different engineering approaches.

## Classical Techniques

A practical toolkit for structured/tabular data:

### Encoding categoricals
Raw category labels can't be used directly — models need numbers. Two main approaches:
- **One-hot encoding** — create a binary column per category (`is_google`, `is_amazon`). No ordering implied. Each category gets its own weight in the model. Best default for nominal categories.
- **Ordinal encoding** (numbers: Google=1, Amazon=2) — implies a magnitude and ordering that usually doesn't exist. Only appropriate when the category genuinely has a natural order (e.g., low/medium/high).
- **Target encoding** — replace the category with the average target value for that category (e.g., average default rate per employer). Compact, but risks target leakage if done on the full training set without care.

### Scaling
Models sensitive to feature magnitude (linear models, SVMs, neural nets) are thrown off when one feature ranges 0–1 and another ranges 0–1,000,000. Two fixes:
- **Min-max scaling** — squash to [0, 1]: `(x - min) / (max - min)`
- **Z-score normalization** — center at mean=0, std=1: `(x - mean) / std`

Tree-based models (XGBoost, random forest) are not sensitive to scale — scaling doesn't matter for them.

### Log transforms
Apply when data spans multiple orders of magnitude (income, city population, web traffic) or when proportional differences matter more than absolute ones. `log(salary)` compresses the high tail, making right-skewed distributions more symmetric and turning multiplicative/proportional relationships into additive ones that linear models can fit. A doubling of salary looks the same everywhere on a log scale; on a raw scale, doubling $30k (+$30k) and doubling $500k (+$500k) look completely different.

### Binning / bucketing
Group continuous values into discrete ranges (age → decades: 20s, 30s, 40s). Trades precision for generalization — prevents the model from learning spurious patterns from noisy fine-grained differences. Useful when you expect the relationship to be step-wise rather than continuous.

### Derived quantities and interaction features
Compute new columns that don't exist in the raw data but carry more signal:
- `loan_amount / salary` → debt-to-income ratio (more meaningful than either column alone)
- `days_since_last_purchase` → derived from a raw timestamp
- `age_at_application` → derived from birthdate and loan date

These require domain expertise — the model cannot discover a debt-to-income ratio on its own without seeing many examples where the ratio matters.

### Decomposition
Break compound values into parts. A raw `birthdate` field can become `age`, `years_to_retirement`, or `decade_born`. A `timestamp` can become `hour_of_day`, `day_of_week`, `is_weekend`. Decomposition lets the model find patterns in the components independently.

---

## Feature Engineering vs. Representation Learning

Modern deep learning automates much of feature engineering through **representation learning** (also called feature learning): instead of human experts manually designing extraction rules, deep neural networks learn to discover the most relevant patterns directly from raw data during training. This is a core reason deep learning displaced hand-engineered pipelines in image and audio tasks.

### How Feature Learning Works in Deep Networks

Deep neural networks (with many hidden layers) extract features hierarchically:
- Each layer progressively extracts richer, more abstract representations of the input
- Early layers capture low-level patterns; deeper layers capture high-level concepts
- Feature richness compounds: layer 1 < layer 10 < layer 50, and so on

This hierarchy is only possible with large enough datasets. Given sufficient data, a deep network can automatically learn *which* features matter — removing the need to know in advance what to extract. This scales far better than hand-engineering, especially as dataset diversity grows and model generalization requirements increase.

## Feature Engineering in the LLM/GenAI Era

Feature engineering hasn't disappeared — it has shifted form:

- **Numerical & Tabular Translation**: Converting raw numbers into text-based relationships (e.g., percentiles) helps LLMs reason about data more accurately
- **Context Engineering (RAG)**: Deciding how to chunk data and tag metadata is feature engineering for retrieval — it determines what the model sees and how relevant it is
- **Prompt Precision**: Strategically constructed prompts reduce ambiguity — analogous to hand-crafting features that help older models "see" patterns
- **Hybrid Systems**: Traditional feature-heavy models (XGBoost, etc.) still run alongside GenAI for speed and regulatory transparency
- **LLMs as Feature Engineers**: LLMs are increasingly used to brainstorm and automate the creation of new features for other models

## Key Components of a Feature Engineering Platform

- Central feature store — shared, versioned feature definitions
- Data visualization — inspecting distributions, correlations, and feature importance
- Python SDK — programmatic feature creation and retrieval

## Related Tools

- [Language Modeling](language-modeling.md) — representation learning is the deep learning approach to automating feature engineering; one-hot encoding of characters is a classic feature engineering technique used in the makemore bigram model
- [LLM Wiki](llm-wiki.md) — LLMs both consume engineered features and act as feature engineering tools themselves

## Related Concepts

- [Language Modeling Fundamentals](../concepts/language-modeling-fundamentals.md) — one-hot encoding applied in the bigram model is a concrete example of feature engineering in practice
