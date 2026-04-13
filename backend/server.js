const express = require('express');
const cors = require('cors');
require('dotenv').config();

const db = require('./db');
const app = express();

app.use(cors());
app.use(express.json());

// --- Health Check / Test Endpoint ---
app.get('/api/health', async (req, res) => {
    try {
        const [rows] = await db.query('SELECT 1 + 1 AS result');
        res.json({ status: 'healthy', db: 'connected', result: rows[0].result });
    } catch (err) {
        console.error('DB Error:', err);
        res.status(500).json({ status: 'error', message: 'Database connection failed' });
    }
});

// --- Mock API endpoints for early frontend development ---
// These will be replaced by actual DB queries when ready
app.get('/api/events', (req, res) => {
    res.json([
        { event_id: 1, event_type: 'Suspicious Login', risk_level: 'High', description: 'Login from unknown device' },
        { event_id: 2, event_type: 'Multiple Requests', risk_level: 'Medium', description: 'Unusual rapid navigation' }
    ]);
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Backend Server running on port ${PORT}`);
});
