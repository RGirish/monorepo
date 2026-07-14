"""Feature engineering pipeline on the Bike Sharing Demand dataset.

Each stage adds engineered features on top of the previous stage and
re-measures RMSLE via cross-validation, so the effect of each feature
engineering decision is directly visible as a score delta.
"""
import os
import certifi

os.environ.setdefault("SSL_CERT_FILE", certifi.where())

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import make_scorer, mean_squared_log_error
from sklearn.model_selection import KFold, cross_val_score

RANDOM_STATE = 42


def load_data() -> pd.DataFrame:
    data = fetch_openml("Bike_Sharing_Demand", version=2, as_frame=True)
    df = data.frame.copy()
    # casual + registered sum to count exactly -> leakage if kept as features
    df = df.drop(columns=["casual", "registered"], errors="ignore")
    return df


def rmsle(y_true, y_pred):
    y_pred = np.clip(y_pred, 0, None)
    return np.sqrt(mean_squared_log_error(y_true, y_pred))


rmsle_scorer = make_scorer(rmsle, greater_is_better=False)


def evaluate(X: pd.DataFrame, y: pd.Series, label: str) -> float:
    model = GradientBoostingRegressor(random_state=RANDOM_STATE)
    cv = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(model, X, y, scoring=rmsle_scorer, cv=cv)
    score = -scores.mean()
    print(f"{label:40s} RMSLE = {score:.4f}")
    return score


def naive_encode_categories(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    for col in X.select_dtypes(include="category").columns:
        X[col] = X[col].cat.codes
    return X


def stage1_baseline(df: pd.DataFrame) -> float:
    """Minimal cleaning only: raw fields, naive category codes, no engineering."""
    X = naive_encode_categories(df.drop(columns=["count"]))
    y = df["count"]
    return evaluate(X, y, "Stage 1: baseline (raw fields)")


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # weekday 0 and 6 are the two days always workingday=False -> weekend
    df["is_weekend"] = df["weekday"].isin([0, 6]).astype(int)
    df["is_rush_hour"] = df["hour"].isin([7, 8, 9, 17, 18, 19]).astype(int)
    df["time_of_day"] = pd.cut(
        df["hour"],
        bins=[-1, 5, 11, 16, 23],
        labels=["night", "morning", "afternoon", "evening"],
    )
    # hour/month are cyclical (23 and 0 are adjacent) -> sin/cos preserves that, a raw int doesn't
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    return df.drop(columns=["hour", "month"])


def stage2_time_features(df: pd.DataFrame) -> float:
    """Stage 1 fields plus derived/cyclical time features."""
    X = naive_encode_categories(add_time_features(df.drop(columns=["count"])))
    y = df["count"]
    return evaluate(X, y, "Stage 2: + time-derived features")


def onehot_encode_categories(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    categorical_cols = X.select_dtypes(include="category").columns
    # a 2-category column (e.g. holiday True/False) has no false ordering to
    # introduce, so a single 0/1 code is already a correct encoding for it
    binary_cols = [c for c in categorical_cols if X[c].cat.categories.size == 2]
    nominal_cols = [c for c in categorical_cols if c not in binary_cols]
    for col in binary_cols:
        X[col] = X[col].cat.codes
    return pd.get_dummies(X, columns=nominal_cols)


def stage3_categorical_encoding(df: pd.DataFrame) -> float:
    """Stage 2 fields, but nominal categoricals (season/weather/time_of_day)
    are one-hot encoded instead of getting arbitrary integer codes."""
    X = onehot_encode_categories(add_time_features(df.drop(columns=["count"])))
    y = df["count"]
    return evaluate(X, y, "Stage 3: + proper categorical encoding")


if __name__ == "__main__":
    df = load_data()
    stage1_baseline(df)
    stage2_time_features(df)
    stage3_categorical_encoding(df)
