import { useEffect, useState } from "react";
import { socket } from "./socket";
import MapView from "./components/MapView.jsx";
import TruckList from "./components/TruckList.jsx";
import AlertPanel from "./components/AlertPanel.jsx";

const SERVER_URL = import.meta.env.VITE_SERVER_URL || "http://localhost:4000";

export default function App() {
  const [trucks, setTrucks] = useState({});
  const [routes, setRoutes] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    fetch(`${SERVER_URL}/api/routes`)
      .then((r) => r.json())
      .then(setRoutes)
      .catch(() => {});

    function onConnect() {
      setConnected(true);
    }
    function onDisconnect() {
      setConnected(false);
    }
    function onInit(list) {
      const map = {};
      for (const t of list) map[t.id] = t;
      setTrucks(map);
    }
    function onUpdate(truck) {
      setTrucks((prev) => ({ ...prev, [truck.id]: truck }));
    }
    function onAlert(alert) {
      setAlerts((prev) => [alert, ...prev].slice(0, 15));
    }

    socket.on("connect", onConnect);
    socket.on("disconnect", onDisconnect);
    socket.on("trucks:init", onInit);
    socket.on("truck:update", onUpdate);
    socket.on("alert:new", onAlert);

    return () => {
      socket.off("connect", onConnect);
      socket.off("disconnect", onDisconnect);
      socket.off("trucks:init", onInit);
      socket.off("truck:update", onUpdate);
      socket.off("alert:new", onAlert);
    };
  }, []);

  const truckList = Object.values(trucks);
  const counts = truckList.reduce(
    (acc, t) => {
      if (t.status.late) acc.late++;
      if (t.status.offRoute) acc.offRoute++;
      if (t.status.maintenance) acc.maintenance++;
      return acc;
    },
    { late: 0, offRoute: 0, maintenance: 0 }
  );

  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <span className="brand-mark" />
          <div>
            <h1>NB Fleet Tracker</h1>
            <p>Live delivery truck monitoring across New Brunswick</p>
          </div>
        </div>
        <div className="summary">
          <SummaryStat label="Trucks" value={truckList.length} />
          <SummaryStat label="Late" value={counts.late} tone="warn" />
          <SummaryStat label="Off Route" value={counts.offRoute} tone="danger" />
          <SummaryStat label="Maintenance" value={counts.maintenance} tone="danger" />
          <span className={`conn-dot ${connected ? "on" : "off"}`} title={connected ? "Connected" : "Disconnected"} />
        </div>
      </header>

      <main className="app-body">
        <MapView trucks={truckList} routes={routes} />
        <aside className="sidebar">
          <TruckList trucks={truckList} />
          <AlertPanel alerts={alerts} />
        </aside>
      </main>
    </div>
  );
}

function SummaryStat({ label, value, tone }) {
  return (
    <div className={`stat ${tone ?? ""} ${value > 0 && tone ? "active" : ""}`}>
      <span className="stat-value">{value}</span>
      <span className="stat-label">{label}</span>
    </div>
  );
}
