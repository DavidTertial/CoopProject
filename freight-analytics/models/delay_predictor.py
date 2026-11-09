"""
models/delay_predictor.py
Shipment delay classifier.

- Preprocessing + model live in ONE sklearn Pipeline (one-hot encoding with
  handle_unknown="ignore"), so training and inference can't drift apart.
- Time-based split: train on older shipments, test on the most recent months
  (how the model would actually be used — predicting the future).
- Candidate models are compared against a majority-class baseline using
  ROC-AUC; the best one is saved along with a metrics JSON for the dashboard.

Usage:
    from models.delay_predictor import train, load_model, predict
    model, metrics = train(df)
    result = predict(model, {...})
"""

import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

MODEL_DIR    = os.path.dirname(__file__)
MODEL_PATH   = os.path.join(MODEL_DIR, "delay_model.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")

CATEGORICAL_FEATURES = ["freight_type", "weather_condition", "origin_region",
                        "destination_region", "carrier_id"]
NUMERIC_FEATURES     = ["distance_km", "weight_kg", "scheduled_days", "ship_month",
                        "ship_dow", "is_winter", "is_cross_border"]
ALL_FEATURES         = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET               = "is_delayed"
TEST_START           = "2025-11-01"   # hold out the last 12 months (full seasonal cycle)


def _preprocessor(scale_numeric: bool) -> ColumnTransformer:
    num = StandardScaler() if scale_numeric else "passthrough"
    return ColumnTransformer([
        ("num", num, NUMERIC_FEATURES),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])


def candidate_models() -> dict[str, Pipeline]:
    return {
        "Baseline (majority class)": Pipeline([
            ("prep", _preprocessor(False)),
            ("clf", DummyClassifier(strategy="most_frequent")),
        ]),
        "Logistic Regression": Pipeline([
            ("prep", _preprocessor(True)),
            ("clf", LogisticRegression(max_iter=2000, class_weight="balanced")),
        ]),
        "Random Forest": Pipeline([
            ("prep", _preprocessor(False)),
            ("clf", RandomForestClassifier(
                n_estimators=300, max_depth=8, min_samples_leaf=20,
                class_weight="balanced", random_state=42, n_jobs=-1)),
        ]),
    }


def time_split(df: pd.DataFrame, test_start: str = TEST_START):
    dates = pd.to_datetime(df["ship_date"])
    train_mask = dates < pd.Timestamp(test_start)
    return df[train_mask], df[~train_mask]


def _score(y_true, prob, threshold=0.5) -> dict:
    pred = (prob >= threshold).astype(int)
    auc = roc_auc_score(y_true, prob) if len(np.unique(prob)) > 1 else 0.5
    return {
        "roc_auc":   round(float(auc), 4),
        "accuracy":  round(float(accuracy_score(y_true, pred)), 4),
        "precision": round(float(precision_score(y_true, pred, zero_division=0)), 4),
        "recall":    round(float(recall_score(y_true, pred, zero_division=0)), 4),
        "f1":        round(float(f1_score(y_true, pred, zero_division=0)), 4),
    }


def train(df: pd.DataFrame, save: bool = True) -> tuple[Pipeline, dict]:
    """Fit candidates, pick best by test ROC-AUC, save it. Returns (model, metrics)."""
    data = df[ALL_FEATURES + [TARGET, "ship_date"]].dropna()
    train_df, test_df = time_split(data)
    X_train, y_train = train_df[ALL_FEATURES], train_df[TARGET]
    X_test,  y_test  = test_df[ALL_FEATURES],  test_df[TARGET]
    print(f"[model] Train {len(X_train):,} rows (< {TEST_START}) | Test {len(X_test):,} rows")

    results, fitted = {}, {}
    for name, pipe in candidate_models().items():
        pipe.fit(X_train, y_train)
        prob = pipe.predict_proba(X_test)[:, 1]
        results[name] = _score(y_test, prob)
        fitted[name] = pipe
        r = results[name]
        print(f"[model] {name:<26} AUC {r['roc_auc']:.3f} | acc {r['accuracy']:.1%} "
              f"| prec {r['precision']:.1%} | recall {r['recall']:.1%}")

    best_name = max((n for n in results if not n.startswith("Baseline")),
                    key=lambda n: results[n]["roc_auc"])
    best = fitted[best_name]

    # Permutation importance on held-out data (unbiased, works on raw columns)
    perm = permutation_importance(best, X_test, y_test, scoring="roc_auc",
                                  n_repeats=10, random_state=42, n_jobs=-1)
    importance = (pd.DataFrame({"feature": ALL_FEATURES,
                                "importance": perm.importances_mean.round(4)})
                  .sort_values("importance", ascending=False))
    print(f"[model] Selected: {best_name}")
    print(f"[model] Top drivers (permutation, AUC drop):\n"
          f"{importance.head(6).to_string(index=False)}")

    metrics = {
        "selected_model":    best_name,
        "test_start":        TEST_START,
        "train_rows":        int(len(X_train)),
        "test_rows":         int(len(X_test)),
        "test_delay_rate":   round(float(y_test.mean()), 4),
        "results":           results,
        "feature_importance": importance.to_dict(orient="records"),
    }

    if save:
        # Refit selected model on ALL data for deployment
        final = candidate_models()[best_name].fit(data[ALL_FEATURES], data[TARGET])
        joblib.dump(final, MODEL_PATH)
        with open(METRICS_PATH, "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"[model] Saved -> {MODEL_PATH}")
        best = final

    return best, metrics


def load_model() -> Pipeline:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Run: python run_pipeline.py")
    return joblib.load(MODEL_PATH)


def load_metrics() -> dict | None:
    if not os.path.exists(METRICS_PATH):
        return None
    with open(METRICS_PATH) as f:
        return json.load(f)


def predict(model: Pipeline, input_dict: dict) -> dict:
    """Predict delay probability for a single shipment (keys = ALL_FEATURES)."""
    X = pd.DataFrame([input_dict])[ALL_FEATURES]
    prob = float(model.predict_proba(X)[0, 1])
    return {
        "delayed_probability": round(prob, 3),
        "prediction":          "Delayed" if prob >= 0.5 else "On Time",
        "risk_level":          "High" if prob >= 0.65 else "Medium" if prob >= 0.40 else "Low",
    }
