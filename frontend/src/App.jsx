import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
        <nav className="glass-card" style={{ display: 'flex', gap: '20px', marginBottom: '40px', alignItems: 'center' }}>
          <h2 style={{ margin: 0, marginRight: 'auto', color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '24px' }}>🛡️</span> BankingSecurity
          </h2>
          <Link to="/">Login</Link>
          <Link to="/dashboard">User Portal</Link>
          <Link to="/admin" style={{ color: 'var(--accent-alert)' }}>Admin Security</Link>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="glass-card" style={{ maxWidth: '400px', margin: '100px auto', textAlign: 'center' }}>
              <h2>Secure Login</h2>
              <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>
                Authenticating will securely track your IP, DEVICE, and generated SESSION.
              </p>
              <button style={{ marginTop: '2rem', padding: '10px 24px', background: 'var(--accent-primary)', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', width: '100%' }}>Authenticate</button>
            </div>
          } />
          
          <Route path="/dashboard" element={
            <div className="glass-card" style={{ borderLeft: '4px solid var(--accent-success)' }}>
              <h1>User Portal</h1>
              <p style={{ color: 'var(--text-secondary)' }}>Welcome to your secure banking interface.</p>
              <div style={{ marginTop: '2rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                 <div className="glass-card"><h3>Accounts Overview</h3><p>Data from ACCOUNT table</p></div>
                 <div className="glass-card"><h3>Transfer Funds</h3><p>Will trigger trg_check_amount</p></div>
              </div>
            </div>
          } />

          <Route path="/admin" element={
            <div className="glass-card" style={{ borderLeft: '4px solid var(--accent-alert)' }}>
              <h1 style={{ color: 'var(--accent-alert)' }}>Security Command Center</h1>
              <p style={{ color: 'var(--text-secondary)' }}>Live monitoring of system requests and suspicious activities.</p>
              <div style={{ marginTop: '2rem', display: 'grid', gridTemplateColumns: '1fr', gap: '1rem' }}>
                 <div className="glass-card" style={{ background: 'rgba(239, 68, 68, 0.1)' }}>
                    <h3 style={{ color: 'var(--accent-alert)' }}>High Risk Events</h3>
                    <p>Data retrieved from SECURITY_EVENT table.</p>
                 </div>
              </div>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
