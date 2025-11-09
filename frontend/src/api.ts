import { ElMessage } from "element-plus"
import { useAuthStore } from "./stores/auth.store"
import router from "./router"

export const API_BASE_URL = 'http://81.177.166.4:8000' as const

export async function req_json_auth(
    endpoint: string,
    method: string = 'POST',
    data?: any
  ): Promise<Response | undefined> {
    try {
      const authStore = useAuthStore()
      const headers = new Headers()
      headers.append('Content-Type', 'application/json')
  
      if (authStore.getToken) {
        headers.append('Authorization', `Bearer ${authStore.getToken}`)
      }
  
      const body = data ? JSON.stringify(data) : undefined
  
      const res = await fetch(`${API_BASE_URL}${endpoint}`, {
        method,
        headers,
        body,
      })
      console.log('req_json_auth', { res })
      if (res.status === 401) {
        authStore.clearToken()
        router.push('/')
        throw new Error('Authentification failed')
      }
      if (res.status >= 500 && res.status < 600) {
        console.log('req_urlencoded', res.status)
        ElMessage.error('Ошибка сервера 500')
        throw new Error('Server error')
      }
      if (!res.ok) {
        throw new Error('http error')
      }
      return res
    } catch (error) {
      if (error instanceof Error && error.name === 'TypeError' && error.message.includes('fetch')) {
        ElMessage.error(`Ошибка сервера`)
      }
    }
  }