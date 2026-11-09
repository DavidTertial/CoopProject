-- analysis_queries.sql
-- Ad-hoc analytics against data/freight.db (SQLite 3.25+ for window functions).
-- Run all:  python sql/run_queries.py      Run one:  python sql/run_queries.py 3
-- Each query starts with a "-- name:" line so the runner can split them.

-- name: 1. Monthly on-time % with 3-month rolling average
WITH monthly AS (
    SELECT substr(ship_date, 1, 7)          AS month,
           COUNT(*)                         AS shipments,
           ROUND(100.0 * AVG(on_time), 1)   AS on_time_pct
    FROM shipments
    GROUP BY month
)
SELECT month, shipments, on_time_pct,
       ROUND(AVG(on_time_pct) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1)
           AS on_time_pct_3mo_avg
FROM monthly
ORDER BY month;

-- name: 2. Carrier ranking vs network average (min 100 shipments)
SELECT carrier_id, shipments, on_time_pct, avg_delay_when_late,
       RANK() OVER (ORDER BY on_time_pct DESC)                          AS rank,
       ROUND(on_time_pct - AVG(on_time_pct) OVER (), 1)                 AS pts_vs_network
FROM v_carrier_scorecard
WHERE shipments >= 100
ORDER BY rank;

-- name: 3. Worst lane per origin region (lanes with >= 30 shipments)
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY origin_region ORDER BY on_time_pct ASC) AS rn
    FROM v_lane_performance
    WHERE shipments >= 30
)
SELECT origin_region, destination_region, shipments, on_time_pct, avg_distance_km
FROM ranked
WHERE rn = 1
ORDER BY on_time_pct;

-- name: 4. Winter vs non-winter delay rate by weather
SELECT weather_condition,
       ROUND(100.0 * AVG(CASE WHEN is_winter = 1 THEN is_delayed END), 1) AS winter_delay_pct,
       ROUND(100.0 * AVG(CASE WHEN is_winter = 0 THEN is_delayed END), 1) AS other_delay_pct,
       SUM(is_winter)                                                     AS winter_shipments
FROM shipments
GROUP BY weather_condition
ORDER BY winter_delay_pct DESC;

-- name: 5. Cross-border vs domestic service level
SELECT CASE is_cross_border WHEN 1 THEN 'Cross-border (US)' ELSE 'Domestic' END AS segment,
       COUNT(*)                                                 AS shipments,
       ROUND(100.0 * AVG(on_time), 1)                           AS on_time_pct,
       ROUND(AVG(CASE WHEN is_delayed = 1 THEN delay_days END), 2) AS avg_delay_when_late
FROM shipments
GROUP BY segment;

-- name: 6. Year-over-year on-time change by freight type
WITH yearly AS (
    SELECT freight_type, ship_year, ROUND(100.0 * AVG(on_time), 1) AS on_time_pct
    FROM shipments
    GROUP BY freight_type, ship_year
)
SELECT freight_type, ship_year, on_time_pct,
       ROUND(on_time_pct - LAG(on_time_pct) OVER (PARTITION BY freight_type ORDER BY ship_year), 1)
           AS yoy_change_pts
FROM yearly
ORDER BY freight_type, ship_year;

-- name: 7. Data-quality history (latest pipeline runs)
SELECT run_at, rows_in, rows_out, duplicates_removed, rows_rejected
FROM dq_log
ORDER BY run_at DESC
LIMIT 5;
