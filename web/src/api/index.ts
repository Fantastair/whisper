import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
})

// 请求拦截器：自动附加 token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：401 时跳回登录
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.hash = '#/login'
    }
    return Promise.reject(err)
  },
)

// ===== 认证 =====
export function login(password: string) {
  return api.post<{ token: string }>('/auth/login', { password })
}

// ===== 任务管理 =====
export interface Task {
  id: string
  filename: string
  status: string
  created_at: string
  updated_at: string
}

export interface TaskDetail extends Task {
  transcript?: string
  corrected_text?: string
  summary?: string
  report?: string
}

export function getTasks() {
  return api.get<Task[]>('/tasks')
}

export function getTask(id: string) {
  return api.get<TaskDetail>(`/tasks/${id}`)
}

export function uploadAudio(file: File, onProgress?: (pct: number) => void) {
  const form = new FormData()
  form.append('file', file)
  return api.post<{ task_id: string }>('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress(e) {
      if (onProgress && e.total) {
        onProgress(Math.round((e.loaded / e.total) * 100))
      }
    },
  })
}
