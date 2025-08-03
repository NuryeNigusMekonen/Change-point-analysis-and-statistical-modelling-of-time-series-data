import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// File: src/App.jsx
import React from "react";
import Dashboard from "./pages/Dashboard";

const App = () => {
  return (
    <main className="min-h-screen bg-gray-100 p-4">
      <Dashboard />
    </main>
  );
};

export default App;