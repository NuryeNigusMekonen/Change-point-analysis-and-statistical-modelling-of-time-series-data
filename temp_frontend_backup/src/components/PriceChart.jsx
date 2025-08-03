import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceDot, ReferenceLine, ResponsiveContainer } from "recharts";

const PriceChart = ({ priceData, changePoints, events }) => {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Brent Oil Price Trend</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={priceData}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="price" stroke="#8884d8" dot={false} />
          {changePoints.map((cp, i) => (
            <ReferenceLine key={i} x={cp.date} stroke="red" strokeDasharray="3 3" label={`CP${i + 1}`} />
          ))}
          {events.map((ev, i) => (
            <ReferenceDot key={i} x={ev.date} y={ev.price} r={5} fill="#82ca9d" label={ev.title} />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceChart;