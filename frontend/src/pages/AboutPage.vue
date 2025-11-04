<script setup lang="ts">
import { onMounted, ref } from 'vue'

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
    <h1>About</h1>
    <p>This is the About page.</p>
    <button @click="addProduct">Add product</button>


    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <table v-else class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Category</th>
          <th>Product</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.category }}</td>
          <td>{{ item.product }}</td>
          <td>{{ item.price.toFixed(2) }}</td>
          <td>
            <button
              class="icon-btn"
              @click="deleteProduct(item.id)"
              aria-label="Удалить"
              title="Удалить"
            >🗑</button>
          </td>
        </tr>
      </tbody>
    </table>
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


