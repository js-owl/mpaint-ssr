<script lang="ts" setup>
import { reactive, ref, computed } from 'vue'
import DialogRegistration from './DialogRegistration.vue'
import { useWindowSize } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import { API_BASE_URL } from '@/api'

let dialogFormVisible = defineModel<boolean>()
const formLabelWidth = '140px'

const formData = reactive({
  username: '',
  password: '',
})

const loading = ref(false)

const isRegistrationVisible = ref(false)

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 768)

const onSubmit = async () => {
  if (!formData.username || !formData.password) {
    ElMessage.warning('Введите email и пароль')
    return
  }

  loading.value = true
  try {
    const payload = {
      email: formData.username.trim(),
      password: formData.password,
    }

    const response = await fetch(`${API_BASE_URL}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      let errorMessage = 'Ошибка входа'
      try {
        const errorBody = await response.json()
        if (typeof errorBody?.detail === 'string') {
          errorMessage = errorBody.detail
        }
      } catch {
        // ignore JSON parse errors
      }
      throw new Error(errorMessage)
    }

    const data = await response.json()
    if (data?.access_token) {
      localStorage.setItem('access_token', data.access_token)
    }

    ElMessage.success('Вы успешно вошли')

    formData.username = ''
    formData.password = ''
    dialogFormVisible.value = false
  } catch (e) {
    const message = e instanceof Error ? e.message : 'Ошибка входа'
    ElMessage.error(message)
  } finally {
    loading.value = false
  }
}

const onRegistration = async () => {
  console.log('onRegistration')
  dialogFormVisible.value = false
  isRegistrationVisible.value = true
}
</script>

<template>
  <el-dialog v-model="dialogFormVisible" title="Войти" width="500" :fullscreen="isMobile">
    <el-form :model="formData">
      <el-form-item label="Имя" :label-width="formLabelWidth">
        <el-input v-model="formData.username" autocomplete="off" />
      </el-form-item>
      <el-form-item label="Пароль" :label-width="formLabelWidth">
        <el-input v-model="formData.password" type="password" show-password />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogFormVisible = false">Отмена</el-button>
        <el-button type="primary" @click="onSubmit" :loading="loading"> Войти </el-button>
        <el-divider></el-divider>
        <div class="registration">
          <div style="margin-right: 20px">Еще нет аккаунта?</div>
          <el-button
            type="primary"
            style="background-color: #be2a44; border: 1px solid #be2a44"
            @click="onRegistration"
          >
            Зарегистрироваться
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
  <DialogRegistration v-model="isRegistrationVisible" />
</template>

<style scoped>
.registration {
  display: flex;
  justify-content: end;
  align-items: center;
  gap: 10px;
}
</style>
