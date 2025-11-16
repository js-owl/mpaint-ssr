<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { req_json_auth } from '../api'

interface ProductForm {
  category: string
  product: string
  price: number | null
}

const form = reactive<ProductForm>({
  category: '',
  product: '',
  price: null,
})

const submitting = ref(false)

function isValid(): boolean {
  return (
    form.category.trim().length > 0 &&
    form.product.trim().length > 0 &&
    form.price !== null &&
    Number(form.price) > 0
  )
}

async function onSubmit() {
  if (!isValid()) {
    ElMessage.warning('Заполните все поля корректно')
    return
  }
  try {
    submitting.value = true
    const res = await req_json_auth('/products/', 'POST', {
      category: form.category.trim(),
      product: form.product.trim(),
      price: Number(form.price),
    })
    if (res) {
      ElMessage.success('Продукт создан')
      onReset()
    }
  } catch (e) {
    ElMessage.error('Не удалось создать продукт')
  } finally {
    submitting.value = false
  }
}

function onReset() {
  form.category = ''
  form.product = ''
  form.price = null
}
</script>

<template>
    <div style="max-width: 560px; margin: 24px auto;">
      <h2 style="margin-bottom: 16px;">Create Product</h2>
      <el-form :model="form" label-width="120px">
        <el-form-item label="Category">
          <el-input v-model="form.category" placeholder="e.g. Electronics" />
        </el-form-item>
        <el-form-item label="Product">
          <el-input v-model="form.product" placeholder="e.g. Wireless Mouse" />
        </el-form-item>
        <el-form-item label="Price">
          <el-input-number v-model="form.price" :min="0.01" :precision="2" :step="1" controls-position="right" style="width: 100%;" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="onSubmit">Submit</el-button>
          <el-button @click="onReset" :disabled="submitting">Reset</el-button>
        </el-form-item>
      </el-form>
    </div>
   </template>

<style scoped>
</style>
