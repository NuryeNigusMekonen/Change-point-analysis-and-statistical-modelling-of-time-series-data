import React from "react";

// Normalize date to YYYY-MM-DD
const normalizeDate = (dateStr) => {
  const d = new Date(dateStr);
  if (isNaN(d)) return null;
  return d.toISOString().split("T")[0];
};

// Helper: Get date ± range
const getNearbyDates = (baseDateStr, range = 7) => {
  const base = new Date(baseDateStr);
  if (isNaN(base)) return [];
  const nearby = [];
  for (let i = -range; i <= range; i++) {
    const date = new Date(base);
    date.setDate(date.getDate() + i);
    nearby.push(date.toISOString().split("T")[0]);
  }
  return nearby;
};

export default function EventPanel({ events = [], changePoints = {}, windowSize = 30 }) {
  // Prepare change point dates by type
  const cpDatesByType = {
    mean: new Set((changePoints.mean || []).map(normalizeDate)),
    trend: new Set((changePoints.trend || []).map(normalizeDate)),
    var: new Set((changePoints.var || []).map(normalizeDate)),
  };

  // Badge styles
  const badgeStyle = {
    display: "inline-block",
    padding: "2px 6px",
    borderRadius: "4px",
    fontSize: "12px",
    fontWeight: "bold",
    marginRight: "6px",
    color: "white",
  };

  const badgeColors = {
    mean: "#e74c3c",  // red
    trend: "#27ae60", // green
    var: "#2980b9",   // blue
  };

  // Match if any date in window matches
  const getChangePointTypes = (date) => {
    const types = [];
    const nearby = getNearbyDates(date, windowSize); //  use dynamic window

    for (const type of ["mean", "trend", "var"]) {
      for (const d of nearby) {
        if (cpDatesByType[type].has(d)) {
          types.push(type);
          break;
        }
      }
    }

    return types;
  };

  return (
    <div
      style={{
        flex: 1,
        maxHeight: "600px",
        overflowY: "auto",
        border: "1px solid #ccc",
        borderRadius: 5,
        padding: 10,
        minWidth: 250,
        backgroundColor: "#f9f9f9",
      }}
    >
      <h2>Key Events (±{windowSize} days)</h2>
      {events.length === 0 && <p>No events found.</p>}
      <ul style={{ listStyle: "none", paddingLeft: 0 }}>
        {events.map(({ date, event }, i) => {
          const cpTypes = getChangePointTypes(date);
          const isChange = cpTypes.length > 0;

          return (
            <li
              key={i}
              style={{
                marginBottom: 10,
                backgroundColor: isChange ? "#fef4e9" : "transparent",
                padding: "6px 8px",
                borderRadius: 4,
                border: isChange ? "1px solid #f5c16c" : "none",
              }}
            >
              <div>
                <strong>{date}:</strong> {event}
              </div>
              {isChange && (
                <div style={{ marginTop: 4 }}>
                  {cpTypes.map((type) => (
                    <span
                      key={type}
                      style={{
                        ...badgeStyle,
                        backgroundColor: badgeColors[type],
                      }}
                    >
                      {type.toUpperCase()}
                    </span>
                  ))}
                </div>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}
