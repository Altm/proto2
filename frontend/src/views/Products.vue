<template>
  <div class="products">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Product Catalog</h3>
          <el-button type="primary" @click="showAddForm = true">Add Product</el-button>
        </div>
      </template>
      
      <!-- Search and filters -->
      <el-form :inline="true" class="filter-form">
        <el-form-item label="Search">
          <el-input 
            v-model="searchQuery" 
            placeholder="Search products..."
            clearable
          />
        </el-form-item>
        <el-form-item label="Category">
          <el-select v-model="filters.category" placeholder="All Categories">
            <el-option label="All" value="" />
            <el-option label="Red Wine" value="red_wine" />
            <el-option label="White Wine" value="white_wine" />
            <el-option label="Sparkling" value="sparkling" />
            <el-option label="Glassware" value="glassware" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="applyFilters">Search</el-button>
        </el-form-item>
      </el-form>
      
      <!-- Products table -->
      <el-table :data="filteredProducts" style="width: 100%" v-loading="loading">
        <el-table-column prop="name" label="Product Name" width="200" />
        <el-table-column prop="category" label="Category" width="120" />
        <el-table-column prop="producer" label="Producer" width="150" />
        <el-table-column prop="country" label="Country" width="100" />
        <el-table-column prop="region" label="Region" width="120" />
        <el-table-column prop="vintage" label="Vintage" width="80" />
        <el-table-column prop="price" label="Price" width="80">
          <template #default="{ row }">
            ${{ row.price }}
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="editProduct(row)">Edit</el-button>
            <el-button size="small" type="danger" @click="deleteProduct(row)">Delete</el-button>
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
    
    <!-- Add/Edit Product Dialog -->
    <el-dialog 
      v-model="showProductDialog" 
      :title="editingProduct ? 'Edit Product' : 'Add Product'" 
      width="600px"
    >
      <el-form :model="productForm" :rules="formRules" ref="productFormRef" label-width="120px">
        <el-form-item label="Product Name" prop="name">
          <el-input v-model="productForm.name" placeholder="Enter product name" />
        </el-form-item>
        <el-form-item label="Category" prop="category">
          <el-select v-model="productForm.category" placeholder="Select category" style="width: 100%">
            <el-option label="Red Wine" value="red_wine" />
            <el-option label="White Wine" value="white_wine" />
            <el-option label="Sparkling" value="sparkling" />
            <el-option label="Rose" value="rose" />
            <el-option label="Dessert" value="dessert" />
            <el-option label="Glassware" value="glassware" />
            <el-option label="Accessories" value="accessories" />
          </el-select>
        </el-form-item>
        <el-form-item label="Producer" prop="producer">
          <el-input v-model="productForm.producer" placeholder="Enter producer name" />
        </el-form-item>
        <el-form-item label="Country" prop="country">
          <el-input v-model="productForm.country" placeholder="Enter country" />
        </el-form-item>
        <el-form-item label="Region" prop="region">
          <el-input v-model="productForm.region" placeholder="Enter region" />
        </el-form-item>
        <el-form-item label="Vintage" prop="vintage">
          <el-input v-model="productForm.vintage" placeholder="Enter vintage year" />
        </el-form-item>
        <el-form-item label="Price" prop="price">
          <el-input-number 
            v-model="productForm.price" 
            :precision="2" 
            :step="0.01" 
            :min="0" 
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="Description">
          <el-input 
            v-model="productForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="Enter product description"
          />
        </el-form-item>
        <el-form-item label="Active">
          <el-switch v-model="productForm.active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showProductDialog = false">Cancel</el-button>
          <el-button type="primary" @click="saveProduct">Save</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// Sample product data
