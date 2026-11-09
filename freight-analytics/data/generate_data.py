"""
generate_data.py
Generates a realistic synthetic Canadian freight shipment dataset.

Delays are driven by a logistic risk model (weather, season, distance,
cross-border customs, carrier reliability, service type, day of week), so
there is real, learnable signal plus irreducible noise, like real ops data.

A small share of "dirty" records (duplicates, bad weights, missing weather,
inconsistent casing/whitespace) is injected on purpose so the ETL
cleaning step has real work to do.

Run once: python data/generate_data.py [--n 5000]
Output:   data/raw/shipments.csv
"""

import argparse
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

SEED = 42

# ── Geography ────────────────────────────────────────────────────────────────
CITIES = {
    "Fredericton, NB":   (45.96, -66.64),
    "Moncton, NB":       (46.09, -64.80),
    "Saint John, NB":    (45.27, -66.06),
    "Edmundston, NB":    (47.37, -68.32),
    "Miramichi, NB":     (47.02, -65.50),
    "Halifax, NS":       (44.65, -63.57),
    "Truro, NS":         (45.36, -63.27),
    "Sydney, NS":        (46.14, -60.19),
    "Charlottetown, PE": (46.24, -63.13),
    "Quebec City, QC":   (46.81, -71.21),
    "Montreal, QC":      (45.50, -73.57),
    "Ottawa, ON":        (45.42, -75.69),
    "Toronto, ON":       (43.65, -79.38),
    "Kingston, ON":      (44.23, -76.49),
    "Sudbury, ON":       (46.49, -80.99),
    "Winnipeg, MB":      (49.90, -97.14),
    "Calgary, AB":       (51.05, -114.07),
    "Edmonton, AB":      (53.55, -113.49),
    "Vancouver, BC":     (49.28, -123.12),
    "Bangor, ME":        (44.80, -68.78),   # US cross-border
    "Portland, ME":      (43.66, -70.26),
    "Boston, MA":        (42.36, -71.06),
}
CITY_NAMES = list(CITIES.keys())
US_CITIES = {"Bangor, ME", "Portland, ME", "Boston, MA"}

# Atlantic-heavy network: origins/destinations weighted toward Maritime hubs
CITY_WEIGHTS = np.array([
    6, 7, 5, 2, 2, 7, 2, 1, 2,   # Atlantic
    3, 6,                        # Quebec
    3, 7, 2, 1,                  # Ontario
    2, 2, 2, 2,                  # West
    1, 1, 2,                     # US
], dtype=float)
CITY_WEIGHTS /= CITY_WEIGHTS.sum()

FREIGHT_TYPES = ["LTL", "Truckload", "Residential", "Dedicated"]
FREIGHT_MIX = [0.40, 0.35, 0.15, 0.10]
FREIGHT_WEIGHTS = {
    "LTL":         (200,  5000),
    "Truckload":   (5000, 40000),
    "Residential": (10,   500),
    "Dedicated":   (1000, 25000),
}

WEATHER = ["Clear", "Rain", "Snow", "Fog", "Ice"]
# Weather probabilities by season (winter vs rest of year)
WEATHER_PROBS_WINTER = [0.38, 0.10, 0.34, 0.06, 0.12]
WEATHER_PROBS_OTHER  = [0.60, 0.25, 0.04, 0.10, 0.01]

CARRIERS = [f"CR-{str(i).zfill(3)}" for i in range(1, 16)]

# ── Risk model coefficients (log-odds of a delay) ────────────────────────────
BASE_LOGIT = -1.55
WEATHER_EFFECT = {"Clear": 0.0, "Rain": 0.35, "Fog": 0.55, "Snow": 0.95, "Ice": 1.40}
FREIGHT_EFFECT = {"LTL": 0.15, "Truckload": -0.10, "Residential": 0.45, "Dedicated": -0.45}


def carrier_reliability(seed: int = SEED) -> dict:
    """Fixed per-carrier log-odds offset. A few carriers are clearly worse."""
    rng = np.random.default_rng(seed + 1)
    offsets = rng.normal(0, 0.35, len(CARRIERS))
    offsets[[3, 9]] += 0.9    # two chronic under-performers
    offsets[[0, 6]] -= 0.6    # two top performers
    return dict(zip(CARRIERS, offsets.round(3)))


# ── Helpers ───────────────────────────────────────────────────────────────────
def haversine_km(c1, c2):
    """Great-circle distance between two (lat, lon) points in km."""
    lat1, lon1 = np.radians(c1)
    lat2, lon2 = np.radians(c2)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    return float(6371 * 2 * np.arcsin(np.sqrt(a)))


def scheduled_days(distance_km, freight_type):
    """Expected transit days based on distance and service type."""
    base = max(1, round(distance_km / 700))
    if freight_type == "Residential":
        base += 1
    return base


