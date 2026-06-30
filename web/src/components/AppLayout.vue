<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { NMenu, NButton, NLayout, NLayoutSider, NLayoutHeader, NLayoutContent, NIcon } from 'naive-ui'
import { CloudUploadSharp, ListSharp, LogOutSharp } from '@vicons/ionicons5'
import { h, computed } from 'vue'
import { useMessage } from 'naive-ui'
import LogoIcon from './LogoIcon.vue'

const auth = useAuthStore()
const router = useRouter()
const message = useMessage()

const menuOptions = computed(() => [
  {
    label: '上传音频',
    key: 'upload',
    icon: () => h(CloudUploadSharp),
  },
  {
    label: '任务列表',
    key: 'tasks',
    icon: () => h(ListSharp),
  },
])

function handleMenuUpdate(key: string) {
  router.push(`/${key}`)
}

function handleLogout() {
  auth.logout()
  message.success('已退出')
  router.push('/login')
}
</script>

<template>
  <n-layout has-sider class="app-layout">
    <!-- 侧边栏：桌面端 -->
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="220"
      :native-scrollbar="false"
      class="sider"
    >
      <div class="sider-header">
        <LogoIcon :size="28" class="sider-logo" />
        <span class="title">轻 语</span>
      </div>
      <n-menu
        :options="menuOptions"
        :value="router.currentRoute.value.name as string"
        @update:value="handleMenuUpdate"
      />
      <div class="sider-footer">
        <n-button quaternary size="small" @click="handleLogout">
          <template #icon>
            <n-icon><log-out-sharp /></n-icon>
          </template>
          退出
        </n-button>
      </div>
    </n-layout-sider>

    <!-- 主体内容 -->
    <n-layout>
      <!-- 顶部栏：移动端 -->
      <n-layout-header class="mobile-header">
        <div class="mobile-header-inner">
          <LogoIcon :size="24" class="mobile-logo" />
          <span class="title">轻 语</span>
          <n-button quaternary size="small" @click="handleLogout">
            <template #icon>
              <n-icon><log-out-sharp /></n-icon>
            </template>
          </n-button>
        </div>
        <n-menu
          :options="menuOptions"
          :value="router.currentRoute.value.name as string"
          mode="horizontal"
          @update:value="handleMenuUpdate"
        />
      </n-layout-header>

      <n-layout-content class="main-content">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
}

.sider {
  background: #fff;
  border-right: 1px solid #f1f5f9;
}

.sider-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px 16px;
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: 4px;
}

.sider-header .sider-logo {
  color: #4f46e5;
  flex-shrink: 0;
}

.sider-footer {
  position: absolute;
  bottom: 16px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
}

.mobile-header {
  display: none;
  background: #fff;
  border-bottom: 1px solid #f1f5f9;
}

.mobile-header-inner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  letter-spacing: 3px;
}

.mobile-header .mobile-logo {
  color: #4f46e5;
  flex-shrink: 0;
}

.main-content {
  padding: 24px;
  background: #f8fafc;
  min-height: calc(100vh - 48px);
}

@media (max-width: 768px) {
  .sider {
    display: none;
  }

  .mobile-header {
    display: block;
  }

  .main-content {
    padding: 16px;
    min-height: calc(100vh - 100px);
  }
}
</style>
