import React from "react";

const EventPanel = ({ events }) => {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Event List</h2>
      <ul className="space-y-2">
        {events.map((ev, i) => (
          <li key={i} className="border p-2 rounded hover:bg-gray-50">
            <strong>{ev.title}</strong> — {ev.date} — Impact: {ev.impact}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EventPanel;