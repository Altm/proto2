<template>
  <div class="promotions">
    <el-card>
      <template #header>
        <div class="card-header">
          <h3>Promotions Management</h3>
          <el-button type="primary" @click="showAddPromotion = true">Add Promotion</el-button>
        </div>
      </template>
      
      <!-- Active promotions -->
      <el-tabs v-model="activeTab">
        <el-tab-pane label="Active Promotions" name="active">
          <el-table :data="activePromotions" style="width: 100%">
            <el-table-column prop="name" label="Promotion Name" width="200" />
            <el-table-column prop="type" label="Type" width="150">
              <template #default="{ row }">
                <el-tag :type="getPromotionTypeTag(row.type)">
                  {{ formatPromotionType(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="Description" />
            <el-table-column prop="startDate" label="Start Date" width="120" />
            <el-table-column prop="endDate" label="End Date" width="120" />
            <el-table-column label="Actions" width="200">
              <template #default="{ row }">
                <el-button size="small" @click="editPromotion(row)">Edit</el-button>
                <el-button size="small" type="danger" @click="deletePromotion(row)">Delete</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <el-tab-pane label="Inactive Promotions" name="inactive">
          <el-table :data="inactivePromotions" style="width: 100%">
            <el-table-column prop="name" label="Promotion Name" width="200" />
            <el-table-column prop="type" label="Type" width="150">
              <template #default="{ row }">
                <el-tag :type="getPromotionTypeTag(row.type)">
                  {{ formatPromotionType(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="Description" />
            <el-table-column prop="startDate" label="Start Date" width="120" />
            <el-table-column prop="endDate" label="End Date" width="120" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    
    <!-- Add/Edit Promotion Dialog -->
    <el-dialog 
      v-model="showAddPromotion" 
      :title="editingPromotion ? 'Edit Promotion' : 'Add Promotion'" 
      width="600px"
    >
      <el-form :model="promotionForm" :rules="formRules" ref="promotionFormRef" label-width="150px">
        <el-form-item label="Promotion Name" prop="name">
          <el-input v-model="promotionForm.name" placeholder="Enter promotion name" />
        </el-form-item>
        
        <el-form-item label="Promotion Type" prop="type">
          <el-select v-model="promotionForm.type" placeholder="Select promotion type" style="width: 100%">
            <el-option label="Buy 5 Get 1 Free (5+1)" value="five_plus_one" />
            <el-option label="Free Shipping over $25" value="free_shipping" />
            <el-option label="Percentage Discount" value="percentage_discount" />
            <el-option label="Fixed Amount Discount" value="fixed_discount" />
          </el-select>
        </el-form-item>
        
        <!-- Specific fields for 5+1 promotion -->
        <template v-if="promotionForm.type === 'five_plus_one'">
          <el-form-item label="Applies to Vintage Years">
            <el-select 
              v-model="promotionForm.vintageYears" 
              multiple 
              placeholder="Select vintage years (leave empty for all)"
              style="width: 100%"
            >
              <el-option 
                v-for="year in availableVintageYears" 
                :key="year" 
                :label="year" 
                :value="year" 
              />
            </el-select>
          </el-form-item>
          <el-form-item label="Applies to Products">
            <el-select 
              v-model="promotionForm.productIds" 
              multiple 
              placeholder="Select products (leave empty for all bottles)"
              style="width: 100%"
            >
              <el-option 
                v-for="product in bottleProducts" 
                :key="product.id" 
                :label="product.name" 
                :value="product.id" 
              />
            </el-select>
          </el-form-item>
        </template>
        
        <!-- Specific fields for free shipping promotion -->
        <template v-if="promotionForm.type === 'free_shipping'">
          <el-form-item label="Minimum Order Amount" prop="minOrderAmount">
            <el-input-number 
              v-model="promotionForm.minOrderAmount" 
              :precision="2" 
              :step="1" 
              :min="0" 
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
        </template>
        
        <!-- Specific fields for discount promotions -->
        <template v-if="['percentage_discount', 'fixed_discount'].includes(promotionForm.type)">
          <el-form-item 
            v-if="promotionForm.type === 'percentage_discount'" 
            label="Discount Percentage" 
            prop="discountValue"
          >
            <el-input-number 
              v-model="promotionForm.discountValue" 
              :precision="2" 
              :step="0.1" 
              :min="0" 
              :max="100" 
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
          
          <el-form-item 
            v-if="promotionForm.type === 'fixed_discount'" 
            label="Discount Amount" 
            prop="discountValue"
          >
            <el-input-number 
              v-model="promotionForm.discountValue" 
              :precision="2" 
              :step="1" 
              :min="0" 
              controls-position="right"
              style="width: 100%"
            />
          </el-form-item>
        </template>
        
        <el-form-item label="Description">
          <el-input 
            v-model="promotionForm.description" 
            type="textarea" 
            :rows="3"
            placeholder="Enter promotion description"
          />
        </el-form-item>
        
        <el-form-item label="Start Date" prop="startDate">
          <el-date-picker
            v-model="promotionForm.startDate"
            type="date"
            placeholder="Select start date"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="End Date" prop="endDate">
          <el-date-picker
            v-model="promotionForm.endDate"
            type="date"
            placeholder="Select end date"
            style="width: 100%"
          />
        </el-form-item>
        
        <el-form-item label="Active">
          <el-switch v-model="promotionForm.active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddPromotion = false">Cancel</el-button>
          <el-button type="primary" @click="savePromotion">Save</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- Promotion Details Section -->
    <el-card class="details-card" v-if="selectedPromotion">
      <template #header>
        <div class="card-header">
          <h3>{{ selectedPromotion.name }} Details</h3>
        </div>
      </template>
      
      <div class="promotion-details">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Type">
            <el-tag :type="getPromotionTypeTag(selectedPromotion.type)">
              {{ formatPromotionType(selectedPromotion.type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Status">
            <el-tag :type="selectedPromotion.active ? 'success' : 'info'">
              {{ selectedPromotion.active ? 'Active' : 'Inactive' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Start Date">
            {{ selectedPromotion.startDate }}
          </el-descriptions-item>
          <el-descriptions-item label="End Date">
            {{ selectedPromotion.endDate }}
          </el-descriptions-item>
          <el-descriptions-item label="Description" :span="2">
            {{ selectedPromotion.description }}
          </el-descriptions-item>
          
          <!-- Additional details based on promotion type -->
          <template v-if="selectedPromotion.type === 'five_plus_one'">
            <el-descriptions-item label="Applies to Vintage Years" :span="2">
              <el-tag 
                v-for="year in selectedPromotion.vintageYears || []" 
                :key="year" 
                style="margin-right: 5px;"
              >
                {{ year }}
              </el-tag>
              <span v-if="!(selectedPromotion.vintageYears && selectedPromotion.vintageYears.length)">
                All vintage years
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="Applies to Products" :span="2">
              <el-tag 
                v-for="productId in selectedPromotion.productIds || []" 
                :key="productId" 
                style="margin-right: 5px;"
              >
                {{ getProductName(productId) }}
              </el-tag>
              <span v-if="!(selectedPromotion.productIds && selectedPromotion.productIds.length)">
                All bottles
              </span>
            </el-descriptions-item>
          </template>
          
          <template v-if="selectedPromotion.type === 'free_shipping'">
            <el-descriptions-item label="Minimum Order Amount">
              ${{ selectedPromotion.minOrderAmount }}
            </el-descriptions-item>
          </template>
          
          <template v-if="['percentage_discount', 'fixed_discount'].includes(selectedPromotion.type)">
            <el-descriptions-item label="Discount Value">
              <template v-if="selectedPromotion.type === 'percentage_discount'">
                {{ selectedPromotion.discountValue }}%
              </template>
              <template v-else>
                ${{ selectedPromotion.discountValue }}
              </template>
            </el-descriptions-item>
          </template>
        </el-descriptions>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// Sample promotions data
const promotionsData = ref([
  { 
    id: 1, 
    name: '5+1 Free Promotion', 
    type: 'five_plus_one', 
    description: 'Buy 5 bottles of the same wine and vintage, get 1 free', 
    startDate: '2023-01-01', 
    endDate: '2023-12-31', 
    active: true,
    vintageYears: [2015, 2016, 2017, 2018],
    productIds: [1, 2, 3] // Specific products
  },
  { 
    id: 2, 
    name: 'Free Shipping over $25', 
    type: 'free_shipping', 
    description: 'Free shipping for orders over $25', 
    startDate: '2023-01-01', 
    endDate: '2023-12-31', 
    active: true,
    minOrderAmount: 25.00
  },
  { 
    id: 3, 
    name: 'Seasonal Discount', 
    type: 'percentage_discount', 
    description: '20% discount on selected products', 
    startDate: '2023-11-01', 
    endDate: '2023-12-31', 
    active: false,
    discountValue: 20.00
  }
])

// Sample products data (for reference)
const productsData = ref([
  { id: 1, name: 'Château Margaux 2018', category: 'red_wine', productType: 'bottle' },
  { id: 2, name: 'Château Margaux 2017', category: 'red_wine', productType: 'bottle' },
  { id: 3, name: 'Dom Pérignon 2016', category: 'sparkling', productType: 'bottle' },
  { id: 4, name: 'Wine Tasting Glass Set', category: 'glassware', productType: 'glass' },
])

const activeTab = ref('active')
const showAddPromotion = ref(false)
const editingPromotion = ref(null)
const selectedPromotion = ref(null)

const promotionForm = ref({
  name: '',
  type: '',
  description: '',
  startDate: '',
  endDate: '',
  active: true,
  // Specific to promotion types
  vintageYears: [],
  productIds: [],
  minOrderAmount: 0,
  discountValue: 0
})

const formRules = {
  name: [{ required: true, message: 'Promotion name is required', trigger: 'blur' }],
  type: [{ required: true, message: 'Promotion type is required', trigger: 'change' }],
  startDate: [{ required: true, message: 'Start date is required', trigger: 'change' }],
  endDate: [{ required: true, message: 'End date is required', trigger: 'change' }]
}

// Computed properties
const activePromotions = computed(() => {
  return promotionsData.value.filter(promo => promo.active)
})

const inactivePromotions = computed(() => {
  return promotionsData.value.filter(promo => !promo.active)
})

const availableVintageYears = computed(() => {
  // In a real app, this would come from the database
  return [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
})

const bottleProducts = computed(() => {
  return productsData.value.filter(product => product.productType === 'bottle')
})

// Methods
const getPromotionTypeTag = (type) => {
  switch(type) {
    case 'five_plus_one':
      return 'warning'
    case 'free_shipping':
      return 'success'
    case 'percentage_discount':
      return 'primary'
    case 'fixed_discount':
      return 'info'
    default:
      return 'info'
  }
}

const formatPromotionType = (type) => {
  switch(type) {
    case 'five_plus_one':
      return '5+1 Free'
    case 'free_shipping':
      return 'Free Shipping'
    case 'percentage_discount':
      return 'Percentage Discount'
    case 'fixed_discount':
      return 'Fixed Discount'
    default:
      return type
  }
}

const getProductName = (productId) => {
  const product = productsData.value.find(p => p.id === productId)
  return product ? product.name : 'Unknown Product'
}

const editPromotion = (promotion) => {
  editingPromotion.value = { ...promotion }
  promotionForm.value = { ...promotion }
  showAddPromotion.value = true
}

const deletePromotion = async (promotion) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete "${promotion.name}"?`,
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }
    )
    
    // Remove from array
    const index = promotionsData.value.findIndex(p => p.id === promotion.id)
    if (index !== -1) {
      promotionsData.value.splice(index, 1)
      ElMessage.success('Promotion deleted successfully')
    }
  } catch {
    // User cancelled deletion
  }
}

const savePromotion = async () => {
  // In a real implementation, we'd validate using Element Plus form validation
  
  if (editingPromotion.value) {
    // Update existing promotion
    const index = promotionsData.value.findIndex(p => p.id === editingPromotion.value.id)
    if (index !== -1) {
      promotionsData.value[index] = { ...promotionForm.value, id: editingPromotion.value.id }
      ElMessage.success('Promotion updated successfully')
    }
  } else {
    // Add new promotion
    const newId = Math.max(...promotionsData.value.map(p => p.id), 0) + 1
    promotionsData.value.push({ ...promotionForm.value, id: newId })
    ElMessage.success('Promotion added successfully')
  }
  
  showAddPromotion.value = false
  resetForm()
}

const resetForm = () => {
  promotionForm.value = {
    name: '',
    type: '',
    description: '',
    startDate: '',
    endDate: '',
    active: true,
    vintageYears: [],
    productIds: [],
    minOrderAmount: 0,
    discountValue: 0
  }
  editingPromotion.value = null
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.details-card {
  margin-top: 20px;
}

.promotion-details {
  padding: 20px 0;
}

.dialog-footer {
  text-align: right;
}
</style>