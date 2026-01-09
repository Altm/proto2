import { createRouter, createWebHistory } from 'vue-router'

// Import components dynamically
const Dashboard = () => import('../views/Dashboard.vue')
const Inventory = () => import('../views/Inventory.vue')
const Products = () => import('../views/Products.vue')
const Sales = () => import('../views/Sales.vue')
const Reports = () => import('../views/Reports.vue')
const Promotions = () => import('../views/Promotions.vue')

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/inventory',
    name: 'Inventory',
    component: Inventory
  },
  {
    path: '/products',
    name: 'Products',
    component: Products
  },
  {
    path: '/sales',
    name: 'Sales',
    component: Sales
  },
  {
    path: '/reports',
    name: 'Reports',
    component: Reports
  },
  {
    path: '/promotions',
    name: 'Promotions',
    component: Promotions
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router