import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from "recharts";

// Get nearby ±windowSize days
function getNearbyDates(dateStr, windowSize) {
  const base = new Date(dateStr);
  const dates = new Set();
  for (let i = -windowSize; i <= windowSize; i++) {
    const d = new Date(base);
    d.setDate(base.getDate() + i);
    dates.add(d.toISOString().split("T")[0]);
  }
  return dates;
}

export default function ChartView({ data, changePoints, events = [], windowSize = 30 }) {
  if (!data.length) return <p>Loading price data...</p>;

  const cpStyles = {
    mean: { stroke: "red", label: "MEAN" },
    trend: { stroke: "green", label: "TREND" },
    var: { stroke: "blue", label: "VAR" }
  };

  const changePointLines = [];
  const cpDatesByType = {
    mean: new Set(changePoints.mean?.map(d => d) || []),
    trend: new Set(changePoints.trend?.map(d => d) || []),
    var: new Set(changePoints.var?.map(d => d) || []),
  };

  // Draw change point lines
  Object.keys(cpDatesByType).forEach(type => {
    cpDatesByType[type].forEach(cpDate => {
      if (data.some(d => d.date === cpDate)) {
        changePointLines.push(
          <ReferenceLine
            key={`${type}-${cpDate}`}
            x={cpDate}
            stroke={cpStyles[type].stroke}
            strokeDasharray="3 3"
            label={{
              value: cpStyles[type].label,
              position: "top",
              fill: cpStyles[type].stroke,
              fontWeight: "bold",
              fontSize: 12,
              offset: 10,
            }}
          />
        );
      }
    });
  });

  // Tag events with CP type if nearby
    const dataDates = data.map(d => d.date);

  const highlightedEvents = events.map(event => {
    const tags = [];
    let closestDate = null;
    let minDiff = Infinity;

    Object.entries(cpDatesByType).forEach(([type, cpSet]) => {
      Array.from(cpSet).forEach(cpDate => {
        const nearbyDates = getNearbyDates(cpDate, windowSize);
        if (nearbyDates.has(event.date)) {
          tags.push(type);
          // Try to find the closest matching date in actual data
          dataDates.forEach(date => {
            if (nearbyDates.has(date)) {
              const diff = Math.abs(new Date(event.date) - new Date(date));
              if (diff < minDiff) {
                minDiff = diff;
                closestDate = date;
              }
            }
          });
        }
      });
    });

    return tags.length > 0 ? { ...event, tags, chartDate: closestDate || event.date } : null;
  }).filter(Boolean);

  // Render event lines based on first tag
  const eventLines = highlightedEvents.map((event, idx) => {
    const type = event.tags[0]; // Pick first tag to color the line
    return (
      <ReferenceLine
        key={`event-${idx}`}
        x={event.chartDate}
        stroke="orange"
        strokeDasharray="4 4"
        label={{
          value: event.event,
          position: "top",
          angle: -45,
          fill: cpStyles[type]?.stroke || "orange",
          fontSize: 12,
          fontWeight: "bold",
          offset: 15,
        }}
      />
    );
  });


  return (
    <div style={{ flex: 3 }}>
      <h2>Brent Oil Prices</h2>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={data} margin={{ top: 40, right: 30, left: 0, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={60}
            interval="preserveStartEnd"
          />
          <YAxis domain={["auto", "auto"]} />
          <Tooltip />
          <Legend verticalAlign="top" />
          <Line
            type="monotone"
            dataKey="price"
            stroke="#8884d8"
            dot={false}
            animationDuration={1500}
          />
          {changePointLines}
          {eventLines}
        </LineChart>
      </ResponsiveContainer>

      <div style={{ marginTop: 10 }}>
        <span style={{ color: "red", fontWeight: "bold", marginRight: 15 }}>■ MEAN</span>
        <span style={{ color: "green", fontWeight: "bold", marginRight: 15 }}>■ TREND</span>
        <span style={{ color: "blue", fontWeight: "bold", marginRight: 15 }}>■ VAR</span>
        <span style={{ color: "orange", fontWeight: "bold" }}>■ EVENT (near CP)</span>
      </div>
    </div>
  );
}
