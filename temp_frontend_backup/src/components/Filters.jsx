import React from "react";

const Filters = ({ filters, setFilters }) => {
  return (
    <div className="bg-white p-4 rounded shadow flex flex-wrap gap-4 items-end">
      <div>
        <label className="block text-sm font-medium">Start Date</label>
        <input type="date" value={filters.start || ""} onChange={e => setFilters(f => ({ ...f, start: e.target.value }))} className="border rounded p-1" />
      </div>
      <div>
        <label className="block text-sm font-medium">End Date</label>
        <input type="date" value={filters.end || ""} onChange={e => setFilters(f => ({ ...f, end: e.target.value }))} className="border rounded p-1" />
      </div>
      <div>
        <label className="block text-sm font-medium">Event Type</label>
        <select value={filters.eventType} onChange={e => setFilters(f => ({ ...f, eventType: e.target.value }))} className="border rounded p-1">
          <option value="all">All</option>
          <option value="conflict">Conflict</option>
          <option value="policy">Policy</option>
          <option value="economic">Economic</option>
        </select>
      </div>
    </div>
  );
};

export default Filters;