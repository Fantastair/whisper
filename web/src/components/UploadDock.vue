<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '../stores/tasks'
import { NButton, useMessage } from 'naive-ui'

const emit = defineEmits<{
  uploaded: [taskId: string]
}>()

const router = useRouter()
const taskStore = useTaskStore()
const message = useMessage()

const dragging = ref(false)
const uploading = ref(false)
const progress = ref(0)

let dragCounter = 0

function onDragEnter(e: DragEvent) {
  e.preventDefault()
  dragCounter++
  dragging.value = true
}

function onDragLeave(e: DragEvent) {
  e.preventDefault()
  dragCounter--
  if (dragCounter <= 0) {
    dragCounter = 0
    dragging.value = false
  }
}

function onDragOver(e: DragEvent) {
  e.preventDefault()
}

async function handleDrop(e: DragEvent) {
  e.preventDefault()
  dragging.value = false
  dragCounter = 0
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    await uploadFile(files[0])
  }
}

async function handleClick() {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'audio/*,video/*'
  input.onchange = async () => {
    if (input.files && input.files.length > 0) {
      await uploadFile(input.files[0])
    }
  }
  input.click()
}

async function uploadFile(file: File) {
  uploading.value = true
  progress.value = 0
  try {
    const taskId = await taskStore.upload(file, (pct) => {
      progress.value = pct
    })
    message.success('上传成功')
    // 刷新任务列表
    await taskStore.fetchTasks()
    emit('uploaded', taskId)
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
    progress.value = 0
  }
}
</script>

<template>
  <div
    class="upload-dock"
    :class="{ dragging, uploading }"
    @dragenter="onDragEnter"
    @dragleave="onDragLeave"
    @dragover="onDragOver"
    @drop="handleDrop"
    @click="!uploading && handleClick()"
  >
    <!-- 上传中进度条 -->
    <div v-if="uploading" class="dock-progress">
      <div class="progress-fill" :style="{ width: progress + '%' }" />
      <span class="progress-text">上传中 {{ progress }}%</span>
    </div>

    <!-- 默认状态 -->
    <div v-else class="dock-content">
      <div class="dock-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
          <path d="M12 5v14M5 12h14" v-if="!dragging" />
          <path d="M12 2v10M8 6l4-4 4 4M4 18v2a2 2 0 002 2h12a2 2 0 002-2v-2" v-else />
        </svg>
      </div>
      <span class="dock-text" v-if="!dragging">拖拽文件到此处，或点击上传</span>
      <span class="dock-text dragging-text" v-else>松开以上传文件</span>
    </div>
  </div>
</template>

<style scoped>
.upload-dock {
  position: relative;
  margin: 0 16px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  overflow: hidden;
  user-select: none;
}

.upload-dock:hover {
  background: rgba(255, 255, 255, 0.09);
  border-color: rgba(129, 140, 248, 0.3);
}

.upload-dock.dragging {
  background: rgba(129, 140, 248, 0.12);
  border-color: rgba(129, 140, 248, 0.5);
  box-shadow: 0 0 24px rgba(129, 140, 248, 0.15);
}

.upload-dock.uploading {
  cursor: default;
  background: rgba(129, 140, 248, 0.08);
}

/* ===== 默认内容 ===== */
.dock-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
}

.dock-icon {
  color: #818cf8;
  display: flex;
  flex-shrink: 0;
}

.dock-text {
  font-size: 14px;
  color: #94a3b8;
  letter-spacing: 1px;
  transition: color 0.3s;
}

.dragging-text {
  color: #a5b4fc;
}

/* ===== 进度条 ===== */
.dock-progress {
  position: relative;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.3), rgba(129, 140, 248, 0.5));
  transition: width 0.3s ease;
  border-radius: 20px;
}

.progress-text {
  position: relative;
  z-index: 1;
  font-size: 13px;
  color: #c7d2fe;
  letter-spacing: 1px;
  font-weight: 500;
}
</style>
