import React from "react";

export default function EventPanel({ events }) {
  return (
    <div style={{
      flex: 1,
      maxHeight: "600px",
      overflowY: "auto",
      border: "1px solid #ccc",
      borderRadius: 5,
      padding: 10,
      minWidth: 250,
      backgroundColor: "#f9f9f9"
    }}>
      <h2>Key Events</h2>
      {events.length === 0 && <p>No events found.</p>}
      <ul style={{ listStyle: "none", paddingLeft: 0 }}>
        {events.map(({ date, event }, i) => (
          <li key={i} style={{ marginBottom: 8 }}>
            <strong>{date}:</strong> {event}
          </li>
        ))}
      </ul>
    </div>
  );
}
