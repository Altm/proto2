const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Placeholder endpoints for the wine shop admin panel
app.get('/api/products', (req, res) => {
  // Return list of products
  res.json({
    success: true,
    data: []
  });
});

app.get('/api/inventory', (req, res) => {
  // Return inventory data
  res.json({
    success: true,
    data: []
  });
});

app.get('/api/sales', (req, res) => {
  // Return sales data
  res.json({
    success: true,
    data: []
  });
});

app.get('/api/promotions', (req, res) => {
  // Return promotions data
  res.json({
    success: true,
    data: []
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});