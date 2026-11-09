# Freight Analytics Platform

![tests](https://github.com/DavidTertial/CoopProject/actions/workflows/freight-analytics.yml/badge.svg)

An end-to-end data engineering + analytics project modelled on the work of a transportation & logistics IT Data & Analytics team: raw shipment feed → cleaned, validated warehouse → SQL analytics → ML delay risk → interactive BI dashboard.

> All data is synthetic. Built as a portfolio project for data & analytics co-op roles in transportation/logistics.

---

## Highlights

| Layer | What it does |
|---|---|
| **Data generation** | ~5,000 Canadian/US-Northeast shipments across 22 cities. Delays come from a logistic risk model (weather × season, distance, customs, carrier reliability, service type, Friday pickups) — real signal plus noise. ~2% dirty records (duplicates, invalid weights, missing weather, bad casing) are injected on purpose. |
| **ETL + data quality** | Standardises text, de-duplicates re-sent records, applies 7 validation rules, recomputes the delay label from dates, engineers features. Every run writes a reconciled DQ report (`rows_in = rows_out + duplicates + rejected`) to a `dq_log` table. |
| **Warehouse (SQLite)** | `shipments` fact table with indexes, pre-aggregated `shipment_metrics`, and `v_carrier_scorecard` / `v_lane_performance` views. Loaded in a single transaction. |
| **SQL analytics** | 7 analysis queries using CTEs and window functions (rolling averages, `RANK`, `ROW_NUMBER`, `LAG`) — `sql/analysis_queries.sql`. |
| **ML delay model** | sklearn `Pipeline` (one-hot + model, so train/serve can't drift). **Time-based split** (train before Nov 2025, test on the following 12 months). Logistic Regression vs Random Forest vs majority-class baseline, chosen by ROC-AUC. Drivers explained with permutation importance. |
| **BI dashboard** | Plotly Dash: KPI cards, monthly trend, freight-type and weather breakdowns, top lanes, **carrier scorecard vs network average**, model performance card, and a live delay-risk predictor (pick cities + carrier → distance and risk computed). |
| **Tests / CI** | 10 pytest tests (data quality, load reconciliation, every SQL query, model beats baseline, unseen categories) run on GitHub Actions. |

## Results (hold-out year, 1,766 shipments)

| Model | ROC-AUC | Precision (delayed) | Recall (delayed) |
|---|---|---|---|
| Majority-class baseline | 0.500 | — | 0% |
| **Logistic Regression (selected)** | **0.715** | 55% | 64% |
| Random Forest | 0.695 | 54% | 67% |

Because the data is synthetic, the true delay probability for each shipment is known: an "oracle" using the exact generating formula scores **AUC 0.726** on the same test set — the model recovers ~98% of the achievable signal. The remaining error is irreducible noise, which is why accuracy alone (66% vs a 62% baseline) undersells it; ranking shipments by risk is what matters for dispatch.

**Top delay drivers:** carrier, weather, scheduled transit days, winter season, freight type.

**Sample findings (from `sql/run_queries.py`):**
- On-time drops from ~67% to ~47% in Dec–Feb; ice/snow in winter push delay rates to 66–76%.
- Carrier spread is ~45 points (best 77% on-time, worst 32%) — the biggest controllable lever.
- Cross-border (US) lanes run ~7 points below domestic.

---

## Project structure

```
freight-analytics/
├── data/generate_data.py      # Synthetic generator (risk model + dirty-record injection)
├── pipeline/
│   ├── extract.py             # Load raw CSV
│   ├── transform.py           # clean() → DQ report, add_features()
│   └── load.py                # SQLite: tables, indexes, views, dq_log
├── sql/
│   ├── analysis_queries.sql   # CTEs + window functions
│   └── run_queries.py         # Runner
├── models/delay_predictor.py  # Pipeline, time split, model comparison, permutation importance
├── dashboard/app.py           # Plotly Dash BI dashboard
├── tests/test_pipeline.py     # pytest suite
└── run_pipeline.py            # ETL + train
```

## Run it

```bash
pip install -r requirements.txt
python data/generate_data.py     # → data/raw/shipments.csv
python run_pipeline.py           # ETL + DQ + train → data/freight.db, models/
python sql/run_queries.py        # print SQL analyses
python dashboard/app.py          # → http://127.0.0.1:8050
python -m pytest -q              # tests
```

## Possible next steps

- Swap SQLite for PostgreSQL / Azure SQL and schedule the pipeline (Airflow / Azure Data Factory)
- Publish the warehouse to Power BI with the same KPIs
- Calibrate probabilities and pick the alert threshold from a cost of a missed delay vs a false alarm

---

David Ajaero · UNB Software Engineering (Co-op) · [github.com/DavidTertial](https://github.com/DavidTertial)
