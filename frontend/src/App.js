import React, { useEffect, useState } from "react";
import axios from "axios";
import Header from "./components/Header";
import ChartView from "./components/ChartView";
import EventPanel from "./components/EventPanel";
import DateFilter from "./components/DateFilter";

import "./styles.css";

function App() {
  const [prices, setPrices] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoints, setChangePoints] = useState({});
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [windowSize, setWindowSize] = useState(30);

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
    <div className="app">
      <Header />

      {/* Date Filters */}
      <DateFilter
        dateRange={{ start: startDate, end: endDate }}
        setDateRange={(updater) => {
          if (typeof updater === "function") {
            // If updater is a function (like setDateRange(prev => ...))
            const prev = { start: startDate, end: endDate };
            const next = updater(prev);
            setStartDate(next.start);
            setEndDate(next.end);
          } else {
            // If updater is an object
            setStartDate(updater.start);
            setEndDate(updater.end);
          }
        }}
      />


      {/* Window Size Selector */}
      <div className="date-filter-container">
        <label>
          Match Window (± days)
          <select
            value={windowSize}
            onChange={e => setWindowSize(Number(e.target.value))}
            style={{ padding: "8px", borderRadius: "6px", marginTop: "5px" }}
          >
            <option value={1}>1</option>
            <option value={7}>7</option>
            <option value={14}>14</option>
            <option value={30}>30</option>
            <option value={60}>60</option>
          </select>
        </label>

        <button
          onClick={fetchData}
          style={{
            padding: "10px 16px",
            backgroundColor: "#14213d",
            color: "#fff",
            border: "none",
            borderRadius: "6px",
            fontWeight: "bold",
            cursor: "pointer",
            marginTop: "20px",
            height: "42px"
          }}
        >
          Filter
        </button>
      </div>

      {/* Chart + Events */}
      <div style={{ display: "flex", gap: 30 }}>
        <EventPanel events={events} changePoints={changePoints} windowSize={windowSize} />
        <ChartView data={prices} changePoints={changePoints} events={events} windowSize={windowSize} />
      </div>
    </div>
  );
}

export default App;
