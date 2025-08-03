import React from "react";

const StatsSummary = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {Object.entries(stats).map(([key, val], i) => (
        <div key={i} className="bg-white p-4 rounded shadow">
          <h3 className="text-lg font-semibold capitalize">{key.replace("_", " ")}</h3>
          <p className="text-2xl font-bold">{val}</p>
        </div>
      ))}
    </div>
  );
};

export default StatsSummary;