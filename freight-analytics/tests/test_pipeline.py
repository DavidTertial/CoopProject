"""
Pipeline tests:  python -m pytest -q
Uses a small generated dataset and a temp SQLite DB — never touches data/freight.db.
"""

import os
import sqlite3
import sys

import pandas as pd
import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from data.generate_data import generate, inject_dirty_records          # noqa: E402
from models.delay_predictor import ALL_FEATURES, predict, train         # noqa: E402
from pipeline.load import load                                          # noqa: E402
from pipeline.transform import VALID_FREIGHT, VALID_WEATHER, transform  # noqa: E402
from sql.run_queries import load_queries                                # noqa: E402

DATE_COLS = ["ship_date", "scheduled_delivery", "actual_delivery"]


@pytest.fixture(scope="module")
def raw():
    df = inject_dirty_records(generate(n=2000, seed=7), seed=7)
    for c in DATE_COLS:
        df[c] = pd.to_datetime(df[c])
    return df


@pytest.fixture(scope="module")
def clean(raw):
    return transform(raw)


@pytest.fixture(scope="module")
def db(clean, tmp_path_factory):
    df, report = clean
    return load(df, report, db_path=str(tmp_path_factory.mktemp("db") / "test.db"))


# ── Generator ────────────────────────────────────────────────────────────────
def test_generator_is_deterministic():
    pd.testing.assert_frame_equal(generate(n=200, seed=1), generate(n=200, seed=1))


def test_generator_injects_dirty_rows(raw):
    assert raw["shipment_id"].duplicated().any()
    assert raw["weather_condition"].isna().any()
    assert (raw["weight_kg"] <= 0).any()


# ── Transform / data quality ─────────────────────────────────────────────────
def test_clean_output_is_valid(clean):
    df, _ = clean
    assert df["shipment_id"].is_unique
    assert (df["weight_kg"] > 0).all()
    assert set(df["freight_type"]) <= VALID_FREIGHT
    assert set(df["weather_condition"]) <= VALID_WEATHER
    assert df[["origin_region", "destination_region"]].notna().all().all()
    assert (df["origin_city"] == df["origin_city"].str.strip()).all()


def test_dq_report_reconciles(clean):
    df, r = clean
    assert r["rows_out"] == len(df)
    assert r["rows_in"] == r["rows_out"] + r["duplicates_removed"] + r["rows_rejected"]
    assert r["duplicates_removed"] > 0 and r["rows_rejected"] > 0


def test_label_matches_dates(clean):
    df, _ = clean
    expected = (df["actual_delivery"] - df["scheduled_delivery"]).dt.days.clip(lower=0)
    assert (df["delay_days"] == expected).all()
    assert (df["is_delayed"] == (df["delay_days"] > 0)).all()


# ── Load / SQL ───────────────────────────────────────────────────────────────
def test_load_creates_tables_and_views(db, clean):
    with sqlite3.connect(db) as conn:
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master")}
        assert {"shipments", "shipment_metrics", "dq_log",
                "v_carrier_scorecard", "v_lane_performance"} <= names
        assert conn.execute("SELECT COUNT(*) FROM shipments").fetchone()[0] == len(clean[0])


def test_metrics_table_totals_match(db, clean):
    with sqlite3.connect(db) as conn:
        total = conn.execute("SELECT SUM(total_shipments) FROM shipment_metrics").fetchone()[0]
    assert total == len(clean[0])


def test_all_analysis_queries_run(db):
    queries = load_queries()
    assert len(queries) >= 5
    with sqlite3.connect(db) as conn:
        for name, sql in queries:
            assert len(pd.read_sql(sql, conn)) > 0, name


# ── Model ────────────────────────────────────────────────────────────────────
def test_model_beats_baseline_and_predicts(clean):
    df, _ = clean
    model, m = train(df, save=False)
    best = m["results"][m["selected_model"]]
    assert best["roc_auc"] > m["results"]["Baseline (majority class)"]["roc_auc"] + 0.1

    sample = df.iloc[0][ALL_FEATURES].to_dict()
    out = predict(model, sample)
    assert 0 <= out["delayed_probability"] <= 1
    assert out["risk_level"] in {"Low", "Medium", "High"}


def test_model_handles_unseen_category(clean):
    df, _ = clean
    model, _ = train(df, save=False)
    sample = df.iloc[0][ALL_FEATURES].to_dict()
    sample["carrier_id"] = "CR-999"
    assert 0 <= predict(model, sample)["delayed_probability"] <= 1
