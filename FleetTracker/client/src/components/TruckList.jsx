function statusBadge(truck) {
  if (truck.status.maintenance) return { label: "Maintenance", cls: "badge-purple" };
  if (truck.status.offRoute) return { label: "Off Route", cls: "badge-red" };
  if (truck.status.late) return { label: "Late", cls: "badge-amber" };
  return { label: "On Time", cls: "badge-green" };
}

function severity(truck) {
  if (truck.status.maintenance) return 0;
  if (truck.status.offRoute) return 1;
  if (truck.status.late) return 2;
  return 3;
}

export default function TruckList({ trucks }) {
  const sorted = [...trucks].sort((a, b) => severity(a) - severity(b));

  return (
    <section className="panel">
      <h2>Fleet ({trucks.length})</h2>
      <div className="truck-table">
        {sorted.map((truck) => {
          const badge = statusBadge(truck);
          return (
            <div className="truck-row" key={truck.id}>
              <div className="truck-row-main">
                <strong>{truck.id}</strong>
                <span className={`badge ${badge.cls}`}>{badge.label}</span>
              </div>
              <div className="truck-row-sub">
                {truck.driver} · {truck.cargo}
              </div>
              <div className="truck-row-sub">
                {truck.speedKmH} km/h · {truck.progressPct}% of route
              </div>
            </div>
          );
        })}
        {trucks.length === 0 && <p className="empty">Waiting for fleet data…</p>}
      </div>
    </section>
  );
}
