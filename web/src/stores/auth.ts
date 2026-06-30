import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const loading = ref(false)

  const isLoggedIn = () => !!token.value

  async function login(password: string) {
    loading.value = true
    try {
      const res = await apiLogin(password)
      token.value = res.data.token
      localStorage.setItem('token', res.data.token)
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = ''
    localStorage.removeItem('token')
  }

  return { token, loading, isLoggedIn, login, logout }
})
