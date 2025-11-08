<script lang="ts" setup>
import { computed, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useWindowSize } from '@vueuse/core'
import { API_BASE_URL } from '@/api'

const dialogFormVisible = defineModel<boolean>()

interface FormData {
  username: string
  password: string
  confirmPassword: string
  email: string
  full_name?: string
  phone_number?: string
  inn?: string
}

const formRef = ref<FormInstance>()
const form = ref<FormData>({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  full_name: '',
  phone_number: '',
  inn: '',
})

const usernameError = ref('')
const emailError = ref('')

const loading = ref(false)

const { width } = useWindowSize()
const isMobile = computed(() => width.value < 768)

const containsCyrillic = (value: string) => /[\u0400-\u04FF]/.test(value)

const validateLogin = (_rule: any, value: string, callback: (error?: Error) => void) => {
  if (!value) {
    callback(new Error('Пожалуйста, введите логин'))
  } else if (value.length < 4) {
    callback(new Error('Логин должен содержать минимум 4 символа'))
  } else if (containsCyrillic(value)) {
    callback(new Error('Логин не должен содержать кириллицу'))
  } else {
    callback()
  }
}

const validatePassword = (_rule: any, value: string, callback: (error?: Error) => void) => {
  if (!value) {
    callback(new Error('Пожалуйста, введите пароль'))
  } else if (value.length < 6) {
    callback(new Error('Пароль должен содержать минимум 6 символов'))
  } else if (containsCyrillic(value)) {
    callback(new Error('Пароль не должен содержать кириллицу'))
  } else {
    callback()
  }
}

const validateConfirmPassword = (_rule: any, value: string, callback: (error?: Error) => void) => {
  if (!value) {
    callback(new Error('Пожалуйста, подтвердите пароль'))
  } else if (containsCyrillic(value)) {
    callback(new Error('Пароль не должен содержать кириллицу'))
  } else if (value !== form.value.password) {
    callback(new Error('Пароли не совпадают'))
  } else {
    callback()
  }
}

const validateEmailNoCyrillic = (_rule: any, value: string, callback: (error?: Error) => void) => {
  if (containsCyrillic(value)) {
    callback(new Error('Email не должен содержать кириллицу'))
  } else {
    callback()
  }
}

const validatePhoneNumber = (_rule: any, value: string, callback: (error?: Error) => void) => {
  if (!/^\d+$/.test(value)) {
    callback(new Error('Телефон должен содержать только цифры'))
    return
  }
  const length = value.length
  if (length < 10 || length > 15) {
    callback(new Error('Введите корректный номер телефона (10–15 цифр)'))
    return
  }
  callback()
}

const onPhoneInput = (val: string) => {
  form.value.phone_number = (val || '').replace(/\D/g, '')
}

const rules = ref<FormRules<FormData>>({
  username: [
    { required: true, message: 'Пожалуйста, введите логин', trigger: 'blur' },
    { validator: validateLogin, trigger: 'blur' },
  ],
  email: [
    { required: true, message: 'Пожалуйста, введите email', trigger: 'blur' },
    { type: 'email', message: 'Введите корректный email', trigger: ['blur', 'change'] },
    { validator: validateEmailNoCyrillic, trigger: ['blur', 'change'] },
  ],
  phone_number: [
    { required: true, message: 'Пожалуйста, введите телефон', trigger: 'blur' },
    { validator: validatePhoneNumber, trigger: ['blur', 'change'] },
  ],
  password: [
    { required: true, message: 'Пожалуйста, введите пароль', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: 'Пожалуйста, подтвердите пароль', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ],
})

const closeDialog = () => {
  dialogFormVisible.value = false
  // Reset form when closing
  form.value = {
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
    full_name: '',
    phone_number: '',
    inn: '',
  }
  usernameError.value = ''
  emailError.value = ''
  // Clear validation errors
  if (formRef.value) {
    formRef.value.clearValidate()
  }
}

const submitForm = async () => {
  if (!formRef.value) return

  usernameError.value = ''
  emailError.value = ''

  const isValid = await formRef.value.validate().catch(() => false)
  if (!isValid) return

  loading.value = true

  try {
    const payload = {
      name: form.value.full_name || form.value.username,
      email: form.value.email,
      password: form.value.password,
    }

    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    if (!response.ok) {
      let errorMessage = 'Ошибка при регистрации'
      let status: number | undefined
      try {
        const errorBody = await response.json()
        if (typeof errorBody?.detail === 'string') {
          errorMessage = errorBody.detail
        }
      } catch {
        // ignore JSON parse errors
      }
      status = response.status
      const error = new Error(errorMessage) as Error & { status?: number }
      error.status = status
      throw error
    }

    ElMessage({
      type: 'success',
      message: 'Регистрация успешно завершена!',
    })

    // Close dialog and reset form
    closeDialog()
  } catch (error) {
    console.error('Form validation/submit failed:', { error })
    const err = error as Error & { status?: number }
    if (err.status === 400) {
      if (/email/i.test(err.message)) {
        emailError.value = err.message
      } else {
        usernameError.value = err.message
      }
    } else {
      ElMessage({
        type: 'error',
        message: err.message || 'Ошибка при регистрации',
      })
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <el-dialog
    v-model="dialogFormVisible"
    title="Регистрация"
    width="500"
    :close-on-click-modal="false"
    :close-on-press-escape="true"
    :fullscreen="isMobile"
    @close="closeDialog"
  >
    <el-form
      :model="form"
      :rules="rules"
      ref="formRef"
      label-width="0"
      label-position="top"
      @submit.prevent="submitForm"
    >
      <el-form-item label="Логин" prop="username" :error="usernameError">
        <el-input
          v-model="form.username"
          placeholder="Введите логин"
          @input="usernameError = ''"
        />
      </el-form-item>

      <el-form-item label="Email" prop="email" :error="emailError">
        <el-input
          v-model="form.email"
          placeholder="Введите email"
          type="email"
          @input="emailError = ''"
        />
      </el-form-item>



      <el-form-item label="Пароль" prop="password">
        <el-input
          v-model="form.password"
          placeholder="Введите пароль"
          type="password"
          show-password
        />
      </el-form-item>

      <el-form-item label="Подтвердите пароль" prop="confirmPassword">
        <el-input
          v-model="form.confirmPassword"
          placeholder="Подтвердите пароль"
          type="password"
          show-password
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit" style="width: 100%; margin-top: 10px;" :loading="loading">
          {{ loading ? 'Регистрация...' : 'Регистрация' }}
        </el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>
