import React from "react";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine
} from "recharts";

export default function ChartView({ data, changePoints, events = [] }) {
  if (!data.length) return <p>Loading price data...</p>;

  const cpStyles = {
    mean: { stroke: "red", label: "MEAN" },
    trend: { stroke: "green", label: "TREND" },
    var: { stroke: "blue", label: "VAR" }
  };

  const changePointLines = [];
  ["mean", "trend", "var"].forEach(type => {
    if (!changePoints[type]) return;
    changePoints[type].forEach(cpDate => {
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

  const eventLines = events.map((event, idx) => {
  console.log("Event:", event.date, event.event);
  if (data.some(d => d.date === event.date)) {
    return (
      <ReferenceLine
        key={`event-${idx}`}
        x={event.date}
        stroke="orange"
        strokeDasharray="4 4"
        label={{
          value: event.event,
          position: "top",
          fill: "orange",
          fontSize: 10,
          fontStyle: "italic",
          offset: 15,
        }}
      />
    );
  }
  return null;
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
        <span style={{ color: "orange", fontWeight: "bold" }}>■ EVENT</span>
      </div>
    </div>
  );
}