const productsData = ref([
  { id: 1, name: 'Château Margaux 2018', category: 'red_wine', producer: 'Château Margaux', country: 'France', region: 'Bordeaux', vintage: '2018', price: 450.00, active: true },
  { id: 2, name: 'Château Margaux 2017', category: 'red_wine', producer: 'Château Margaux', country: 'France', region: 'Bordeaux', vintage: '2017', price: 380.00, active: true },
  { id: 3, name: 'Dom Pérignon 2016', category: 'sparkling', producer: 'Moët & Chandon', country: 'France', region: 'Champagne', vintage: '2016', price: 220.00, active: true },
  { id: 4, name: 'Opus One 2017', category: 'red_wine', producer: 'Opus One Winery', country: 'USA', region: 'Napa Valley', vintage: '2017', price: 320.00, active: true },
  { id: 5, name: 'Screaming Eagle Cabernet 2015', category: 'red_wine', producer: 'Screaming Eagle', country: 'USA', region: 'Napa Valley', vintage: '2015', price: 2500.00, active: true },
  { id: 6, name: 'Champagne Glass Set', category: 'glassware', producer: 'Riedel', country: 'Austria', region: 'Kufstein', vintage: '-', price: 85.00, active: true },
  { id: 7, name: 'Wine Tasting Glass Set', category: 'glassware', producer: 'Schott Zwiesel', country: 'Germany', region: 'Bavaria', vintage: '-', price: 65.00, active: true },
])

const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(productsData.value.length)

const searchQuery = ref('')
const filters = ref({
  category: ''
})

const showProductDialog = ref(false)
const editingProduct = ref(null)

const productForm = ref({
  name: '',
  category: '',
  producer: '',
  country: '',
  region: '',
  vintage: '',
  price: 0,
  description: '',
  active: true
})

const formRules = {
  name: [{ required: true, message: 'Product name is required', trigger: 'blur' }],
  category: [{ required: true, message: 'Category is required', trigger: 'change' }],
  producer: [{ required: true, message: 'Producer is required', trigger: 'blur' }],
  price: [{ required: true, message: 'Price is required', trigger: 'blur' }]
}

// Computed property to filter products based on search and filters
const filteredProducts = computed(() => {
  return productsData.value.filter(product => {
    const matchesSearch = !searchQuery.value || 
      product.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      product.producer.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesCategory = !filters.value.category || product.category === filters.value.category
    
    return matchesSearch && matchesCategory
  })
})

const applyFilters = () => {
  // In a real app, this would trigger API call with filters
  console.log('Applying filters:', { searchQuery: searchQuery.value, filters: filters.value })
}

const handleSizeChange = (size) => {
  pageSize.value = size
  console.log('Page size changed:', size)
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  console.log('Current page changed:', page)
}

const editProduct = (product) => {
  editingProduct.value = { ...product }
  productForm.value = { ...product }
  showProductDialog.value = true
}

const deleteProduct = async (product) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete "${product.name}"?`,
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    // Remove from array
    const index = productsData.value.findIndex(p => p.id === product.id)
    if (index !== -1) {
      productsData.value.splice(index, 1)
      totalItems.value = productsData.value.length
      ElMessage.success('Product deleted successfully')
    }
  } catch {
    // User cancelled deletion
  }
}

const saveProduct = async () => {
  // Validate form
  // In a real implementation, we'd validate using Element Plus form validation
  
  if (editingProduct.value) {
    // Update existing product
    const index = productsData.value.findIndex(p => p.id === editingProduct.value.id)
    if (index !== -1) {
      productsData.value[index] = { ...productForm.value, id: editingProduct.value.id }
      ElMessage.success('Product updated successfully')
    }
  } else {
    // Add new product
    const newId = Math.max(...productsData.value.map(p => p.id), 0) + 1
    productsData.value.push({ ...productForm.value, id: newId })
    totalItems.value = productsData.value.length
    ElMessage.success('Product added successfully')
  }
  
  showProductDialog.value = false
  resetForm()
}

const resetForm = () => {
  productForm.value = {
    name: '',
    category: '',
    producer: '',
    country: '',
    region: '',
    vintage: '',
    price: 0,
    description: '',
    active: true
  }
  editingProduct.value = null
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