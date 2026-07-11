<script setup lang="ts">
import { onMounted, h, type Component } from 'vue'
import { useTaskStore } from '../stores/tasks'
import { NTag, NSpin, NButton, NIcon, useMessage } from 'naive-ui'
import {
  ChevronDown, ChevronUp, RefreshOutline,
  CloudUploadOutline, VideocamOutline, DocumentTextOutline,
  SparklesOutline, ClipboardOutline, CheckmarkCircleOutline,
  MicOutline, MusicalNotesOutline,
} from '@vicons/ionicons5'

const taskStore = useTaskStore()
const message = useMessage()

// 进度管线阶段定义
interface PipelineStage {
  key: string
  label: string
  icon: Component
}

const PIPELINE: PipelineStage[] = [
  { key: 'upload',     label: '上传',      icon: CloudUploadOutline },
  { key: 'extract',    label: '提取音频',  icon: VideocamOutline },
  { key: 'transcribe', label: '转写文本',  icon: DocumentTextOutline },
  { key: 'correct',    label: 'AI 修正',   icon: SparklesOutline },
  { key: 'summarize',  label: 'AI 总结',   icon: ClipboardOutline },
  { key: 'done',       label: '完成',      icon: CheckmarkCircleOutline },
]

// 文件类型图标
const fileTypeIcon = {
  audio: MusicalNotesOutline,
  video: VideocamOutline,
}

// 状态 → 管线阶段映射
const STATUS_STAGE: Record<string, number> = {
  pending:       0,  // 刚上传完
  syncing:       0,  // 上传/同步中
  extracting:    1,  // 提取音频中
  transcribing:  2,  // 转写中
  correcting:    3,  // 修正中
  summarizing:   4,  // 总结中
  completed:     5,  // 已完成
  emailed:       5,  // 已发送
  failed:       -1,  // 失败
}

function stageStatus(taskStatus: string, stageIdx: number): 'done' | 'active' | 'pending' | 'failed' {
  const currentStage = STATUS_STAGE[taskStatus] ?? -1
  if (taskStatus === 'failed') return stageIdx <= currentStage ? 'failed' : 'pending'
  if (currentStage < 0) return 'pending'
  if (stageIdx < currentStage) return 'done'
  if (stageIdx === currentStage) return 'active'
  return 'pending'
}

// 状态标签
const statusLabelMap: Record<string, { label: string; type: 'info' | 'warning' | 'success' | 'error' | 'default' }> = {
  pending:       { label: '排队中',   type: 'default' },
  syncing:       { label: '同步中',   type: 'info' },
  extracting:    { label: '提取中',   type: 'info' },
  transcribing:  { label: '转写中',   type: 'info' },
  correcting:    { label: '修正中',   type: 'warning' },
  summarizing:   { label: '总结中',   type: 'warning' },
  completed:     { label: '已完成',   type: 'success' },
  emailed:       { label: '已发送',   type: 'success' },
  failed:        { label: '失败',     type: 'error' },
}

// 展开/折叠
const expandedIds = new Set<string>()
function toggleExpand(taskId: string) {
  if (expandedIds.has(taskId)) {
    expandedIds.delete(taskId)
  } else {
    expandedIds.add(taskId)
  }
}
function isExpanded(taskId: string) {
  return expandedIds.has(taskId)
}

