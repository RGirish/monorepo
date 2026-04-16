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
