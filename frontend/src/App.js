import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "./components/Header";
import ChartView from "./components/ChartView";
import EventPanel from "./components/EventPanel";

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState({});
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const fetchData = () => {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;

    axios.get("http://localhost:5000/api/prices", { params }).then(res => setPrices(res.data));
    axios.get("http://localhost:5000/api/events", { params }).then(res => setEvents(res.data));

    ["mean", "trend", "var"].forEach(type =>
      axios.get(`http://localhost:5000/api/change_points/${type}`).then(res =>
        setChangePoints(prev => ({ ...prev, [type]: res.data.change_points }))
      )
    );
  };

  useEffect(() => {
    fetchData();
  }, [startDate, endDate]);

  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <Header />

      <div style={{ marginBottom: 20 }}>
        <label>
          Start Date:{" "}
          <input
            type="date"
            value={startDate}
            onChange={e => setStartDate(e.target.value)}
          />
        </label>{" "}
        <label>
          End Date:{" "}
          <input
            type="date"
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
          />
        </label>
        <button onClick={fetchData} style={{ marginLeft: 10, padding: "5px 10px" }}>
          Filter
        </button>
      </div>

      <div style={{ display: "flex", gap: 30 }}>
        <EventPanel events={events} />
        <ChartView data={prices} changePoints={changePoints} events={events} />
      </div>
    </div>
  );
}

export default App;
