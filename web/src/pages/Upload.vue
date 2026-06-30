<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useTaskStore } from '../stores/tasks'
import { NUpload, NUploadDragger, NButton, NProgress, NCard, NSpace, NText, NIcon, useMessage } from 'naive-ui'
import { CloudUploadOutline } from '@vicons/ionicons5'

const router = useRouter()
const taskStore = useTaskStore()
const message = useMessage()

const uploading = ref(false)
const progress = ref(0)
const selectedFile = ref<File | null>(null)

function handleFileChange(files: File[]) {
  if (files.length > 0) {
    selectedFile.value = files[0]
  }
}

async function handleUpload() {
  if (!selectedFile.value) {
    message.warning('请先选择一个音频文件')
    return
  }

  uploading.value = true
  progress.value = 0
  try {
    const taskId = await taskStore.upload(selectedFile.value, (pct) => {
      progress.value = pct
    })
    message.success('上传成功！任务已创建')
    router.push(`/tasks`)
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '上传失败，请重试')
  } finally {
    uploading.value = false
    progress.value = 0
    selectedFile.value = null
  }
}
</script>

<template>
  <div class="upload-page">
    <div class="page-header">
      <h2 class="page-title">上传音频</h2>
      <p class="page-desc">将音频文件上传至轻语，自动转写与总结</p>
    </div>

    <n-card class="upload-card" :bordered="false">
      <n-space vertical size="large">
        <n-text class="hint">
          🎵 支持 MP3、WAV、M4A、FLAC 等常见格式，单文件大小不限
        </n-text>

        <div class="drop-zone">
          <n-upload
            :max="1"
            :disabled="uploading"
            accept="audio/*"
            @change="({ fileList }) => handleFileChange(fileList.map(f => f.file!))"
          >
            <n-upload-dragger>
              <div class="upload-hint">
                <n-icon size="56" color="#6366f1">
                  <cloud-upload-outline />
                </n-icon>
                <p class="upload-text" :class="{ hasFile: selectedFile }">
                  {{ selectedFile ? selectedFile.name : '点击或拖拽音频文件到此处' }}
                </p>
                <p v-if="!selectedFile" class="upload-sub">
                  文件大小不限 · 支持长音频（2h+）
                </p>
                <p v-if="selectedFile" class="upload-size">
                  {{ (selectedFile.size / 1024 / 1024).toFixed(1) }} MB
                </p>
              </div>
            </n-upload-dragger>
          </n-upload>
        </div>

        <n-progress
          v-if="uploading"
          type="line"
          :percentage="progress"
          :indicator-placement="'inside'"
          processing
          :height="24"
          :border-radius="12"
          color="#6366f1"
        />

        <n-button
          type="primary"
          size="large"
          block
          round
          :disabled="!selectedFile || uploading"
          :loading="uploading"
          class="upload-btn"
          @click="handleUpload"
        >
          {{ uploading ? '上传中 ' + progress + '%' : '开始上传' }}
        </n-button>
      </n-space>
    </n-card>
  </div>
</template>

<style scoped>
.upload-page {
  max-width: 620px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: 2px;
  margin: 0;
}

.page-desc {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 6px;
}

.upload-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.hint {
  color: #64748b;
  font-size: 13px;
}

.drop-zone {
  border: 2px dashed #e2e8f0;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.drop-zone:hover {
  border-color: #818cf8;
  background: rgba(99, 102, 241, 0.02);
}

.upload-hint {
  text-align: center;
  padding: 32px 24px;
}

.upload-text {
  font-size: 15px;
  color: #334155;
  margin-top: 16px;
  font-weight: 500;
  word-break: break-all;
}

.upload-text.hasFile {
  color: #6366f1;
}

.upload-sub {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 6px;
}

.upload-size {
  font-size: 12px;
  color: #6366f1;
  margin-top: 4px;
  font-weight: 500;
}

.upload-btn {
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important;
}

.upload-btn:hover:not(:disabled) {
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
}
</style>
