"""
dashboard/app.py
Plotly Dash BI dashboard for the Freight Analytics Pipeline.

Run:  python dashboard/app.py
Then open: http://127.0.0.1:8050
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

from models.delay_predictor import load_model, load_metrics, predict
from data.generate_data import CITIES, CARRIERS, haversine_km, scheduled_days
from pipeline.transform import REGION_MAP

# ── Load data ─────────────────────────────────────────────────────────────────
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "freight.db"))
if not os.path.exists(DB_PATH):
    raise FileNotFoundError("Database not found. Run: python run_pipeline.py")

conn = sqlite3.connect(DB_PATH)
df   = pd.read_sql("SELECT * FROM shipments", conn)
conn.close()
df["ship_date"] = pd.to_datetime(df["ship_date"])
model = load_model()
MODEL_METRICS = load_metrics()

FREIGHT_TYPES  = sorted(df["freight_type"].unique())
WEATHER_TYPES  = sorted(df["weather_condition"].unique())
REGIONS        = sorted(df["origin_region"].unique())

# ── Colour palette ─────────────────────────────────────────────────────────────
PALETTE = px.colors.qualitative.Set2
GREEN   = "#2ecc71"
RED     = "#e74c3c"
BLUE    = "#3498db"
DARK    = "#2c3e50"

# ── App ────────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Freight Analytics Platform",
)

# ── KPI card helper ────────────────────────────────────────────────────────────
def kpi_card(title, value, subtitle="", color=BLUE):
    return dbc.Card(
        dbc.CardBody([
            html.P(title, className="text-muted mb-1", style={"fontSize": "0.8rem", "fontWeight": 600}),
            html.H3(value, style={"color": color, "fontWeight": 700}),
            html.P(subtitle, className="text-muted mb-0", style={"fontSize": "0.75rem"}),
        ]),
        className="shadow-sm h-100",
    )


def model_card():
    """Hold-out metrics table + top drivers, read from models/model_metrics.json."""
    if not MODEL_METRICS:
        return html.P("Run python run_pipeline.py to train the model.", className="text-muted")
    m = MODEL_METRICS
    rows = [html.Tr([html.Th("Model"), html.Th("ROC-AUC"), html.Th("Precision"), html.Th("Recall")])]
    for name, r in m["results"].items():
        style = {"fontWeight": 700} if name == m["selected_model"] else {}
        rows.append(html.Tr([html.Td(name), html.Td(f"{r['roc_auc']:.3f}"),
                             html.Td(f"{r['precision']:.0%}"), html.Td(f"{r['recall']:.0%}")], style=style))
    top = pd.DataFrame(m["feature_importance"]).head(6).iloc[::-1]
    fig = px.bar(top, x="importance", y="feature", orientation="h",
                 labels={"importance": "AUC drop when shuffled", "feature": ""},
                 color_discrete_sequence=[BLUE])
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=30), height=170, plot_bgcolor="white")
    return html.Div([
        html.P(f"Trained on shipments before {m['test_start']}, tested on the {m['test_rows']:,} "
               f"after it (time-based split).", className="small text-muted mb-2"),
        dbc.Table(rows, size="sm", bordered=False, className="small mb-2"),
        html.P("Top delay drivers (permutation importance)", className="small fw-bold mb-0"),
        dcc.Graph(figure=fig, config={"displayModeBar": False}),
    ])


# ── Layout ─────────────────────────────────────────────────────────────────────
app.layout = dbc.Container([

    # Header
    dbc.Row(dbc.Col(html.Div([
        html.H2("Freight Analytics Platform", className="mb-0 fw-bold"),
        html.P("Transportation & Logistics Intelligence Dashboard", className="text-muted"),
    ]), className="py-3 border-bottom"), className="mb-4"),

    # Filters
    dbc.Row([
        dbc.Col([
            html.Label("Freight Type", className="fw-bold small"),
            dcc.Dropdown(
                id="filter-freight",
                options=[{"label": "All", "value": "All"}] +
                        [{"label": t, "value": t} for t in FREIGHT_TYPES],
                value="All", clearable=False,
            ),
        ], md=3),
        dbc.Col([
            html.Label("Year", className="fw-bold small"),
            dcc.Dropdown(
                id="filter-year",
                options=[{"label": "All", "value": "All"}] +
                        [{"label": str(y), "value": y} for y in sorted(df["ship_year"].unique())],
                value="All", clearable=False,
            ),
        ], md=3),
        dbc.Col([
            html.Label("Origin Region", className="fw-bold small"),
            dcc.Dropdown(
                id="filter-region",
                options=[{"label": "All", "value": "All"}] +
                        [{"label": r, "value": r} for r in REGIONS],
                value="All", clearable=False,
            ),
        ], md=3),
        dbc.Col([
            html.Label("Weather", className="fw-bold small"),
            dcc.Dropdown(
                id="filter-weather",
                options=[{"label": "All", "value": "All"}] +
                        [{"label": w, "value": w} for w in WEATHER_TYPES],
                value="All", clearable=False,
            ),
        ], md=3),
    ], className="mb-4"),

    # KPI row
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("Total Shipments", className="text-muted mb-1 small fw-bold"),
            html.H3(id="kpi-total", style={"color": BLUE, "fontWeight": 700}),
        ]), className="shadow-sm"), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("On-Time Rate", className="text-muted mb-1 small fw-bold"),
            html.H3(id="kpi-ontime", style={"color": GREEN, "fontWeight": 700}),
        ]), className="shadow-sm"), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("Avg Delay (delayed shipments)", className="text-muted mb-1 small fw-bold"),
            html.H3(id="kpi-delay", style={"color": RED, "fontWeight": 700}),
        ]), className="shadow-sm"), md=3),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("Avg Distance (km)", className="text-muted mb-1 small fw-bold"),
            html.H3(id="kpi-dist", style={"color": DARK, "fontWeight": 700}),
        ]), className="shadow-sm"), md=3),
    ], className="mb-4"),

    # Row 2 — trend + on-time by freight type
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Monthly Shipment Volume & On-Time Rate", className="fw-bold"),
            dbc.CardBody(dcc.Graph(id="chart-trend", style={"height": "300px"})),
        ], className="shadow-sm"), md=8),
        dbc.Col(dbc.Card([
            dbc.CardHeader("On-Time Rate by Freight Type", className="fw-bold"),
            dbc.CardBody(dcc.Graph(id="chart-freight", style={"height": "300px"})),
        ], className="shadow-sm"), md=4),
    ], className="mb-4"),

    # Row 3 — weather impact + top routes
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Delay Rate by Weather Condition", className="fw-bold"),
            dbc.CardBody(dcc.Graph(id="chart-weather", style={"height": "280px"})),
        ], className="shadow-sm"), md=5),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Top 10 Routes by Volume", className="fw-bold"),
            dbc.CardBody(dcc.Graph(id="chart-routes", style={"height": "280px"})),
        ], className="shadow-sm"), md=7),
    ], className="mb-4"),

    # Row 4 — carrier scorecard + model card
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Carrier Scorecard — On-Time % vs Network Average", className="fw-bold"),
            dbc.CardBody(dcc.Graph(id="chart-carriers", style={"height": "320px"})),
        ], className="shadow-sm"), md=7),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Delay Model — Hold-out Performance", className="fw-bold"),
            dbc.CardBody(model_card()),
        ], className="shadow-sm h-100"), md=5),
    ], className="mb-4"),

    # Row 5 — ML prediction widget
    dbc.Row(dbc.Col(dbc.Card([
        dbc.CardHeader(html.Span([
            html.I(className="me-2"),
            f"Shipment Delay Predictor  ({MODEL_METRICS['selected_model'] if MODEL_METRICS else 'ML model'})"
        ]), className="fw-bold"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Freight Type", className="small fw-bold"),
                    dcc.Dropdown(id="pred-freight", options=[{"label": t, "value": t} for t in FREIGHT_TYPES],
                                 value="LTL", clearable=False),
                ], md=3),
                dbc.Col([
                    html.Label("Weather", className="small fw-bold"),
                    dcc.Dropdown(id="pred-weather", options=[{"label": w, "value": w} for w in WEATHER_TYPES],
                                 value="Clear", clearable=False),
                ], md=3),
                dbc.Col([
                    html.Label("Carrier", className="small fw-bold"),
                    dcc.Dropdown(id="pred-carrier", options=[{"label": c, "value": c} for c in CARRIERS],
                                 value=CARRIERS[0], clearable=False),
                ], md=3),
                dbc.Col([
                    html.Label("Ship Day", className="small fw-bold"),
                    dcc.Dropdown(id="pred-dow", options=[{"label": d, "value": i} for i, d in
                                 enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])],
                                 value=1, clearable=False),
                ], md=3),
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label("Origin City", className="small fw-bold"),
                    dcc.Dropdown(id="pred-origin", options=[{"label": c, "value": c} for c in CITIES],
                                 value="Moncton, NB", clearable=False),
                ], md=4),
                dbc.Col([
                    html.Label("Destination City", className="small fw-bold"),
                    dcc.Dropdown(id="pred-dest", options=[{"label": c, "value": c} for c in CITIES],
                                 value="Toronto, ON", clearable=False),
                ], md=4),
                dbc.Col([
                    html.Label("Weight (kg)", className="small fw-bold"),
                    dcc.Slider(id="pred-weight", min=10, max=40000, step=100, value=5000,
                               marks={10: "10", 10000: "10k", 25000: "25k", 40000: "40k"},
                               tooltip={"always_visible": True}),
                ], md=2),
                dbc.Col([
                    html.Label("Shipping Month", className="small fw-bold"),
                    dcc.Slider(id="pred-month", min=1, max=12, step=1, value=6,
                               marks={1: "Jan", 3: "Mar", 6: "Jun", 9: "Sep", 12: "Dec"},
                               tooltip={"always_visible": True}),
                ], md=2),
            ], className="mb-3"),
            dbc.Row(dbc.Col(
                dbc.Button("Run Prediction", id="pred-btn", color="primary", className="w-100"),
                md=3,
            ), className="mb-3"),
            html.Div(id="pred-result"),
        ]),
    ], className="shadow-sm"))),

    html.Hr(className="mt-4"),
    html.P("Freight Analytics Platform  |  David Ajaero  |  UNB Software Engineering Co-op",
           className="text-center text-muted small pb-3"),

], fluid=True)


# ── Callbacks ──────────────────────────────────────────────────────────────────
def apply_filters(freight, year, region, weather):
    dff = df.copy()
    if freight != "All":
        dff = dff[dff["freight_type"] == freight]
    if year != "All":
        dff = dff[dff["ship_year"] == int(year)]
    if region != "All":
        dff = dff[dff["origin_region"] == region]
    if weather != "All":
        dff = dff[dff["weather_condition"] == weather]
    return dff


FILTER_INPUTS = [
    Input("filter-freight", "value"),
    Input("filter-year",    "value"),
    Input("filter-region",  "value"),
    Input("filter-weather", "value"),
]


@app.callback(
    Output("kpi-total",   "children"),
    Output("kpi-ontime",  "children"),
    Output("kpi-delay",   "children"),
    Output("kpi-dist",    "children"),
    *FILTER_INPUTS,
)
def update_kpis(freight, year, region, weather):
    dff = apply_filters(freight, year, region, weather)
    if len(dff) == 0:
        return "—", "—", "—", "—"
    total      = f"{len(dff):,}"
    on_time    = f"{dff['on_time'].mean():.1%}"
    avg_delay  = f"{dff[dff['delay_days'] > 0]['delay_days'].mean():.1f} days" if dff['is_delayed'].sum() > 0 else "0.0 days"
    avg_dist   = f"{dff['distance_km'].mean():,.0f} km"
    return total, on_time, avg_delay, avg_dist


@app.callback(Output("chart-trend", "figure"), *FILTER_INPUTS)
def update_trend(freight, year, region, weather):
    dff = apply_filters(freight, year, region, weather)
    monthly = (
        dff.groupby(dff["ship_date"].dt.to_period("M"))
        .agg(shipments=("shipment_id", "count"), on_time_pct=("on_time", "mean"))
        .reset_index()
    )
    monthly["ship_date"] = monthly["ship_date"].dt.to_timestamp()
    monthly["on_time_pct"] *= 100

    fig = go.Figure()
    fig.add_bar(x=monthly["ship_date"], y=monthly["shipments"],
                name="Shipments", marker_color=BLUE, opacity=0.7, yaxis="y1")
    fig.add_scatter(x=monthly["ship_date"], y=monthly["on_time_pct"],
                    name="On-Time %", line=dict(color=GREEN, width=2.5),
                    yaxis="y2", mode="lines+markers", marker_size=4)
    fig.update_layout(
        yaxis=dict(title="Shipments", side="left"),
        yaxis2=dict(title="On-Time %", side="right", overlaying="y", range=[0, 100]),
        legend=dict(orientation="h", y=1.1),
        margin=dict(l=40, r=40, t=10, b=30),
        hovermode="x unified",
        plot_bgcolor="white",
    )
    return fig


@app.callback(Output("chart-freight", "figure"), *FILTER_INPUTS)
def update_freight(freight, year, region, weather):
    dff = apply_filters(freight, year, region, weather)
    agg = dff.groupby("freight_type")["on_time"].mean().reset_index()
    agg["on_time_pct"] = (agg["on_time"] * 100).round(1)
    fig = px.bar(agg, x="freight_type", y="on_time_pct",
                 color="freight_type", color_discrete_sequence=PALETTE,
                 labels={"freight_type": "", "on_time_pct": "On-Time %"},
                 text="on_time_pct")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=10, b=20),
                      yaxis_range=[0, 110], plot_bgcolor="white")
    return fig


@app.callback(Output("chart-weather", "figure"), *FILTER_INPUTS)
def update_weather(freight, year, region, weather):
    dff = apply_filters(freight, year, region, weather)
    agg = dff.groupby("weather_condition")["is_delayed"].mean().reset_index()
    agg["delay_rate"] = (agg["is_delayed"] * 100).round(1)
    agg = agg.sort_values("delay_rate", ascending=True)
    fig = px.bar(agg, x="delay_rate", y="weather_condition", orientation="h",
                 color="delay_rate", color_continuous_scale=["#2ecc71", "#e74c3c"],
                 labels={"delay_rate": "Delay Rate (%)", "weather_condition": ""},
                 text="delay_rate")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(coloraxis_showscale=False, margin=dict(l=10, r=40, t=10, b=20),
                      plot_bgcolor="white")
    return fig


@app.callback(Output("chart-routes", "figure"), *FILTER_INPUTS)
def update_routes(freight, year, region, weather):
    dff = apply_filters(freight, year, region, weather)
    top = (
        dff.groupby("route")
        .agg(shipments=("shipment_id", "count"), on_time_pct=("on_time", "mean"))
        .reset_index()
        .nlargest(10, "shipments")
        .sort_values("shipments")
    )
    top["on_time_pct"] = (top["on_time_pct"] * 100).round(1)
    fig = px.bar(top, x="shipments", y="route", orientation="h",
                 color="on_time_pct",
                 color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
                 range_color=[60, 100],
                 labels={"shipments": "Shipments", "route": "", "on_time_pct": "On-Time %"},
                 text="shipments")
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(l=10, r=40, t=10, b=20), plot_bgcolor="white")
    return fig


@app.callback(Output("chart-carriers", "figure"), *FILTER_INPUTS)
def update_carriers(freight, year, region, weather):
    dff = apply_filters(freight, year, region, weather)
    if dff.empty:
        return go.Figure()
    network = dff["on_time"].mean() * 100
    agg = (dff.groupby("carrier_id")
           .agg(shipments=("shipment_id", "count"), on_time_pct=("on_time", "mean"))
           .reset_index())
    agg["on_time_pct"] = (agg["on_time_pct"] * 100).round(1)
    agg["vs_network"] = (agg["on_time_pct"] - network).round(1)
    agg = agg.sort_values("on_time_pct", ascending=False)
    fig = px.bar(agg, x="carrier_id", y="on_time_pct",
                 color=agg["vs_network"] >= 0,
                 color_discrete_map={True: GREEN, False: RED},
                 hover_data={"shipments": True, "vs_network": True},
                 labels={"carrier_id": "", "on_time_pct": "On-Time %", "vs_network": "pts vs network"})
    fig.add_hline(y=network, line_dash="dash", line_color=DARK,
                  annotation_text=f"Network {network:.1f}%", annotation_position="top right")
    fig.update_layout(showlegend=False, margin=dict(l=20, r=20, t=10, b=20),
                      yaxis_range=[0, 100], plot_bgcolor="white")
    return fig


@app.callback(
    Output("pred-result", "children"),
    Input("pred-btn", "n_clicks"),
    State("pred-freight", "value"),
    State("pred-weather", "value"),
    State("pred-carrier", "value"),
    State("pred-dow",     "value"),
    State("pred-origin",  "value"),
    State("pred-dest",    "value"),
    State("pred-weight",  "value"),
    State("pred-month",   "value"),
    prevent_initial_call=True,
)
def run_prediction(n, freight, weather, carrier, dow, origin, dest, weight, month):
    if origin == dest:
        return dbc.Alert("Origin and destination must be different.", color="warning", className="mb-0")
    distance = round(haversine_km(CITIES[origin], CITIES[dest]), 1)
    o_region, d_region = REGION_MAP[origin], REGION_MAP[dest]
    input_dict = {
        "freight_type":       freight,
        "weather_condition":  weather,
        "carrier_id":         carrier,
        "origin_region":      o_region,
        "destination_region": d_region,
        "distance_km":        distance,
        "weight_kg":          weight,
        "scheduled_days":     scheduled_days(distance, freight),
        "ship_month":         month,
        "ship_dow":           dow,
        "is_winter":          int(month in [12, 1, 2]),
        "is_cross_border":    int("US Northeast" in (o_region, d_region)),
    }
    result = predict(model, input_dict)
    colour = RED if result["prediction"] == "Delayed" else GREEN

    return dbc.Alert([
        dbc.Row([
            dbc.Col(html.H4(result["prediction"], style={"color": colour, "fontWeight": 700}), md=3),
            dbc.Col([
                html.P(f"Delay probability: {result['delayed_probability']:.1%}", className="mb-1"),
                html.P(f"Risk level: {result['risk_level']}", className="mb-0"),
            ], md=4),
            dbc.Col(html.P(
                f"{origin} → {dest}  |  {distance:,.0f} km  |  {freight}  |  {weight:,} kg  |  {weather}  |  {carrier}",
                className="text-muted small mb-0 mt-1",
            ), md=5),
        ]),
    ], color="danger" if result["prediction"] == "Delayed" else "success", className="mb-0")


if __name__ == "__main__":
    print("Dashboard running at http://127.0.0.1:8050")
    app.run(debug=True)
