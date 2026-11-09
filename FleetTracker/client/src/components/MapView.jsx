import { MapContainer, TileLayer, Marker, Popup, Polyline } from "react-leaflet";
import L from "leaflet";

const NB_CENTER = [46.5, -66.5];

function statusOf(truck) {
  if (truck.status.maintenance) return "maintenance";
  if (truck.status.offRoute) return "offRoute";
  if (truck.status.late) return "late";
  return "onTime";
}

const STATUS_COLOR = {
  onTime: "#22c55e",
  late: "#f59e0b",
  offRoute: "#ef4444",
  maintenance: "#a855f7",
};

function truckIcon(truck) {
  const color = STATUS_COLOR[statusOf(truck)];
  return L.divIcon({
    className: "",
    html: `<div style="
      width:16px;height:16px;border-radius:50%;
      background:${color};border:2px solid white;
      box-shadow:0 0 0 2px ${color}55;
    "></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
  });
}

export default function MapView({ trucks, routes }) {
  return (
    <div className="map-wrap">
      <MapContainer center={NB_CENTER} zoom={7} scrollWheelZoom style={{ height: "100%", width: "100%" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {routes.map((route) => (
          <Polyline
            key={route.id}
            positions={route.waypoints}
            pathOptions={{ color: "#64748b", weight: 2, dashArray: "4 6", opacity: 0.6 }}
          />
        ))}
        {trucks.map((truck) => (
          <Marker key={truck.id} position={[truck.lat, truck.lng]} icon={truckIcon(truck)}>
            <Popup>
              <strong>{truck.id}</strong> — {truck.driver}
              <br />
              Cargo: {truck.cargo}
              <br />
              Speed: {truck.speedKmH} km/h
              <br />
              Progress: {truck.progressPct}%
              <br />
              Status: {statusOf(truck)}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
