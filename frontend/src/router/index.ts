import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../pages/HomePage.vue'),
  },
  {
    path: '/product',
    name: 'product',
    component: () => import('../pages/ProductPage.vue'),
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('../pages/ProductsPage.vue'),
  },
  {
    path: '/cart',
    name: 'cart',
    component: () => import('../pages/CartPage.vue'),
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('../pages/UsersPage.vue'),
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router


