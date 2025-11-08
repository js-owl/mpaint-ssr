<template>
  <ElDialog
    v-model="visible"
    class="registration-dialog"
    title="Регистрация"
    width="460px"
    :close-on-click-modal="false"
    :destroy-on-close="false"
    @closed="handleClosed"
  >
    <ElForm
      ref="formRef"
      :model="form"
      :rules="rules"
      label-position="top"
      class="registration-form"
    >
      <ElFormItem label="Имя" prop="name">
        <ElInput v-model="form.name" autocomplete="name" placeholder="Введите имя" />
      </ElFormItem>

      <ElFormItem label="Email" prop="email">
        <ElInput
          v-model="form.email"
          type="email"
          autocomplete="email"
          placeholder="Введите email"
        />
      </ElFormItem>

      <ElFormItem label="Роль" prop="role">
        <ElSelect v-model="form.role" placeholder="Выберите роль" filterable>
          <ElOption
            v-for="option in roleOptions"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </ElSelect>
      </ElFormItem>

      <ElFormItem label="Пароль" prop="password">
        <ElInput
          v-model="form.password"
          type="password"
          autocomplete="new-password"
          show-password
          placeholder="Придумайте пароль"
        />
      </ElFormItem>
    </ElForm>

    <template #footer>
      <div class="dialog-footer">
        <ElButton @click="handleCancel" :disabled="isSubmitting">Отмена</ElButton>
        <ElButton type="primary" :loading="isSubmitting" @click="handleSubmit">
          Зарегистрироваться
        </ElButton>
      </div>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { API_BASE_URL } from '@/api'

type RegistrationForm = {
  name: string
  email: string
  role: string
  password: string
}

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (event: 'update:modelValue', value: boolean): void
  (event: 'registered', payload: Record<string, unknown>): void
}>()

const visible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
})

const roleOptions = [
  { label: 'Пользователь', value: 'user' },
  { label: 'Администратор', value: 'admin' },
  { label: 'Менеджер', value: 'manager' },
]

const formRef = ref<FormInstance>()
const form = reactive<RegistrationForm>({
  name: '',
  email: '',
  role: roleOptions[0]?.value ?? '',
  password: '',
})

const rules: FormRules<RegistrationForm> = {
  name: [
    { required: true, message: 'Введите имя', trigger: 'blur' },
    { min: 2, message: 'Имя должно содержать минимум 2 символа', trigger: 'blur' },
  ],
  email: [
    { required: true, message: 'Введите email', trigger: 'blur' },
    { type: 'email', message: 'Некорректный формат email', trigger: ['blur', 'change'] },
  ],
  role: [{ required: true, message: 'Выберите роль', trigger: 'change' }],
  password: [
    { required: true, message: 'Введите пароль', trigger: 'blur' },
    { min: 6, message: 'Пароль должен содержать минимум 6 символов', trigger: 'blur' },
  ],
}

const isSubmitting = ref(false)

const resetForm = () => {
  form.name = ''
  form.email = ''
  form.role = roleOptions[0]?.value ?? ''
  form.password = ''
  formRef.value?.clearValidate()
}

watch(
  () => props.modelValue,
  (value) => {
    if (!value) {
      resetForm()
    }
  }
)

const handleCancel = () => {
  visible.value = false
}

const handleSubmit = async () => {
  if (!formRef.value) {
    return
  }

  try {
    isSubmitting.value = true
    await formRef.value.validate()

    const response = await fetch(`${API_BASE_URL}/users/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form),
    })

    const payload = await response.json().catch(() => null)

    if (!response.ok) {
      const detail =
        (payload && typeof payload === 'object' && 'detail' in payload && payload.detail) ||
        'Не удалось зарегистрировать пользователя'
      throw new Error(typeof detail === 'string' ? detail : 'Не удалось зарегистрировать пользователя')
    }

    ElMessage.success('Пользователь успешно зарегистрирован')
    emit('registered', payload ?? {})
    visible.value = false
  } catch (error) {
    const message =
      error instanceof Error ? error.message : 'Произошла ошибка при регистрации пользователя'
    ElMessage.error(message)
  } finally {
    isSubmitting.value = false
  }
}

const handleClosed = () => {
  resetForm()
}
</script>

<style scoped>
.registration-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>

