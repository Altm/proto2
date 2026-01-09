<template>
  <div class="reports">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Reports & Inventory</h3>
        </div>
      </template>
      
      <!-- Report selection and filters -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="Report Type">
          <el-select v-model="reportType" placeholder="Select report type">
            <el-option label="Sales Report" value="sales" />
            <el-option label="Inventory Report" value="inventory" />
            <el-option label="Discrepancy Report" value="discrepancy" />
          </el-select>
        </el-form-item>
        <el-form-item label="Date Range">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="To"
            start-placeholder="Start date"
            end-placeholder="End date"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="generateReport">Generate Report</el-button>
          <el-button>Export PDF</el-button>
        </el-form-item>
      </el-form>
      
      <!-- Inventory Report Section -->
      <div v-if="reportType === 'inventory'" class="report-section">
        <h4>Inventory Report</h4>
        
        <!-- Inventory Table -->
        <el-table :data="inventoryReportData" style="width: 100%" v-loading="loading">
          <el-table-column prop="productName" label="Product Name" width="200" />
          <el-table-column prop="vintageYear" label="Vintage Year" width="120" />
          <el-table-column prop="productType" label="Type" width="100">
            <template #default="{ row }">
              <el-tag :type="row.productType === 'bottle' ? 'primary' : 'success'">
                {{ row.productType }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="location" label="Location" width="120" />
          <el-table-column prop="recordedStock" label="Recorded Stock" width="120" />
          <el-table-column prop="actualStock" label="Actual Count" width="120">
            <template #default="{ row }">
              <el-input-number 
                v-model="row.actualStock" 
                :min="0" 
                size="small"
                @change="calculateDiscrepancy(row)"
              />
            </template>
          </el-table-column>
          <el-table-column prop="discrepancy" label="Discrepancy" width="120">
            <template #default="{ row }">
              <span :class="getDiscrepancyClass(row.discrepancy)">
                {{ row.discrepancy }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="Status" width="120">
            <template #default="{ row }">
              <el-tag :type="getDiscrepancyTagType(row.discrepancy)">
                {{ getDiscrepancyStatus(row.discrepancy) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="report-actions">
          <el-button type="primary" @click="submitInventoryCount">Submit Counts</el-button>
          <el-button @click="resetCounts">Reset Counts</el-button>
        </div>
      </div>
      
      <!-- Sales Report Section -->
      <div v-else-if="reportType === 'sales'" class="report-section">
        <h4>Sales Report</h4>
        
        <!-- Sales by Vintage Chart -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>Sales by Vintage Year</span>
            </div>
          </template>
          <div class="chart-placeholder">
            Sales by vintage chart would appear here
          </div>
        </el-card>
        
        <!-- Sales by Product Type Chart -->
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>Sales by Product Type</span>
            </div>
          </template>
          <div class="chart-placeholder">
            Sales by product type chart would appear here
          </div>
        </el-card>
        
        <!-- Detailed Sales Table -->
        <el-table :data="salesReportData" style="width: 100%" v-loading="loading">
          <el-table-column prop="productName" label="Product Name" width="200" />
          <el-table-column prop="vintageYear" label="Vintage Year" width="120" />
          <el-table-column prop="productType" label="Type" width="100">
            <template #default="{ row }">
              <el-tag :type="row.productType === 'bottle' ? 'primary' : 'success'">
                {{ row.productType }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="soldQuantity" label="Quantity Sold" width="120" />
          <el-table-column prop="revenue" label="Revenue" width="120">
            <template #default="{ row }">
              ${{ row.revenue.toFixed(2) }}
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- Discrepancy Report Section -->
      <div v-else-if="reportType === 'discrepancy'" class="report-section">
        <h4>Discrepancy Report</h4>
        
        <el-table :data="discrepancyReportData" style="width: 100%" v-loading="loading">
          <el-table-column prop="productName" label="Product Name" width="200" />
          <el-table-column prop="vintageYear" label="Vintage Year" width="120" />
          <el-table-column prop="productType" label="Type" width="100">
            <template #default="{ row }">
              <el-tag :type="row.productType === 'bottle' ? 'primary' : 'success'">
                {{ row.productType }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="location" label="Location" width="120" />
          <el-table-column prop="recordedStock" label="Recorded" width="100" />
          <el-table-column prop="actualStock" label="Actual" width="100" />
          <el-table-column prop="difference" label="Difference" width="100">
            <template #default="{ row }">
              <span :class="getDiscrepancyClass(row.difference)">
                {{ row.difference }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="variancePercentage" label="Variance %" width="120">
            <template #default="{ row }">
              {{ ((Math.abs(row.difference) / row.recordedStock) * 100).toFixed(2) }}%
            </template>
          </el-table-column>
          <el-table-column prop="reason" label="Reason" width="150">
            <template #default="{ row }">
              <el-select v-model="row.reason" placeholder="Select reason" size="small">
                <el-option label="Count error" value="count_error" />
                <el-option label="Breakage" value="breakage" />
                <el-option label="Tasting" value="tasting" />
                <el-option label="Missing" value="missing" />
                <el-option label="Other" value="other" />
              </el-select>
            </template>
          </el-table-column>
        </el-table>
        
        <div class="report-actions">
          <el-button type="primary" @click="processDiscrepancies">Process Discrepancies</el-button>
        </div>
      </div>
      
      <!-- Summary Cards -->
      <el-row :gutter="20" class="summary-row" v-if="reportType !== 'discrepancy'">
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="summary-item">
              <div class="summary-title">Total Items</div>
              <div class="summary-value">{{ totalItems }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="summary-item">
              <div class="summary-title">Total Value</div>
              <div class="summary-value">${{ totalValue.toFixed(2) }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="summary-item">
              <div class="summary-title">Discrepancies</div>
              <div class="summary-value">{{ discrepancyCount }}</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="summary-card">
            <div class="summary-item">
              <div class="summary-title">Avg Variance %</div>
              <div class="summary-value">{{ avgVariancePercent.toFixed(2) }}%</div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// Sample inventory report data
const inventoryReportData = ref([
  { id: 1, productName: 'Château Margaux 2018', vintageYear: 2018, productType: 'bottle', location: 'Cellar A', recordedStock: 45, actualStock: 43, discrepancy: -2 },
  { id: 2, productName: 'Château Margaux 2017', vintageYear: 2017, productType: 'bottle', location: 'Cellar A', recordedStock: 32, actualStock: 32, discrepancy: 0 },
  { id: 3, productName: 'Dom Pérignon 2016', vintageYear: 2016, productType: 'bottle', location: 'Cellar B', recordedStock: 28, actualStock: 29, discrepancy: 1 },
  { id: 4, productName: 'Opus One 2017', vintageYear: 2017, productType: 'bottle', location: 'Cellar A', recordedStock: 15, actualStock: 14, discrepancy: -1 },
  { id: 5, productName: 'Screaming Eagle Cabernet 2015', vintageYear: 2015, productType: 'bottle', location: 'VIP Room', recordedStock: 8, actualStock: 8, discrepancy: 0 },
  { id: 6, productName: 'Champagne Glass Set', vintageYear: '-', productType: 'glass', location: 'Bar', recordedStock: 42, actualStock: 40, discrepancy: -2 },
  { id: 7, productName: 'Wine Tasting Glass Set', vintageYear: '-', productType: 'glass', location: 'Tasting Room', recordedStock: 30, actualStock: 30, discrepancy: 0 },
])

// Sample sales report data
const salesReportData = ref([
  { id: 1, productName: 'Château Margaux 2018', vintageYear: 2018, productType: 'bottle', soldQuantity: 15, revenue: 6750.00 },
  { id: 2, productName: 'Dom Pérignon 2016', vintageYear: 2016, productType: 'bottle', soldQuantity: 8, revenue: 1760.00 },
  { id: 3, productName: 'Wine Tasting Glass Set', vintageYear: '-', productType: 'glass', soldQuantity: 12, revenue: 780.00 },
  { id: 4, productName: 'Opus One 2017', vintageYear: 2017, productType: 'bottle', soldQuantity: 5, revenue: 1600.00 },
])

// Sample discrepancy report data
const discrepancyReportData = ref([
  { id: 1, productName: 'Château Margaux 2018', vintageYear: 2018, productType: 'bottle', location: 'Cellar A', recordedStock: 45, actualStock: 43, difference: -2, variancePercentage: 4.44, reason: 'breakage' },
  { id: 3, productName: 'Dom Pérignon 2016', vintageYear: 2016, productType: 'bottle', location: 'Cellar B', recordedStock: 28, actualStock: 29, difference: 1, variancePercentage: 3.57, reason: 'count_error' },
  { id: 4, productName: 'Opus One 2017', vintageYear: 2017, productType: 'bottle', location: 'Cellar A', recordedStock: 15, actualStock: 14, difference: -1, variancePercentage: 6.67, reason: 'tasting' },
  { id: 6, productName: 'Champagne Glass Set', vintageYear: '-', productType: 'glass', location: 'Bar', recordedStock: 42, actualStock: 40, difference: -2, variancePercentage: 4.76, reason: 'breakage' },
])

const loading = ref(false)
const reportType = ref('inventory')
const dateRange = ref([])

// Computed values for summary cards
const totalItems = computed(() => {
  if (reportType.value === 'inventory') {
    return inventoryReportData.value.length
  } else if (reportType.value === 'sales') {
    return salesReportData.value.reduce((sum, item) => sum + item.soldQuantity, 0)
  }
  return 0
})

const totalValue = computed(() => {
  if (reportType.value === 'inventory') {
    // Calculate based on some price per item - simplified calculation
    return inventoryReportData.value.reduce((sum, item) => sum + (item.recordedStock * 100), 0)
  } else if (reportType.value === 'sales') {
    return salesReportData.value.reduce((sum, item) => sum + item.revenue, 0)
  }
  return 0
})

const discrepancyCount = computed(() => {
  return inventoryReportData.value.filter(item => item.discrepancy !== 0).length
})

const avgVariancePercent = computed(() => {
  const discrepancies = inventoryReportData.value.filter(item => item.recordedStock > 0)
  if (discrepancies.length === 0) return 0
  
  const totalVariance = discrepancies.reduce((sum, item) => {
    return sum + Math.abs(item.discrepancy) / item.recordedStock * 100
  }, 0)
  
  return totalVariance / discrepancies.length
})

const generateReport = () => {
  // In a real app, this would fetch data from the API
  console.log('Generating report:', { reportType: reportType.value, dateRange: dateRange.value })
  ElMessage.info(`Generating ${reportType.value} report...`)
}

const calculateDiscrepancy = (item) => {
  item.discrepancy = item.actualStock - item.recordedStock
}

const getDiscrepancyClass = (value) => {
  if (value === 0) return 'discrepancy-zero'
  return value > 0 ? 'discrepancy-positive' : 'discrepancy-negative'
}

const getDiscrepancyTagType = (value) => {
  if (value === 0) return 'success'
  return value > 0 ? 'warning' : 'danger'
}

const getDiscrepancyStatus = (value) => {
  if (value === 0) return 'Match'
  return value > 0 ? 'Excess' : 'Shortage'
}

const submitInventoryCount = () => {
  // In a real app, this would submit counts to the API
  ElMessage.success('Inventory counts submitted successfully!')
  console.log('Submitting inventory counts:', inventoryReportData.value)
}

const resetCounts = () => {
  inventoryReportData.value.forEach(item => {
    item.actualStock = item.recordedStock
    item.discrepancy = 0
  })
  ElMessage.info('Counts reset to recorded values')
}

const processDiscrepancies = () => {
  // In a real app, this would process discrepancies in the API
  ElMessage.success('Discrepancies processed successfully!')
  console.log('Processing discrepancies:', discrepancyReportData.value)
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

.report-section {
  margin-top: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.report-actions {
  margin-top: 20px;
  text-align: right;
}

.summary-row {
  margin-top: 30px;
}

.summary-card {
  text-align: center;
}

.summary-item {
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

.discrepancy-zero {
  color: #67c23a;
}

.discrepancy-positive {
  color: #e6a23c;
}

.discrepancy-negative {
  color: #f56c6c;
}
</style>