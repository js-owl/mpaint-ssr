<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Delete } from '@element-plus/icons-vue'

type Item = {
  id: number
  category: string
  product: string
  price: number
}

const items = ref<Item[]>([])
const loading = ref<boolean>(true)
const error = ref<string>('')
const baseURL = 'http://81.177.166.4:8000'

async function loadItems() {
  try {
    const response = await fetch(`${baseURL}/products`)
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    const data: Item[] = await response.json()
    items.value = data
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to load data'
  } finally {
    loading.value = false
  }
}

async function addProduct() {
  try {
    const response = await fetch(`${baseURL}/products`, { method: 'POST' })
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    const created: Item = await response.json()
    items.value = [...items.value, created]
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to add product'
  }
}

async function deleteProduct(id: number) {
  try {
    const response = await fetch(`${baseURL}/products/${id}`, { method: 'DELETE' })
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    items.value = items.value.filter((item) => item.id !== id)
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to delete product'
  }
}

onMounted(async () => {
  await loadItems()
})
</script>

<template>
  <div class="about-page">
    <h1>Products</h1>
    <el-button type="primary" @click="addProduct">Add product</el-button>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <el-table v-else :data="items" class="data-table" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="category" label="Category" />
      <el-table-column prop="product" label="Product" />
      <el-table-column prop="price" label="Price" width="120">
        <template #default="{ row }">
          {{ Number(row.price).toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column label="Actions" width="120">
        <template #default="{ row }">
          <el-button type="danger" size="small" :icon="Delete" @click="deleteProduct(row.id)" />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped>
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.data-table thead {
  background: #f5f5f5;
}

.error {
  color: #b00020;
}

.icon-btn {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
}

.icon-btn:hover {
  opacity: 0.8;
}
</style>

