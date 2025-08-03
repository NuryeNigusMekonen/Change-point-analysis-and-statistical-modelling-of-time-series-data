import axios from "axios";

const API_BASE = "http://localhost:5000/api";

export const getDashboardData = async (filters) => {
  const params = new URLSearchParams(filters);
  const res = await axios.get(`${API_BASE}/dashboard?${params.toString()}`);
  return res.data;
};
