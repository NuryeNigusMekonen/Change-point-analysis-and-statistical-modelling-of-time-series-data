import React, { useEffect, useState } from "react";
import PriceChart from "../components/PriceChart";
import EventPanel from "../components/EventPanel";
import StatsSummary from "../components/StatsSummary";
import Filters from "../components/Filters";
import { getDashboardData } from "../services/api";

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [filters, setFilters] = useState({ start: null, end: null, eventType: "all" });

  useEffect(() => {
    const fetchData = async () => {
      const res = await getDashboardData(filters);
      setData(res);
    };
    fetchData();
  }, [filters]);

  return (
    <div className="grid gap-4">
      <Filters filters={filters} setFilters={setFilters} />
      {data ? (
        <>
          <PriceChart priceData={data.prices} changePoints={data.change_points} events={data.events} />
          <StatsSummary stats={data.stats} />
          <EventPanel events={data.events} />
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Dashboard;