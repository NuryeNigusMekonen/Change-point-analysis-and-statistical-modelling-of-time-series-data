import React from "react";

export default function Header() {
  return (
    <header className="header-container">
      <div className="branding">
        <img
          src="/logo.png"
          alt="Birhan Energies Logo"
          className="company-logo"
        />
        <h2 className="company-name">Birhan Energies</h2>
      </div>

      <h1 className="animated-title">Brent Oil Price Change-Point Dashboard</h1>
      <p className="subtitle">Explore key events and their impact on Brent oil prices.</p>
      <hr />
    </header>
  );
}