// 格式化文件大小
function formatSize(bytes: number | null): string {
  if (!bytes) return ''
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(() => {
  taskStore.fetchTasks()
})

function handleRefresh() {
  taskStore.fetchTasks()
}
</script>

<template>
  <div class="tasks-page">
    <!-- 页头 -->
    <div class="page-top">
      <div>
        <h2 class="page-title">任务列表</h2>
      </div>
      <n-button text class="refresh-btn" @click="handleRefresh" :loading="taskStore.loading">
        <template #icon>
          <RefreshOutline />
        </template>
      </n-button>
    </div>

    <!-- 加载中 -->
    <n-spin :show="taskStore.loading && taskStore.tasks.length === 0">
      <!-- 空状态 -->
      <div v-if="!taskStore.loading && taskStore.tasks.length === 0" class="empty-state">
        <div class="empty-icon">
          <n-icon size="56" :component="MicOutline" />
        </div>
        <p class="empty-text">还没有任务</p>
        <p class="empty-sub">拖拽音频/视频文件到下方 Dock 栏开始使用</p>
      </div>

      <!-- 任务卡片列表 -->
      <div v-else class="task-list">
        <article
          v-for="task in taskStore.tasks"
          :key="task.id"
          class="task-card"
          :class="{ failed: task.status === 'failed', expanded: isExpanded(task.id) }"
          @click="toggleExpand(task.id)"
        >
          <!-- 卡片头部 -->
          <div class="card-header">
            <div class="card-info">
              <span class="file-icon">
                <n-icon size="22" :component="fileTypeIcon[task.file_type]" />
              </span>
              <div class="card-meta">
                <span class="filename">{{ task.original_name || task.filename }}</span>
                <span class="file-meta">
                  {{ formatSize(task.file_size) }}
                  <span v-if="task.file_type === 'video'" class="video-badge">视频</span>
                </span>
              </div>
            </div>
            <div class="card-right">
              <n-tag
                :type="(statusLabelMap[task.status]?.type as any) || 'default'"
                size="small"
                round
                :bordered="false"
              >
                {{ statusLabelMap[task.status]?.label || task.status }}
              </n-tag>
              <span class="expand-icon">
                <ChevronDown v-if="!isExpanded(task.id)" />
                <ChevronUp v-else />
              </span>
            </div>
          </div>

          <!-- 进度管线 -->
          <div class="pipeline">
            <div
              v-for="(stage, idx) in PIPELINE"
              :key="stage.key"
              class="pipeline-step"
              :class="[
                stageStatus(task.status, idx),
                { 'skip-extract': task.file_type !== 'video' && stage.key === 'extract' }
              ]"
            >
              <div class="step-dot">
                <n-icon size="14" :component="stage.icon" />
              </div>
              <span class="step-label">{{ stage.label }}</span>
              <!-- 连接线 -->
              <div v-if="idx < PIPELINE.length - 1" class="step-line" />
            </div>
          </div>

          <!-- 展开详情 -->
          <div v-if="isExpanded(task.id)" class="card-detail" @click.stop>
            <div class="detail-row" v-if="task.status === 'failed' && (task as any).error_message">
              <span class="detail-label">错误信息</span>
              <span class="detail-value error-text">{{ (task as any).error_message }}</span>
            </div>
            <div class="detail-row" v-if="(task as any).transcript">
              <span class="detail-label">转写结果</span>
              <p class="detail-value transcript-preview">{{ (task as any).transcript?.slice(0, 200) }}…</p>
            </div>
            <div class="detail-row" v-if="(task as any).summary">
              <span class="detail-label">AI 总结</span>
              <p class="detail-value">{{ (task as any).summary }}</p>
            </div>
            <div class="detail-row">
              <span class="detail-label">创建时间</span>
              <span class="detail-value">{{ task.created_at }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">更新时间</span>
              <span class="detail-value">{{ task.updated_at }}</span>
            </div>
          </div>
        </article>
      </div>
    </n-spin>
  </div>
</template>

<style scoped>
.tasks-page {
  max-width: 720px;
  margin: 0 auto;
}

/* ===== 页头 ===== */
.page-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: 3px;
  margin: 0;
}

.refresh-btn {
  color: #64748b !important;
  font-size: 18px;
}

/* ===== 空状态 ===== */
.empty-state {
  text-align: center;
  padding: 80px 24px;
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 18px;
  color: #94a3b8;
  font-weight: 500;
  margin: 0 0 8px;
}

.empty-sub {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

/* ===== 任务卡片 ===== */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 16px 20px;
  cursor: pointer;
  transition: all 0.25s ease;
  backdrop-filter: blur(12px);
}

.task-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(129, 140, 248, 0.2);
}

