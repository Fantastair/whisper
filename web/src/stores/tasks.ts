import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTasks, getTask, uploadAudio } from '../api'
import type { Task, TaskDetail } from '../api'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const currentTask = ref<TaskDetail | null>(null)
  const loading = ref(false)

  async function fetchTasks() {
    loading.value = true
    try {
      const res = await getTasks()
      tasks.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function fetchTask(id: string) {
    loading.value = true
    try {
      const res = await getTask(id)
      currentTask.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function upload(file: File, onProgress?: (pct: number) => void) {
    const res = await uploadAudio(file, onProgress)
    return res.data.task_id
  }

  return { tasks, currentTask, loading, fetchTasks, fetchTask, upload }
})
