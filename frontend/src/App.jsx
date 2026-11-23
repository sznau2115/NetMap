import { useEffect, useState } from "react";
import api from "./api/client";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("checking");

  useEffect(() => {
    api.get("/api/health")
      .then(() => setBackendStatus("online"))
      .catch(() => setBackendStatus("offline"));
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <div className="logo-icon">N</div>
          <span>NetMap</span>
        </div>

        <div className="menu-label">WORKSPACE</div>

        <nav>
          <button className="nav-item active">⌂ Dashboard</button>
          <button className="nav-item">▦ Buildings</button>
          <button className="nav-item">⌘ Devices</button>
          <button className="nav-item">⇄ Connections</button>
          <button className="nav-item">◷ Monitoring</button>
        </nav>

        <div className="sidebar-bottom">
          <div className="connection-status">
            <span className={`status-dot ${backendStatus}`} />
            <div>
              <strong>Backend API</strong>
              <small>
                {backendStatus === "checking"
                  ? "Checking..."
                  : backendStatus === "online"
                  ? "Connected"
                  : "Disconnected"}
              </small>
            </div>
          </div>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace / Dashboard</span>
            <h1>Dashboard</h1>
          </div>

          <div className="topbar-right">
            <span className="version">NetMap v0.1.0</span>
          </div>
        </header>

        <section className="content">
          <div className="welcome">
            <div>
              <h2>Network infrastructure overview</h2>
              <p>
                Manage your buildings, network devices and connections
                from one place.
              </p>
            </div>
          </div>

          <div className="stats">
            <div className="stat-card">
              <span>Buildings</span>
              <strong>0</strong>
              <small>Registered buildings</small>
            </div>

            <div className="stat-card">
              <span>Devices</span>
              <strong>0</strong>
              <small>Network devices</small>
            </div>

            <div className="stat-card">
              <span>Connections</span>
              <strong>0</strong>
              <small>Network connections</small>
            </div>

            <div className="stat-card">
              <span>Online devices</span>
              <strong>0</strong>
              <small>Currently available</small>
            </div>
          </div>

          <div className="map-card">
            <div className="map-card-header">
              <div>
                <h3>Network map</h3>
                <p>Building infrastructure visualization</p>
              </div>
              <span className="coming-soon">Coming soon</span>
            </div>

            <div className="empty-map">
              <div className="empty-map-icon">⌖</div>
              <h3>No floor plans yet</h3>
              <p>
                Your network map will appear here after adding
                a building and uploading a floor plan.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;