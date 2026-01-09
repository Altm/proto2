<template>
  <div class="inventory">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Inventory Management</h3>
          <el-button type="primary" @click="showAddForm = true">Add Item</el-button>
        </div>
      </template>
      
      <!-- Filters -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="Product Type">
          <el-select v-model="filters.productType" placeholder="All Types">
            <el-option label="All" value="" />
            <el-option label="Bottle" value="bottle" />
            <el-option label="Glass" value="glass" />
          </el-select>
        </el-form-item>
        <el-form-item label="Vintage Year">
          <el-input v-model="filters.vintageYear" placeholder="Filter by year" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilters">Search</el-button>
        </el-form-item>
      </el-form>
      
      <!-- Inventory table -->
      <el-table :data="filteredInventory" style="width: 100%" v-loading="loading">
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
        <el-table-column prop="currentStock" label="Current Stock" width="120" />
        <el-table-column prop="reservedStock" label="Reserved" width="100" />
        <el-table-column prop="availableStock" label="Available" width="100">
          <template #default="{ row }">
            {{ row.currentStock - row.reservedStock }}
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="adjustStock(row)">Adjust</el-button>
            <el-button size="small" type="danger" @click="writeOffItem(row)">Write Off</el-button>
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
    
    <!-- Adjust Stock Dialog -->
    <el-dialog v-model="showAdjustDialog" title="Adjust Stock" width="500px">
      <el-form :model="adjustmentForm" label-width="120px">
        <el-form-item label="Product">
          <el-input v-model="adjustmentForm.productName" disabled />
        </el-form-item>
        <el-form-item label="Current Stock">
          <el-input v-model.number="adjustmentForm.currentStock" disabled />
        </el-form-item>
        <el-form-item label="New Stock Amount">
          <el-input-number 
            v-model="adjustmentForm.newAmount" 
            :min="0" 
            controls-position="right"
          />
        </el-form-item>
        <el-form-item label="Reason">
          <el-select v-model="adjustmentForm.reason" placeholder="Select reason">
            <el-option label="Count correction" value="count_correction" />
            <el-option label="Breakage" value="breakage" />
            <el-option label="Tasting" value="tasting" />
            <el-option label="Other" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="Notes">
          <el-input 
            v-model="adjustmentForm.notes" 
            type="textarea" 
            placeholder="Additional notes"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAdjustDialog = false">Cancel</el-button>
          <el-button type="primary" @click="confirmAdjustment">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- Write Off Dialog -->
    <el-dialog v-model="showWriteOffDialog" title="Write Off Item" width="500px">
      <el-form :model="writeOffForm" label-width="120px">
        <el-form-item label="Product">
          <el-input v-model="writeOffForm.productName" disabled />
        </el-form-item>
        <el-form-item label="Quantity to Write Off">
          <el-input-number 
            v-model="writeOffForm.quantity" 
            :min="1" 
            :max="writeOffForm.maxQuantity"
            controls-position="right"
          />
        </el-form-item>
        <el-form-item label="Reason">
          <el-select v-model="writeOffForm.reason" placeholder="Select reason">
            <el-option label="Breakage" value="breakage" />
            <el-option label="Tasting" value="tasting" />
            <el-option label="Expired" value="expired" />
            <el-option label="Other" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="Notes">
          <el-input 
            v-model="writeOffForm.notes" 
            type="textarea" 
            placeholder="Additional notes"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showWriteOffDialog = false">Cancel</el-button>
          <el-button type="primary" @click="confirmWriteOff">Confirm</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

// Sample inventory data
const inventoryData = ref([
  { id: 1, productName: 'Château Margaux 2018', vintageYear: 2018, productType: 'bottle', location: 'Cellar A', currentStock: 45, reservedStock: 5 },
  { id: 2, productName: 'Château Margaux 2017', vintageYear: 2017, productType: 'bottle', location: 'Cellar A', currentStock: 32, reservedStock: 3 },
  { id: 3, productName: 'Dom Pérignon 2016', vintageYear: 2016, productType: 'bottle', location: 'Cellar B', currentStock: 28, reservedStock: 2 },
  { id: 4, productName: 'Opus One 2017', vintageYear: 2017, productType: 'bottle', location: 'Cellar A', currentStock: 15, reservedStock: 0 },
  { id: 5, productName: 'Screaming Eagle Cabernet 2015', vintageYear: 2015, productType: 'bottle', location: 'VIP Room', currentStock: 8, reservedStock: 1 },
  { id: 6, productName: 'Champagne Glass Set', vintageYear: '-', productType: 'glass', location: 'Bar', currentStock: 42, reservedStock: 0 },
  { id: 7, productName: 'Wine Tasting Glass Set', vintageYear: '-', productType: 'glass', location: 'Tasting Room', currentStock: 30, reservedStock: 0 },
])

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(inventoryData.value.length)

const filters = ref({
  productType: '',
  vintageYear: ''
})

const showAdjustDialog = ref(false)
const showWriteOffDialog = ref(false)
const showAddForm = ref(false)

const adjustmentForm = ref({
  productId: null,
  productName: '',
  currentStock: 0,
  newAmount: 0,
  reason: '',
  notes: ''
})

const writeOffForm = ref({
  productId: null,
  productName: '',
  quantity: 1,
  maxQuantity: 0,
  reason: '',
  notes: ''
})

// Filtered inventory based on search criteria
const filteredInventory = computed(() => {
  return inventoryData.value.filter(item => {
    const matchesType = !filters.value.productType || item.productType === filters.value.productType
    const matchesYear = !filters.value.vintageYear || String(item.vintageYear).includes(filters.value.vintageYear)
    return matchesType && matchesYear
  })
})

const applyFilters = () => {
  // In a real app, this would trigger API call with filters
  console.log('Applying filters:', filters.value)
}

const handleSizeChange = (size) => {
  pageSize.value = size
  console.log('Page size changed:', size)
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  console.log('Current page changed:', page)
}

const adjustStock = (item) => {
  adjustmentForm.value = {
    productId: item.id,
    productName: item.productName,
    currentStock: item.currentStock,
    newAmount: item.currentStock,
    reason: '',
    notes: ''
  }
  showAdjustDialog.value = true
}

const writeOffItem = (item) => {
  writeOffForm.value = {
    productId: item.id,
    productName: item.productName,
    quantity: 1,
    maxQuantity: item.currentStock,
    reason: '',
    notes: ''
  }
  showWriteOffDialog.value = true
}

const confirmAdjustment = () => {
  // In a real app, this would make an API call
  const itemIndex = inventoryData.value.findIndex(item => item.id === adjustmentForm.value.productId)
  if (itemIndex !== -1) {
    inventoryData.value[itemIndex].currentStock = adjustmentForm.value.newAmount
    ElMessage.success(`Stock adjusted for ${adjustmentForm.value.productName}`)
  }
  showAdjustDialog.value = false
}

const confirmWriteOff = () => {
  // In a real app, this would make an API call
  const itemIndex = inventoryData.value.findIndex(item => item.id === writeOffForm.value.productId)
  if (itemIndex !== -1) {
    inventoryData.value[itemIndex].currentStock -= writeOffForm.value.quantity
    ElMessage.success(`${writeOffForm.value.quantity} items written off for ${writeOffForm.value.productName}`)
  }
  showWriteOffDialog.value = false
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
</style>