.task-card.failed {
  border-color: rgba(239, 68, 68, 0.15);
  background: rgba(239, 68, 68, 0.04);
}

.task-card.expanded {
  border-color: rgba(129, 140, 248, 0.25);
}

/* 卡片头部 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  flex: 1;
}

.file-icon {
  font-size: 22px;
  flex-shrink: 0;
}

.card-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
  gap: 2px;
}

.filename {
  font-size: 14px;
  font-weight: 500;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.file-meta {
  font-size: 11px;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
}

.video-badge {
  display: inline-block;
  font-size: 10px;
  background: rgba(251, 146, 60, 0.15);
  color: #fb923c;
  padding: 1px 6px;
  border-radius: 4px;
}

.card-right {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.expand-icon {
  color: #64748b;
  display: flex;
  transition: transform 0.3s;
}

/* ===== 进度管线 ===== */
.pipeline {
  display: flex;
  align-items: center;
  margin-top: 14px;
  padding: 0 4px;
  gap: 0;
  overflow-x: auto;
}

.pipeline-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
  min-width: 0;
}

.step-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.04);
  border: 1.5px solid rgba(255, 255, 255, 0.08);
  transition: all 0.4s ease;
  z-index: 1;
}

.step-dot :deep(.n-icon) {
  opacity: 0.3;
  transition: opacity 0.4s;
  color: inherit;
}

.step-label {
  font-size: 10px;
  color: #475569;
  margin-top: 4px;
  white-space: nowrap;
  transition: color 0.4s;
}

/* 连接线 */
.step-line {
  position: absolute;
  top: 14px;
  left: calc(50% + 14px);
  width: calc(100% - 28px);
  height: 1.5px;
  background: rgba(255, 255, 255, 0.06);
  z-index: 0;
  transition: background 0.4s;
}

/* 跳过提取步骤（音频文件） */
.pipeline-step.skip-extract {
  display: none;
}

/* 已完成步骤 */
.pipeline-step.done .step-dot {
  background: rgba(34, 197, 94, 0.15);
  border-color: rgba(34, 197, 94, 0.4);
}
.pipeline-step.done .step-dot :deep(.n-icon) {
  opacity: 0.8;
}
.pipeline-step.done .step-label {
  color: #86efac;
}
.pipeline-step.done .step-line {
  background: rgba(34, 197, 94, 0.3);
}

/* 当前步骤 */
.pipeline-step.active .step-dot {
  background: rgba(129, 140, 248, 0.2);
  border-color: rgba(129, 140, 248, 0.6);
  box-shadow: 0 0 12px rgba(129, 140, 248, 0.2);
  animation: pulse-dot 1.8s ease-in-out infinite;
}
.pipeline-step.active .step-dot :deep(.n-icon) {
  opacity: 1;
}
.pipeline-step.active .step-label {
  color: #a5b4fc;
  font-weight: 500;
}

@keyframes pulse-dot {
  0%, 100% { box-shadow: 0 0 8px rgba(129, 140, 248, 0.2); }
  50% { box-shadow: 0 0 18px rgba(129, 140, 248, 0.4); }
}

/* 失败步骤 */
.pipeline-step.failed .step-dot {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
}
.pipeline-step.failed .step-dot :deep(.n-icon) {
  opacity: 0.8;
}
.pipeline-step.failed .step-label {
  color: #fca5a5;
}
.pipeline-step.failed .step-line {
  background: rgba(239, 68, 68, 0.2);
}

/* ===== 展开详情 ===== */
.card-detail {
  margin-top: 14px;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-bottom: 10px;
}
.detail-row:last-child {
  margin-bottom: 0;
}

.detail-label {
  font-size: 11px;
  color: #64748b;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.detail-value {
  font-size: 13px;
  color: #cbd5e1;
  line-height: 1.6;
  margin: 0;
}

.error-text {
  color: #fca5a5;
}

.transcript-preview {
  max-height: 100px;
  overflow-y: auto;
}
</style>
