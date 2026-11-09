# NB Fleet Tracker — 7-Day Build Plan

Portfolio project: a real-time dashboard simulating delivery trucks moving across New Brunswick, flagging trucks that are late, off-route, or need maintenance. Built to show event-driven architecture + map-based visualization skills (aimed at a J.D. Irving–style pitch).

**Stack (simplified for a one-week timeline):** Node.js + Express + Socket.io (backend, simulates the "message broker" role) → React + Vite + Leaflet (frontend). No Kafka/RabbitMQ — Socket.io gives you the same real-time push behavior without a day lost to broker setup. If you want to swap in Kafka later, everything in `server/simulator.js` becomes a producer and `server/index.js` becomes a consumer — the split is already there.

This folder already contains a working scaffold (`server/` and `client/`) so you're not starting blank. The plan below tells you what to learn and build each day, and points at the exact files.

## Day 1 — Get it running, understand the shape

**Learn:** what Express is doing, what Socket.io does differently from a normal HTTP request (persistent connection, server can push without being asked), what an "event-driven" system means in plain terms (producers emit events, consumers react — no polling).

**Do:**
1. `cd server && npm install && npm run dev` — confirm it boots and logs truck ticks.
2. `cd client && npm install && npm run dev` — open the dashboard, confirm markers move on the map.
3. Read `server/index.js` top to bottom. Find where a socket connection triggers `trucks:init`, and where `truck:update` gets broadcast.
4. Read `server/simulator.js`'s `tick()` method. This is the "GPS stream" — in a real system this would be 20 separate truck devices each publishing to a broker; here it's one loop for simplicity.

**Milestone:** dashboard loads locally, trucks are visibly moving.

## Day 2 — Own the simulation logic

**Learn:** haversine distance (why lat/lng math isn't flat-plane math), linear interpolation along a path, basic event-emitter patterns in Node.

**Do:**
1. In `server/routes.js`, add or tweak a 5th route (there's a real NB town list below to steal from).
2. In `server/simulator.js`, adjust `ANOMALY_CHANCE` and watch how often alerts fire.
3. Add a new truck to `INITIAL_TRUCKS` and confirm it shows up live without a restart hiccup.

**Milestone:** you can explain, without looking at the code, how a truck's lat/lng gets computed every tick.

## Day 3 — Alert logic (the "smart" part)

**Learn:** how the three anomaly types are detected — lateness (expected progress vs actual), off-route (perpendicular distance to route segment), maintenance (random fault injection). This is the part that makes it more than "dots on a map."

**Do:**
1. Read `isLate()`, `isOffRoute()`, and `maybeTriggerMaintenance()` in `simulator.js`.
2. Tighten or loosen the off-route threshold (`OFF_ROUTE_KM`) and see how sensitive detection gets.
3. Add a 4th alert type if you want a stretch goal (e.g. "low fuel" based on distance traveled).

**Milestone:** you can trigger and explain all three alert types on demand.

## Day 4 — Frontend map wiring

**Learn:** React state + effects for a live data stream, react-leaflet basics (MapContainer, Marker, Polyline, Popup).

**Do:**
1. Read `client/src/App.jsx` — see how `trucks` state is a keyed object updated on every `truck:update` event.
2. Read `client/src/components/MapView.jsx` — custom marker icons colored by status.
3. Style pass: adjust marker colors, popup content, zoom level to fit NB nicely.

**Milestone:** map looks intentional, not default-Leaflet-blue-pin.

## Day 5 — Dashboard UI (list + alerts panel)

**Learn:** deriving UI state from the same data stream two different ways (map + table), basic accessible status badges.

**Do:**
1. Flesh out `TruckList.jsx` — sortable by status would be a nice touch (late/off-route first).
2. Flesh out `AlertPanel.jsx` — cap it at last ~15 alerts, newest on top, timestamp formatting.
3. Add a summary header bar: total trucks, # late, # off-route, # in maintenance.

**Milestone:** looks like a real ops dashboard, not just a map.

## Day 6 — Polish + realism pass

**Do:**
1. Swap in more accurate route waypoints if you want (OpenStreetMap Nominatim or just eyeball real highways).
2. Add truck "cargo type" and "driver name" fields shown in popups/table — sells the enterprise angle.
3. Write a short PROJECT.md: problem statement, architecture diagram (even ASCII is fine), what you'd change for a real Kafka-based version at scale.
4. Cross-browser/basic responsive check.

**Milestone:** something you'd screen-share in an interview without flinching.

## Day 7 — Deploy + wrap

**Do:**
1. Deploy `server/` to Render or Railway (free tier is fine for a demo).
2. Deploy `client/` to Vercel or Netlify, point `VITE_SERVER_URL` at the deployed backend.
3. Record a 60–90 second screen capture: trucks moving, an alert firing live, the list updating in sync.
4. Push to GitHub with a clean README (this file, trimmed) as the front page.

**Milestone:** a live URL + repo link ready to drop into an application or portfolio.

---

## Real NB towns for extra routes (lat, lng)

- Saint John: 45.2733, -66.0633
- Fredericton: 45.9636, -66.6431
- Moncton: 46.0878, -64.7782
- Edmundston: 47.3735, -68.3251
- Bathurst: 47.6187, -65.6513
- Miramichi: 47.0281, -65.5019
- Woodstock: 46.1526, -67.5952
- Grand Falls: 47.0376, -67.7419
- Sussex: 45.7185, -65.5138
- Campbellton: 48.0065, -66.6731

## If you later want real Kafka (stretch, post-deadline)

Swap `server/simulator.js` to publish JSON messages to a Kafka topic (`kafka-node` or `kafkajs`) instead of calling `this.emit()` directly, then have `server/index.js` run a consumer that forwards messages to Socket.io. The detection logic (lateness/off-route/maintenance) doesn't need to change — only the transport between simulator and API server does. That's a clean "v2" story for an interview: "I shipped it on WebSockets to hit the deadline, then swapped the transport layer for Kafka without touching business logic."
