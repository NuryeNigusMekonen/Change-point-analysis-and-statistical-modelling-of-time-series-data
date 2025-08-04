import React from "react";

export default function DateFilter({ dateRange, setDateRange }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <label>
        Start Date:{" "}
        <input
          type="date"
          value={dateRange.start || ""}
          onChange={e => setDateRange(prev => ({ ...prev, start: e.target.value }))}
        />
      </label>
      <label style={{ marginLeft: 20 }}>
        End Date:{" "}
        <input
          type="date"
          value={dateRange.end || ""}
          onChange={e => setDateRange(prev => ({ ...prev, end: e.target.value }))}
        />
      </label>
    </div>
  );
}
