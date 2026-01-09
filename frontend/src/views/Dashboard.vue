<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-title">Total Products</div>
            <div class="stat-value">124</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-title">Inventory Value</div>
            <div class="stat-value">$24,560</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-title">Monthly Sales</div>
            <div class="stat-value">$12,340</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-title">Low Stock Items</div>
            <div class="stat-value">8</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="charts-row">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>Sales Overview</span>
            </div>
          </template>
          <div class="chart-placeholder">
            Sales chart would appear here
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>Top Products</span>
            </div>
          </template>
          <div class="top-products-list">
            <el-table :data="topProducts" style="width: 100%">
              <el-table-column prop="name" label="Product" />
              <el-table-column prop="sold" label="Sold" />
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const topProducts = ref([
  { name: 'Château Margaux 2018', sold: 42 },
  { name: 'Dom Pérignon 2016', sold: 38 },
  { name: 'Opus One 2017', sold: 35 },
  { name: 'Screaming Eagle Cabernet 2015', sold: 29 },
  { name: 'Romanée-Conti 2016', sold: 24 }
])
</script>

<style scoped>
.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-content {
  padding: 10px;
}

.stat-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-card {
  min-height: 300px;
}

.chart-placeholder {
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.card-header {
  font-weight: bold;
}

.top-products-list {
  min-height: 200px;
}
</style>