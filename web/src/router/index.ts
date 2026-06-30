import { createRouter, createWebHashHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../pages/Login.vue'),
  },
  {
    path: '/',
    component: () => import('../components/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/upload',
      },
      {
        path: 'upload',
        name: 'Upload',
        component: () => import('../pages/Upload.vue'),
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('../pages/Tasks.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

// 导航守卫：未登录跳转到登录页
router.beforeEach((to) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    return '/login'
  }
})

export default router
