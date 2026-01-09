/**
 * API service for the Wine Inventory Admin Panel
 */
import axios from 'axios';

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    // Add authorization token if it exists in localStorage
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors globally
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle global errors here
    if (error.response?.status === 401) {
      // Redirect to login if unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    return Promise.reject(error);
  }
);

// Wine API methods
const wineAPI = {
  getAll: (params = {}) => api.get('/wines/', { params }),
  getById: (id) => api.get(`/wines/${id}`),
  create: (data) => api.post('/wines/', data),
  update: (id, data) => api.put(`/wines/${id}`, data),
  delete: (id) => api.delete(`/wines/${id}`)
};

// Inventory API methods
const inventoryAPI = {
  getAll: (params = {}) => api.get('/inventories/', { params }),
  getById: (id) => api.get(`/inventories/${id}`),
  create: (data) => api.post('/inventories/', data),
  update: (id, data) => api.put(`/inventories/${id}`, data),
  delete: (id) => api.delete(`/inventories/${id}`)
};

// Sales API methods
const salesAPI = {
  getAll: (params = {}) => api.get('/sales/', { params }),
  getById: (id) => api.get(`/sales/${id}`),
  create: (data) => api.post('/sales/', data),
  update: (id, data) => api.put(`/sales/${id}`, data),
  delete: (id) => api.delete(`/sales/${id}`)
};

// Orders API methods
const ordersAPI = {
  getAll: (params = {}) => api.get('/orders/', { params }),
  getById: (id) => api.get(`/orders/${id}`),
  create: (data) => api.post('/orders/', data),
  update: (id, data) => api.put(`/orders/${id}`, data),
  delete: (id) => api.delete(`/orders/${id}`)
};

// Adjustments API methods
const adjustmentsAPI = {
  getAll: (params = {}) => api.get('/adjustments/', { params }),
  getById: (id) => api.get(`/adjustments/${id}`),
  create: (data) => api.post('/adjustments/', data),
  delete: (id) => api.delete(`/adjustments/${id}`)
};

// Reports API methods
const reportsAPI = {
  getInventoryDetails: () => api.get('/reports/inventory-details'),
  getSalesSummary: () => api.get('/reports/sales-summary')
};

export default {
  wine: wineAPI,
  inventory: inventoryAPI,
  sales: salesAPI,
  orders: ordersAPI,
  adjustments: adjustmentsAPI,
  reports: reportsAPI
};