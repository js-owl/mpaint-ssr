<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { Delete } from '@element-plus/icons-vue'
import { API_BASE_URL as baseURL } from '../api'
import { useProfileStore } from '../stores/profile.store'

type CartProduct = {
  id: number
  category: string
  product: string
  price: number
}

type CartItem = {
  id: number
  user_id: number
  product_id: number
  quantity: number
  product: CartProduct | null
}

const items = ref<CartItem[]>([])
const loading = ref<boolean>(true)
const error = ref<string>('')
const isMobile = ref<boolean>(false)

const profileStore = useProfileStore()
const { profile } = storeToRefs(profileStore)

const totalPrice = computed(() =>
  items.value.reduce((total, item) => {
    const price = item.product?.price ?? 0
    return total + price * item.quantity
  }, 0),
)

async function ensureProfileLoaded() {
  if (profile.value) return
  try {
    await profileStore.getProfile()
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to load profile'
  }
}

function getUserId(): number | null {
  const userId = profile.value?.id
  if (!userId) {
    error.value = 'User not loaded'
    return null
  }
  return userId
}

async function loadItems() {
  await ensureProfileLoaded()
  const userId = getUserId()
  if (!userId) {
    loading.value = false
    return
  }

  loading.value = true
  try {
    const response = await fetch(`${baseURL}/cart/${userId}`)
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    const data: CartItem[] = await response.json()
    items.value = data
    error.value = ''
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to load cart items'
  } finally {
    loading.value = false
  }
}

async function updateQuantity(itemId: number, newQuantity: number) {
  if (newQuantity < 1) return

  const userId = getUserId()
  if (!userId) return

  try {
    const response = await fetch(`${baseURL}/cart/${userId}/${itemId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quantity: newQuantity }),
    })
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    const updated: CartItem = await response.json()
    items.value = items.value.map((item) => (item.id === itemId ? updated : item))
    error.value = ''
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to update quantity'
  }
}

async function removeItem(itemId: number) {
  const userId = getUserId()
  if (!userId) return

  try {
    const response = await fetch(`${baseURL}/cart/${userId}/${itemId}`, {
      method: 'DELETE',
    })
    if (!response.ok && response.status !== 204) throw new Error(`Request failed: ${response.status}`)
    items.value = items.value.filter((item) => item.id !== itemId)
    error.value = ''
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to remove item'
  }
}

function decrement(item: CartItem) {
  updateQuantity(item.id, item.quantity - 1)
}

function increment(item: CartItem) {
  updateQuantity(item.id, item.quantity + 1)
}

function handleResize() {
  if (typeof window === 'undefined') return
  isMobile.value = window.innerWidth <= 600
}

onMounted(async () => {
  if (typeof window !== 'undefined') {
    handleResize()
    window.addEventListener('resize', handleResize)
  }
  await loadItems()
})

onBeforeUnmount(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('resize', handleResize)
  }
})
</script>

<template>
  <div class="cart-page">
    <h1>Корзина</h1>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <div v-if="!isMobile" class="table-wrapper">
        <el-table :data="items" class="data-table" stripe style="width: 100%">
          <el-table-column prop="product.category" label="Category" width="80">
            <template #default="{ row }">
              {{ row.product?.category ?? '—' }}
            </template>
          </el-table-column>
          <el-table-column prop="product.product" label="Product">
            <template #default="{ row }">
              {{ row.product?.product ?? '—' }}
            </template>
          </el-table-column>
          <el-table-column label="Price" width="80">
            <template #default="{ row }">
              {{ Number(row.product?.price ?? 0).toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column label="Quantity" width="140">
            <template #default="{ row }">
              <div class="quantity-controls">
                <el-button size="small" @click="decrement(row)">-</el-button>
                <span class="quantity-value">{{ row.quantity }}</span>
                <el-button size="small" @click="increment(row)">+</el-button>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="Subtotal" width="100">
            <template #default="{ row }">
              {{
                Number((row.product?.price ?? 0) * row.quantity).toFixed(2)
              }}
            </template>
          </el-table-column>
          <el-table-column label=" " width="60">
            <template #default="{ row }">
              <el-button type="danger" size="small" :icon="Delete" @click="removeItem(row.id)" />
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div v-else class="mobile-cart">
        <div v-for="item in items" :key="item.id" class="mobile-card">
          <div class="mobile-card__header">
            <div>
              <div class="mobile-card__category">
                {{ item.product?.category ?? '—' }}
              </div>
              <div class="mobile-card__name">
                {{ item.product?.product ?? '—' }}
              </div>
            </div>
            <el-button
              type="danger"
              size="small"
              :icon="Delete"
              @click="removeItem(item.id)"
            />
          </div>

          <div class="mobile-card__section">
            <span class="mobile-card__label">Price</span>
            <span class="mobile-card__value">{{ Number(item.product?.price ?? 0).toFixed(2) }}</span>
          </div>

          <div class="mobile-card__section">
            <span class="mobile-card__label">Quantity</span>
            <div class="mobile-card__value">
              <div class="quantity-controls">
                <el-button size="small" @click="decrement(item)">-</el-button>
                <span class="quantity-value">{{ item.quantity }}</span>
                <el-button size="small" @click="increment(item)">+</el-button>
              </div>
            </div>
          </div>

          <div class="mobile-card__section mobile-card__section--subtotal">
            <span class="mobile-card__label">Subtotal</span>
            <span class="mobile-card__value">
              {{ Number((item.product?.price ?? 0) * item.quantity).toFixed(2) }}
            </span>
          </div>
        </div>
      </div>

      <div class="total">
        Итоговая стоимость: {{ Number(totalPrice).toFixed(2) }}
      </div>
    </template>
  </div>
</template>

<style scoped>
.cart-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.table-wrapper {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-value {
  min-width: 24px;
  text-align: center;
}

.error {
  color: #b00020;
}

.mobile-cart {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.mobile-card {
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
  background: #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.mobile-card__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.mobile-card__category {
  font-size: 12px;
  text-transform: uppercase;
  color: #909399;
}

.mobile-card__name {
  font-weight: 600;
  margin-top: 4px;
}

.mobile-card__section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.mobile-card__section--subtotal {
  border-top: 1px solid #ebeef5;
  padding-top: 8px;
  margin-top: 12px;
  font-weight: 600;
}

.mobile-card__label {
  font-size: 14px;
  color: #606266;
}

.mobile-card__value {
  font-size: 14px;
  color: #303133;
}

.total {
  align-self: flex-end;
  font-weight: 600;
  font-size: 16px;
}

@media (max-width: 800px) {
  .cart-page {
    gap: 12px;
  }

  .data-table {
    font-size: 14px;
  }

  .total {
    align-self: stretch;
    text-align: right;
  }
}
</style>



