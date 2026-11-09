"""
pipeline/transform.py
Clean the raw shipment data and engineer features for ML and BI.
"""

import pandas as pd
import numpy as np


# Region lookup — group cities into logical regions for BI
REGION_MAP = {
    "Fredericton, NB":   "Atlantic",
    "Moncton, NB":       "Atlantic",
    "Saint John, NB":    "Atlantic",
    "Edmundston, NB":    "Atlantic",
    "Miramichi, NB":     "Atlantic",
    "Halifax, NS":       "Atlantic",
    "Truro, NS":         "Atlantic",
    "Sydney, NS":        "Atlantic",
    "Charlottetown, PE": "Atlantic",
    "Quebec City, QC":   "Quebec",
    "Montreal, QC":      "Quebec",
    "Ottawa, ON":        "Ontario",
    "Toronto, ON":       "Ontario",
    "Kingston, ON":      "Ontario",
    "Sudbury, ON":       "Ontario",
    "Winnipeg, MB":      "Prairies",
    "Calgary, AB":       "Prairies",
    "Edmonton, AB":      "Prairies",
    "Vancouver, BC":     "West",
    "Bangor, ME":        "US Northeast",
    "Portland, ME":      "US Northeast",
    "Boston, MA":        "US Northeast",
}


VALID_FREIGHT = {"LTL", "Truckload", "Residential", "Dedicated"}
VALID_WEATHER = {"Clear", "Rain", "Snow", "Fog", "Ice"}
FREIGHT_CANON = {f.lower(): f for f in VALID_FREIGHT}


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Standardise, de-duplicate and validate raw records.

    Returns the clean frame plus a data-quality report (counts per rule)
    that is persisted to the `dq_log` table by the load step.
    """
    df = df.copy()
    report = {"rows_in": len(df)}

    # Standardise text fields
    for col in ["origin_city", "destination_city", "carrier_id", "weather_condition"]:
        df[col] = df[col].astype("string").str.strip()
    df["freight_type"] = (
        df["freight_type"].astype("string").str.strip().str.lower().map(FREIGHT_CANON)
    )

    # Duplicates (same shipment_id re-sent)
    dup_mask = df.duplicated(subset="shipment_id", keep="first")
    report["duplicates_removed"] = int(dup_mask.sum())
    df = df[~dup_mask]

    # Validation rules -> drop + count
    rules = {
        "missing_weather":       df["weather_condition"].isna(),
        "unknown_weather":       df["weather_condition"].notna() & ~df["weather_condition"].isin(VALID_WEATHER),
        "unknown_freight_type":  df["freight_type"].isna(),
        "invalid_weight":        ~(df["weight_kg"] > 0),
        "invalid_distance":      ~(df["distance_km"] > 0),
        "unknown_city":          ~df["origin_city"].isin(REGION_MAP) | ~df["destination_city"].isin(REGION_MAP),
        "delivery_before_ship":  df["actual_delivery"] < df["ship_date"],
    }
    bad = pd.Series(False, index=df.index)
    for name, mask in rules.items():
        report[name] = int((mask & ~bad).sum())   # attribute each row to first failing rule
        bad |= mask
    df = df[~bad]

    # Recompute delay from dates so the label can't drift from the source dates
    recomputed = (df["actual_delivery"] - df["scheduled_delivery"]).dt.days.clip(lower=0)
    report["delay_mismatch_fixed"] = int((recomputed != df["delay_days"]).sum())
    df["delay_days"] = recomputed.astype(int)
    df["is_delayed"] = (df["delay_days"] > 0).astype(int)

    for col in ["origin_city", "destination_city", "carrier_id", "weather_condition", "freight_type"]:
        df[col] = df[col].astype(str)

    report["rows_out"] = len(df)
    report["rows_rejected"] = report["rows_in"] - report["rows_out"] - report["duplicates_removed"]
    return df.reset_index(drop=True), report


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ── Date features ─────────────────────────────────────────────────────────
    df["ship_month"]      = df["ship_date"].dt.month
    df["ship_dow"]        = df["ship_date"].dt.dayofweek   # 0=Mon, 6=Sun
    df["ship_quarter"]    = df["ship_date"].dt.quarter
    df["ship_year"]       = df["ship_date"].dt.year
    df["is_weekend_ship"] = (df["ship_dow"] >= 5).astype(int)
    df["is_winter"]       = df["ship_month"].isin([12, 1, 2]).astype(int)

    # ── Buckets ───────────────────────────────────────────────────────────────
    df["distance_bucket"] = pd.cut(
        df["distance_km"],
        bins=[0, 300, 700, 1500, 3000, np.inf],
        labels=["Local (<300km)", "Regional (300-700km)", "Inter-regional (700-1500km)",
                "Long-haul (1500-3000km)", "Cross-country (>3000km)"],
    ).astype(str)
    df["weight_bucket"] = pd.cut(
        df["weight_kg"],
        bins=[0, 500, 5000, 20000, np.inf],
        labels=["Light (<500kg)", "Medium (500-5000kg)", "Heavy (5-20t)", "Very Heavy (>20t)"],
    ).astype(str)

    # ── Region / route ────────────────────────────────────────────────────────
    df["origin_region"]      = df["origin_city"].map(REGION_MAP)
    df["destination_region"] = df["destination_city"].map(REGION_MAP)
    df["is_cross_border"]    = (
        (df["origin_region"] == "US Northeast") | (df["destination_region"] == "US Northeast")
    ).astype(int)
    df["route"] = df["origin_city"] + " → " + df["destination_city"]

    df["on_time"] = (df["delay_days"] == 0).astype(int)
    return df


def transform(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df, report = clean(df)
    df = add_features(df)
    print(f"[transform] {report['rows_in']:,} in -> {report['rows_out']:,} clean "
          f"({report['duplicates_removed']} duplicates, {report['rows_rejected']} rejected)")
    print(f"[transform] On-time rate: {df['on_time'].mean():.1%}")
    return df, report
