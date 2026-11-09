import express from "express";
import { createServer } from "node:http";
import { Server } from "socket.io";
import cors from "cors";
import { FleetSimulator } from "./simulator.js";

const PORT = process.env.PORT || 4000;

const app = express();
app.use(cors());
app.use(express.json());

const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: "*" },
});

const simulator = new FleetSimulator();

// REST fallbacks / initial page loads
app.get("/api/health", (_req, res) => res.json({ ok: true }));
app.get("/api/routes", (_req, res) => res.json(simulator.getRoutes()));
app.get("/api/trucks", (_req, res) => res.json(simulator.getSnapshot()));

io.on("connection", (socket) => {
  console.log(`[socket] client connected: ${socket.id}`);
  socket.emit("trucks:init", simulator.getSnapshot());

  socket.on("disconnect", () => {
    console.log(`[socket] client disconnected: ${socket.id}`);
  });
});

// Simulator is the "producer" side of the event-driven pipeline: every tick
// it emits update/alert events, which we simply forward to all connected
// dashboards over Socket.io. Swapping this for a real Kafka consumer later
// only touches this file, not the simulation/detection logic.
simulator.on("update", (truck) => {
  io.emit("truck:update", truck);
});

simulator.on("alert", (alert) => {
  io.emit("alert:new", alert);
  console.log(`[alert] ${alert.type.toUpperCase()} — ${alert.message}`);
});

simulator.start();

httpServer.listen(PORT, () => {
  console.log(`Fleet tracker server listening on http://localhost:${PORT}`);
});
