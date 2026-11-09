"""
pipeline/extract.py
Load raw shipment CSV into a DataFrame.
"""

import pandas as pd
import os


def extract(csv_path: str | None = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "raw", "shipments.csv"
        )
    csv_path = os.path.abspath(csv_path)
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Raw data not found at {csv_path}.\n"
            "Run:  python data/generate_data.py"
        )
    df = pd.read_csv(csv_path, parse_dates=["ship_date", "scheduled_delivery", "actual_delivery"])
    print(f"[extract] Loaded {len(df):,} rows from {csv_path}")
    return df
