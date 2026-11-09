"""
run_pipeline.py
Main entry point — runs the full ETL pipeline and trains the ML model.

Usage:
    python data/generate_data.py   # only needed once
    python run_pipeline.py         # ETL + train model
    python dashboard/app.py        # launch dashboard at http://127.0.0.1:8050
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.delay_predictor import train
from pipeline.extract import extract
from pipeline.load import load
from pipeline.transform import transform


def main():
    print("=" * 60)
    print("  Freight Analytics Pipeline")
    print("=" * 60)

    print("\n[1/4] Extracting raw data...")
    df_raw = extract()

    print("\n[2/4] Cleaning + transforming...")
    df_clean, dq_report = transform(df_raw)

    print("\n[3/4] Loading into database...")
    db_path = load(df_clean, dq_report)

    print("\n[4/4] Training delay prediction model...")
    _, metrics = train(df_clean)
    best = metrics["results"][metrics["selected_model"]]
    base = metrics["results"]["Baseline (majority class)"]

    print("\n" + "=" * 60)
    print("  Pipeline complete.")
    print(f"  Database : {db_path}")
    print(f"  Model    : {metrics['selected_model']}")
    print(f"  ROC-AUC  : {best['roc_auc']:.3f}  (baseline {base['roc_auc']:.3f})")
    print(f"  Recall   : {best['recall']:.1%} of delayed shipments flagged")
    print("=" * 60)
    print("\nTo launch the dashboard:  python dashboard/app.py  ->  http://127.0.0.1:8050\n")


if __name__ == "__main__":
    main()
