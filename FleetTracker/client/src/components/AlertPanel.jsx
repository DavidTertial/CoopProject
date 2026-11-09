const TYPE_ICON = {
  late: "⏱",
  offRoute: "⚠",
  maintenance: "🔧",
  resolved: "✓",
};

function timeAgo(ts) {
  const secs = Math.max(0, Math.round((Date.now() - ts) / 1000));
  if (secs < 60) return `${secs}s ago`;
  return `${Math.round(secs / 60)}m ago`;
}

export default function AlertPanel({ alerts }) {
  return (
    <section className="panel">
      <h2>Live Alerts</h2>
      <div className="alert-list">
        {alerts.map((alert, i) => (
          <div className={`alert-row alert-${alert.type}`} key={`${alert.timestamp}-${i}`}>
            <span className="alert-icon">{TYPE_ICON[alert.type] ?? "•"}</span>
            <div>
              <div className="alert-message">{alert.message}</div>
              <div className="alert-time">{timeAgo(alert.timestamp)}</div>
            </div>
          </div>
        ))}
        {alerts.length === 0 && <p className="empty">No alerts yet — fleet is running smoothly.</p>}
      </div>
    </section>
  );
}
