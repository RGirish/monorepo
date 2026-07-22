# Backlog

## AI Learning Ideas

- Prompt engineering best practices
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- Open Knowledge Format for data sharing
  - https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing

## Build Ideas

- [Feature Engineering] Categorical encoding comparator — implement and benchmark one-hot, ordinal, target, frequency, and binary encoding across datasets
- [Feature Engineering] Time series feature extractor — auto-generate lag features, rolling statistics, Fourier transforms, and calendar features from raw data
- [Feature Engineering] Automated feature generator — given a DataFrame, generate candidate features and rank by mutual information or correlation with target
- [Feature Engineering] Feature selection benchmark — implement and compare filter, wrapper, and embedded selection methods
- [Feature Engineering] Leakage detector — flag features that suspiciously correlate with the target via temporal train/test split simulation
- [Feature Engineering] Entity embedding explorer — train neural embeddings for high-cardinality categoricals and visualize with UMAP vs one-hot baseline
- [Feature Engineering] Mini feature store — lightweight feature store with versioning, point-in-time correctness, and cross-experiment reuse
- [ML Models] Build a supervised learning model
- [ML Models] Build an unsupervised learning model
- [ML Models] Build an RL model
- [Networking/Crypto] Signal Protocol chat app (Part 2, Week 17): add pre-key replenishment (the one-time pre-key is currently never rotated once consumed) and push notifications (messages currently only arrive while the app is open, via a live Firestore listener)
- [Networking/Crypto] Signal Protocol chat app (Part 2, Week 17): add a real safety-number-style identity verification screen — compare a fingerprint of both sides' identity keys once, and surface a warning if either side's identity key ever changes after that (libsignal's `saveIdentity()` already detects this via `IdentityChange.REPLACED_EXISTING`, but nothing in the UI surfaces it yet)