def delay_logit(distance_km, freight_type, weather, weight_kg, month, dow,
                cross_border, carrier_offset):
    winter = month in (12, 1, 2)
    z = BASE_LOGIT
    z += WEATHER_EFFECT[weather]
    z += 0.45 if winter else 0.0
    z += 0.35 if winter and weather in ("Snow", "Ice") else 0.0
    z += 0.30 * (distance_km / 1000)
    z += 0.55 if cross_border else 0.0          # customs / border dwell
    z += 0.25 if weight_kg > 20000 else 0.0
    z += 0.30 if dow == 4 else 0.0              # Friday pickups roll over weekend
    z += 0.20 if month in (11, 12) else 0.0     # peak-season volume
    z += FREIGHT_EFFECT[freight_type]
    z += carrier_offset
    return z


# ── Generate records ──────────────────────────────────────────────────────────
def generate(n: int = 5000, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    carrier_fx = carrier_reliability(seed)

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 10, 31)
    date_range = (end_date - start_date).days

    records = []
    for i in range(n):
        o, d = rng.choice(len(CITY_NAMES), size=2, replace=False, p=CITY_WEIGHTS)
        origin, dest = CITY_NAMES[o], CITY_NAMES[d]
        freight_type = rng.choice(FREIGHT_TYPES, p=FREIGHT_MIX)
        lo, hi = FREIGHT_WEIGHTS[freight_type]
        weight_kg = round(float(rng.uniform(lo, hi)), 1)
        carrier_id = rng.choice(CARRIERS)

        ship_date = start_date + timedelta(days=int(rng.integers(0, date_range + 1)))
        month, dow = ship_date.month, ship_date.weekday()
        winter = month in (12, 1, 2)
        weather = rng.choice(WEATHER, p=WEATHER_PROBS_WINTER if winter else WEATHER_PROBS_OTHER)

        distance = round(haversine_km(CITIES[origin], CITIES[dest]), 1)
        cross_border = origin in US_CITIES or dest in US_CITIES
        sched = scheduled_days(distance, freight_type)

        z = delay_logit(distance, freight_type, weather, weight_kg, month, dow,
                        cross_border, carrier_fx[carrier_id])
        p_delay = 1 / (1 + np.exp(-z))
        if rng.random() < p_delay:
            scale = 1.2 + 0.6 * (weather in ("Snow", "Ice")) + 0.3 * (distance > 2000)
            delay = max(1, int(round(rng.exponential(scale))))
        else:
            delay = 0

        sched_delivery = ship_date + timedelta(days=sched)
        actual_delivery = sched_delivery + timedelta(days=delay)

        records.append({
            "shipment_id":        f"SHP-{str(i + 1).zfill(5)}",
            "ship_date":          ship_date.strftime("%Y-%m-%d"),
            "origin_city":        origin,
            "destination_city":   dest,
            "distance_km":        distance,
            "freight_type":       freight_type,
            "weight_kg":          weight_kg,
            "carrier_id":         carrier_id,
            "weather_condition":  weather,
            "scheduled_days":     sched,
            "scheduled_delivery": sched_delivery.strftime("%Y-%m-%d"),
            "actual_delivery":    actual_delivery.strftime("%Y-%m-%d"),
            "delay_days":         delay,
            "is_delayed":         int(delay > 0),
        })

    return pd.DataFrame(records)


def inject_dirty_records(df: pd.DataFrame, seed: int = SEED, rate: float = 0.02) -> pd.DataFrame:
    """Simulate typical source-system data quality problems."""
    rng = np.random.default_rng(seed + 2)
    df = df.copy()
    k = max(1, int(len(df) * rate / 4))

    # 1. Missing weather (sensor / EDI gaps)
    idx = rng.choice(df.index, k, replace=False)
    df.loc[idx, "weather_condition"] = np.nan
    # 2. Invalid weights (zero / negative keying errors)
    idx = rng.choice(df.index, k, replace=False)
    df.loc[idx, "weight_kg"] = rng.choice([0, -1, -250.0], k)
    # 3. Inconsistent casing / whitespace
    idx = rng.choice(df.index, k, replace=False)
    df.loc[idx, "freight_type"] = df.loc[idx, "freight_type"].str.lower() + " "
    df.loc[idx, "origin_city"] = "  " + df.loc[idx, "origin_city"]
    # 4. Duplicate records (re-sent EDI messages)
    dupes = df.loc[rng.choice(df.index, k, replace=False)]
    df = pd.concat([df, dupes]).sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=5000)
    args = parser.parse_args()

    out_dir = os.path.join(os.path.dirname(__file__), "raw")
    os.makedirs(out_dir, exist_ok=True)
    df = inject_dirty_records(generate(args.n))
    out_path = os.path.join(out_dir, "shipments.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df):,} records (incl. injected dirty rows) -> {out_path}")
    print(f"On-time rate: {(df['is_delayed'] == 0).mean():.1%}")
    print(f"Avg delay (delayed only): {df[df['delay_days'] > 0]['delay_days'].mean():.1f} days")
