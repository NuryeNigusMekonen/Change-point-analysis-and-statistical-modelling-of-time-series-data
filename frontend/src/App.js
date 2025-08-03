import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("Loading...");

  useEffect(() => {
    fetch("/api/data")  // Assumes Flask is proxying /api
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage("Error: " + err.message));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>React + Flask Change Point Dashboard</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
