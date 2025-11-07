<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Delete } from '@element-plus/icons-vue'

type UserItem = {
  id: number
  name: string
  email: string
  role: string
}

const users = ref<UserItem[]>([])
const loading = ref<boolean>(true)
const error = ref<string>('')
const baseURL = 'http://81.177.166.4:8000'

async function loadUsers() {
  try {
    const response = await fetch(`${baseURL}/users`)
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    const data: UserItem[] = await response.json()
    users.value = data
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to load users'
  } finally {
    loading.value = false
  }
}

async function addUser() {
  try {
    const response = await fetch(`${baseURL}/users`, { method: 'POST' })
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    const created: UserItem = await response.json()
    users.value = [...users.value, created]
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to add user'
  }
}

async function deleteUser(id: number) {
  try {
    const response = await fetch(`${baseURL}/users/${id}`, { method: 'DELETE' })
    if (!response.ok) throw new Error(`Request failed: ${response.status}`)
    users.value = users.value.filter((user) => user.id !== id)
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to delete user'
  }
}

onMounted(async () => {
  await loadUsers()
})
</script>

<template>
  <div class="users-page">
    <h1>Пользователи</h1>
    <el-button type="primary" @click="addUser">Добавить пользователя</el-button>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <el-table v-else :data="users" class="data-table" stripe style="width: 100%">
      <el-table-column prop="name" label="Name" width="80" />
      <el-table-column prop="email" label="Email" width="150" />
      <el-table-column prop="role" label="Role" width="70" />
      <el-table-column label=" ">
        <template #default="{ row }">
          <el-button type="danger" size="small" :icon="Delete" @click="deleteUser(row.id)" />
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

@media (max-width: 800px) {
  .email-column {
    display: none;
  }
}
</style>


