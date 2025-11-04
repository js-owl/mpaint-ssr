import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../pages/HomePage.vue'),
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('../pages/ProductsPage.vue'),
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router


