<template>
  <div class="sales">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Sales Management</h3>
          <el-button type="primary">New Sale</el-button>
        </div>
      </template>
      
      <!-- Filters -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="Date Range">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="To"
            start-placeholder="Start date"
            end-placeholder="End date"
          />
        </el-form-item>
        <el-form-item label="Product Type">
          <el-select v-model="filters.productType" placeholder="All Types">
            <el-option label="All" value="" />
            <el-option label="Bottle" value="bottle" />
            <el-option label="Glass" value="glass" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilters">Search</el-button>
        </el-form-item>
      </el-form>
      
      <!-- Sales table -->
      <el-table :data="filteredSales" style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="Sale ID" width="100" />
        <el-table-column prop="customer" label="Customer" width="150" />
        <el-table-column prop="productName" label="Product" width="200" />
        <el-table-column prop="vintageYear" label="Vintage" width="100" />
        <el-table-column prop="productType" label="Type" width="100">
          <template #default="{ row }">
            <el-tag :type="row.productType === 'bottle' ? 'primary' : 'success'">
              {{ row.productType }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="quantity" label="Quantity" width="100" />
        <el-table-column prop="unitPrice" label="Unit Price" width="120">
          <template #default="{ row }">
            ${{ row.unitPrice.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="totalPrice" label="Total" width="120">
          <template #default="{ row }">
            ${{ (row.quantity * row.unitPrice).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="saleDate" label="Date" width="150" />
        <el-table-column prop="status" label="Status" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- Pagination -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="totalItems"
        class="pagination"
      />
    </el-card>
    
    <!-- Sales Summary Card -->
    <el-card class="summary-card">
      <template #header>
        <div class="card-header">
          <h3>Sales Summary</h3>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="summary-item">
            <div class="summary-title">Total Sales</div>
            <div class="summary-value">${{ totalSalesAmount.toFixed(2) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="summary-item">
            <div class="summary-title">Total Items Sold</div>
            <div class="summary-value">{{ totalItemsSold }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="summary-item">
            <div class="summary-title">Average Order Value</div>
            <div class="summary-value">${{ averageOrderValue.toFixed(2) }}</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="summary-item">
            <div class="summary-title">Number of Orders</div>
            <div class="summary-value">{{ totalOrders }}</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Sample sales data
const salesData = ref([
  { id: 1001, customer: 'John Smith', productName: 'Château Margaux 2018', vintageYear: 2018, productType: 'bottle', quantity: 2, unitPrice: 450.00, saleDate: '2023-10-15', status: 'completed' },
  { id: 1002, customer: 'Emma Johnson', productName: 'Dom Pérignon 2016', vintageYear: 2016, productType: 'bottle', quantity: 1, unitPrice: 220.00, saleDate: '2023-10-16', status: 'completed' },
  { id: 1003, customer: 'Michael Brown', productName: 'Wine Tasting Glass Set', vintageYear: '-', productType: 'glass', quantity: 4, unitPrice: 65.00, saleDate: '2023-10-16', status: 'completed' },
  { id: 1004, customer: 'Sarah Davis', productName: 'Opus One 2017', vintageYear: 2017, productType: 'bottle', quantity: 1, unitPrice: 320.00, saleDate: '2023-10-17', status: 'pending' },
  { id: 1005, customer: 'Robert Wilson', productName: 'Château Margaux 2017', vintageYear: 2017, productType: 'bottle', quantity: 3, unitPrice: 380.00, saleDate: '2023-10-18', status: 'completed' },
  { id: 1006, customer: 'Jennifer Lee', productName: 'Champagne Glass Set', vintageYear: '-', productType: 'glass', quantity: 2, unitPrice: 85.00, saleDate: '2023-10-18', status: 'completed' },
  { id: 1007, customer: 'David Miller', productName: 'Screaming Eagle Cabernet 2015', vintageYear: 2015, productType: 'bottle', quantity: 1, unitPrice: 2500.00, saleDate: '2023-10-19', status: 'completed' },
])

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(salesData.value.length)

const dateRange = ref([])
const filters = ref({
  productType: ''
})

// Computed properties for sales summary
const totalSalesAmount = computed(() => {
  return salesData.value.reduce((sum, sale) => sum + (sale.quantity * sale.unitPrice), 0)
})

const totalItemsSold = computed(() => {
  return salesData.value.reduce((sum, sale) => sum + sale.quantity, 0)
})

const totalOrders = computed(() => {
  return salesData.value.length
})

const averageOrderValue = computed(() => {
  return totalOrders.value > 0 ? totalSalesAmount.value / totalOrders.value : 0
})

// Filtered sales based on search criteria
const filteredSales = computed(() => {
  return salesData.value.filter(sale => {
    const matchesType = !filters.value.productType || sale.productType === filters.value.productType
    
    // Date range filtering would go here in a real implementation
    const matchesDate = true // Placeholder for date filtering
    
    return matchesType && matchesDate
  })
})

const applyFilters = () => {
  // In a real app, this would trigger API call with filters
  console.log('Applying filters:', { dateRange: dateRange.value, filters: filters.value })
}

const handleSizeChange = (size) => {
  pageSize.value = size
  console.log('Page size changed:', size)
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  console.log('Current page changed:', page)
}

const getStatusType = (status) => {
  switch(status) {
    case 'completed':
      return 'success'
    case 'pending':
      return 'warning'
    case 'cancelled':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-form {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.summary-card {
  margin-top: 20px;
}

.summary-item {
  text-align: center;
  padding: 10px;
}

.summary-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.summary-value {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}
</style>