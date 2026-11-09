"""
pipeline/load.py
Write transformed shipment data to a SQLite database (stdlib sqlite3).

Objects created:
  - shipments           : full cleaned record (indexed on common filter columns)
  - shipment_metrics    : pre-aggregated KPIs for fast dashboard queries
  - dq_log              : one row per pipeline run with data-quality counts (appended)
  - v_carrier_scorecard : view — on-time %, avg delay, volume per carrier
  - v_lane_performance  : view — region-to-region lane KPIs
"""

import json
import os
import sqlite3
from datetime import datetime, timezone

import pandas as pd

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "..", "data", "freight.db")

INDEXES = {
    "ix_ship_date":     "shipments(ship_date)",
    "ix_carrier":       "shipments(carrier_id)",
    "ix_lane":          "shipments(origin_region, destination_region)",
    "ix_freight_type":  "shipments(freight_type)",
}

VIEWS = {
    "v_carrier_scorecard": """
        SELECT carrier_id,
               COUNT(*)                                   AS shipments,
               ROUND(100.0 * AVG(on_time), 1)             AS on_time_pct,
               ROUND(AVG(CASE WHEN is_delayed = 1 THEN delay_days END), 2) AS avg_delay_when_late,
               ROUND(SUM(weight_kg) / 1000.0, 1)          AS tonnes_moved
        FROM shipments
        GROUP BY carrier_id
    """,
    "v_lane_performance": """
        SELECT origin_region, destination_region,
               COUNT(*)                        AS shipments,
               ROUND(100.0 * AVG(on_time), 1)  AS on_time_pct,
               ROUND(AVG(distance_km), 0)      AS avg_distance_km
        FROM shipments
        GROUP BY origin_region, destination_region
    """,
}


def load(df: pd.DataFrame, dq_report: dict | None = None, db_path: str | None = None) -> str:
    db_path = os.path.abspath(db_path or DEFAULT_DB)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    df_store = df.copy()
    for col in ["ship_date", "scheduled_delivery", "actual_delivery"]:
        if pd.api.types.is_datetime64_any_dtype(df_store[col]):
            df_store[col] = df_store[col].dt.strftime("%Y-%m-%d")
    for col in df_store.select_dtypes(include="category").columns:
        df_store[col] = df_store[col].astype(str)

    metrics = (
        df.groupby(["ship_year", "ship_month", "freight_type", "origin_region"])
        .agg(
            total_shipments=("shipment_id", "count"),
            on_time_count=("on_time", "sum"),
            avg_delay_days=("delay_days", "mean"),
            avg_distance_km=("distance_km", "mean"),
            total_weight_kg=("weight_kg", "sum"),
        )
        .reset_index()
    )
    metrics["on_time_pct"] = (metrics["on_time_count"] / metrics["total_shipments"] * 100).round(1)

    # One transaction: either the whole load lands or none of it does
    with sqlite3.connect(db_path) as conn:
        df_store.to_sql("shipments", conn, if_exists="replace", index=False)
        metrics.to_sql("shipment_metrics", conn, if_exists="replace", index=False)

        for name, target in INDEXES.items():
            conn.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {target}")
        for name, sql in VIEWS.items():
            conn.execute(f"DROP VIEW IF EXISTS {name}")
            conn.execute(f"CREATE VIEW {name} AS {sql}")

        if dq_report is not None:
            conn.execute("""CREATE TABLE IF NOT EXISTS dq_log (
                                run_at TEXT, rows_in INT, rows_out INT,
                                duplicates_removed INT, rows_rejected INT, details TEXT)""")
            conn.execute(
                "INSERT INTO dq_log VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 dq_report["rows_in"], dq_report["rows_out"],
                 dq_report["duplicates_removed"], dq_report["rows_rejected"],
                 json.dumps(dq_report)),
            )

        count = conn.execute("SELECT COUNT(*) FROM shipments").fetchone()[0]
    conn.close()

    print(f"[load] shipments: {count:,} rows | shipment_metrics: {len(metrics):,} rows")
    print(f"[load] indexes + views ({', '.join(VIEWS)}) created -> {db_path}")
    return db_path
