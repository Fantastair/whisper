<script setup lang="ts">
import { onMounted } from 'vue'
import { useTaskStore } from '../stores/tasks'
import { NTag, NCard, NEmpty, NSpin, NTable, NButton, useMessage } from 'naive-ui'

const taskStore = useTaskStore()
const message = useMessage()

const statusMap: Record<string, { label: string; type: 'info' | 'warning' | 'success' | 'error' | 'default' }> = {
  pending: { label: '等待处理', type: 'default' },
  syncing: { label: '同步中', type: 'info' },
  transcribing: { label: '转写中', type: 'info' },
  correcting: { label: '矫正中', type: 'warning' },
  summarizing: { label: '总结中', type: 'warning' },
  completed: { label: '已完成', type: 'success' },
  emailed: { label: '已发送', type: 'success' },
  failed: { label: '失败', type: 'error' },
}

onMounted(() => {
  taskStore.fetchTasks()
})
</script>

<template>
  <div class="tasks-page">
    <div class="page-header">
      <h2 class="page-title">任务列表</h2>
      <p class="page-desc">追踪你的音频处理进度</p>
    </div>

    <n-card class="tasks-card" :bordered="false">
      <n-spin :show="taskStore.loading">
        <div v-if="!taskStore.loading && taskStore.tasks.length === 0" class="empty-state">
          <p class="empty-icon">📭</p>
          <p class="empty-text">暂无任务</p>
          <p class="empty-sub">去上传一个音频开始使用吧</p>
        </div>

        <n-table v-else :bordered="false" :single-line="false" size="small">
          <thead>
            <tr>
              <th>文件名</th>
              <th style="width:120px">状态</th>
              <th style="width:180px">上传时间</th>
              <th style="width:100px">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task in taskStore.tasks" :key="task.id">
              <td class="filename-cell">{{ task.filename }}</td>
              <td>
                <n-tag :type="(statusMap[task.status]?.type as any) || 'default'" size="small" round>
                  {{ statusMap[task.status]?.label || task.status }}
                </n-tag>
              </td>
              <td class="time-cell">{{ task.created_at }}</td>
              <td>
                <n-button
                  v-if="task.status === 'completed' || task.status === 'emailed'"
                  size="small"
                  quaternary
                  class="view-btn"
                  @click="message.info('报告查看功能将在后续版本实现')"
                >
                  查看
                </n-button>
              </td>
            </tr>
          </tbody>
        </n-table>
      </n-spin>
    </n-card>
  </div>
</template>

<style scoped>
.tasks-page {
  max-width: 900px;
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

.tasks-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 48px;
  margin: 0 0 16px;
}

.empty-text {
  font-size: 16px;
  color: #475569;
  font-weight: 500;
  margin: 0 0 6px;
}

.empty-sub {
  font-size: 13px;
  color: #94a3b8;
  margin: 0;
}

.filename-cell {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.time-cell {
  color: #64748b;
  font-size: 13px;
}

.view-btn {
  color: #6366f1 !important;
}
</style>
