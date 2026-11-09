import { EventEmitter } from "node:events";
import { ROUTES, findRoute } from "./routes.js";

// ---- tunables ----------------------------------------------------------
const TICK_MS = 2000;              // how often trucks move (ms)
const ANOMALY_CHANCE = 0.05;       // per-truck, per-tick chance of a new event
const OFF_ROUTE_KM = 1.5;          // jitter magnitude counted as "off route"
const LATE_FRACTION_THRESHOLD = 0.12; // how far behind schedule before "late"
const MAINTENANCE_TICKS = 6;       // how many ticks a breakdown lasts

// ---- geo helpers ---------------------------------------------------------
function haversineKm([lat1, lon1], [lat2, lon2]) {
  const R = 6371;
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

function buildCumulativeDistances(waypoints) {
  const cum = [0];
  for (let i = 1; i < waypoints.length; i++) {
    cum.push(cum[i - 1] + haversineKm(waypoints[i - 1], waypoints[i]));
  }
  return cum;
}

// Given a route's waypoints + cumulative distances, find the lat/lng at
// `distanceKm` along the path (clamped to the route length).
function pointAtDistance(waypoints, cumDist, distanceKm) {
  const total = cumDist[cumDist.length - 1];
  const d = Math.max(0, Math.min(distanceKm, total));
  let segIndex = 0;
  while (segIndex < cumDist.length - 2 && cumDist[segIndex + 1] < d) segIndex++;
  const segStart = cumDist[segIndex];
  const segEnd = cumDist[segIndex + 1];
  const segLen = segEnd - segStart || 1e-9;
  const t = (d - segStart) / segLen;
  const [lat1, lon1] = waypoints[segIndex];
  const [lat2, lon2] = waypoints[segIndex + 1];
  return { lat: lat1 + (lat2 - lat1) * t, lng: lon1 + (lon2 - lon1) * t };
}

// ---- fleet definition ----------------------------------------------------
const INITIAL_TRUCKS = [
  { id: "T-101", driver: "M. Boudreau", cargo: "Lumber", routeId: "route-sj-fredericton", baseSpeedKmH: 80, scheduledMinutes: 90 },
  { id: "T-102", driver: "K. LeBlanc", cargo: "Paper Products", routeId: "route-moncton-saintjohn", baseSpeedKmH: 85, scheduledMinutes: 95 },
  { id: "T-103", driver: "J. Arsenault", cargo: "Packaged Goods", routeId: "route-fredericton-edmundston", baseSpeedKmH: 90, scheduledMinutes: 160 },
  { id: "T-104", driver: "S. Doiron", cargo: "Frozen Foods", routeId: "route-moncton-bathurst", baseSpeedKmH: 85, scheduledMinutes: 130 },
  { id: "T-105", driver: "P. Landry", cargo: "Building Materials", routeId: "route-sj-fredericton", baseSpeedKmH: 75, scheduledMinutes: 100 },
  { id: "T-106", driver: "A. Cormier", cargo: "Retail Freight", routeId: "route-moncton-bathurst", baseSpeedKmH: 80, scheduledMinutes: 140 },
];

export class FleetSimulator extends EventEmitter {
  constructor() {
    super();
    this.routeGeometry = new Map();
    for (const route of ROUTES) {
      this.routeGeometry.set(route.id, {
        waypoints: route.waypoints,
        cumDist: buildCumulativeDistances(route.waypoints),
      });
    }

    this.trucks = new Map();
    INITIAL_TRUCKS.forEach((def) => this.trucks.set(def.id, this._initTruck(def)));
  }

  _initTruck(def) {
    const geom = this.routeGeometry.get(def.routeId);
    const start = geom.waypoints[0];
    return {
      ...def,
      progressKm: 0,
      elapsedMs: 0,
      speedMultiplier: 1,
      lat: start[0],
      lng: start[1],
      offRouteOffset: [0, 0],
      offRouteTicksLeft: 0,
      maintenanceTicksLeft: 0,
      status: { late: false, offRoute: false, maintenance: false },
    };
  }

  getSnapshot() {
    return Array.from(this.trucks.values()).map((t) => this._publicView(t));
  }

  getRoutes() {
    return ROUTES;
  }

  start() {
    this.interval = setInterval(() => this._tick(), TICK_MS);
  }

  stop() {
    clearInterval(this.interval);
  }

  _publicView(t) {
    const geom = this.routeGeometry.get(t.routeId);
    const total = geom.cumDist[geom.cumDist.length - 1];
    return {
      id: t.id,
      driver: t.driver,
      cargo: t.cargo,
      routeId: t.routeId,
      lat: t.lat,
      lng: t.lng,
      speedKmH: Math.round(t.baseSpeedKmH * t.speedMultiplier),
      progressPct: Math.min(100, Math.round((t.progressKm / total) * 100)),
      status: { ...t.status },
    };
  }

  _maybeTriggerAnomaly(t) {
    if (t.maintenanceTicksLeft > 0 || Math.random() > ANOMALY_CHANCE) return null;
    const roll = Math.random();
    if (roll < 0.34) {
      // breakdown -> needs maintenance, speed drops to 0 for a while
      t.maintenanceTicksLeft = MAINTENANCE_TICKS;
      t.speedMultiplier = 0;
      return { type: "maintenance", message: `${t.id} flagged for maintenance (engine fault) and has stopped.` };
    }
    if (roll < 0.67) {
      // off-route drift, corrects itself over a few ticks
      const dLat = (Math.random() - 0.5) * 0.05; // ~±2.7km
      const dLng = (Math.random() - 0.5) * 0.05;
      t.offRouteOffset = [dLat, dLng];
      t.offRouteTicksLeft = 5;
      return { type: "offRoute", message: `${t.id} has drifted off its planned route.` };
    }
    // slow-down -> risks being late
    t.speedMultiplier = 0.4;
    setTimeout(() => {
      if (t.maintenanceTicksLeft === 0) t.speedMultiplier = 1;
    }, TICK_MS * 8);
    return { type: "late", message: `${t.id} has slowed significantly and is at risk of running late.` };
  }

  _tick() {
    for (const t of this.trucks.values()) {
      const geom = this.routeGeometry.get(t.routeId);
      const total = geom.cumDist[geom.cumDist.length - 1];
      const scheduledMs = t.scheduledMinutes * 60 * 1000;

      const alert = this._maybeTriggerAnomaly(t);
      if (alert) this.emit("alert", { truckId: t.id, timestamp: Date.now(), ...alert });

      if (t.maintenanceTicksLeft > 0) {
        t.maintenanceTicksLeft--;
        if (t.maintenanceTicksLeft === 0) t.speedMultiplier = 1;
      } else {
        t.elapsedMs += TICK_MS;
        const effectiveSpeed = t.baseSpeedKmH * t.speedMultiplier;
        t.progressKm += effectiveSpeed * (TICK_MS / 3_600_000);
        if (t.progressKm >= total) {
          // completed the route -- loop back for a fresh lap (demo purposes)
          t.progressKm = 0;
          t.elapsedMs = 0;
        }
      }

      if (t.offRouteTicksLeft > 0) {
        t.offRouteTicksLeft--;
        // decay the drift back toward the real route
        t.offRouteOffset = t.offRouteOffset.map((v) => v * 0.6);
      } else {
        t.offRouteOffset = [0, 0];
      }

      const base = pointAtDistance(geom.waypoints, geom.cumDist, t.progressKm);
      t.lat = base.lat + t.offRouteOffset[0];
      t.lng = base.lng + t.offRouteOffset[1];

      const offRouteKm = haversineKm([base.lat, base.lng], [t.lat, t.lng]);
      const expectedFraction = Math.min(1, t.elapsedMs / scheduledMs);
      const actualFraction = t.progressKm / total;

      const prevStatus = t.status;
      t.status = {
        late: actualFraction < expectedFraction - LATE_FRACTION_THRESHOLD,
        offRoute: offRouteKm > OFF_ROUTE_KM,
        maintenance: t.maintenanceTicksLeft > 0,
      };

      this.emit("update", this._publicView(t));

      // fire a status-change alert for anything the anomaly roll didn't already announce
      if (!prevStatus.late && t.status.late) {
        this.emit("alert", { truckId: t.id, timestamp: Date.now(), type: "late", message: `${t.id} is now running behind schedule.` });
      }
      if (prevStatus.offRoute && !t.status.offRoute) {
        this.emit("alert", { truckId: t.id, timestamp: Date.now(), type: "resolved", message: `${t.id} is back on route.` });
      }
    }
  }
}
