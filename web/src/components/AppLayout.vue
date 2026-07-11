<script setup lang="ts">
import { useAuthStore } from "../stores/auth"
import { useRouter } from "vue-router"
import { NButton, useMessage } from "naive-ui"
import LogoIcon from "./LogoIcon.vue"
import UploadDock from "./UploadDock.vue"

const auth = useAuthStore()
const router = useRouter()
const message = useMessage()

function handleLogout() {
  auth.logout()
  message.success("已退出")
  router.push("/login")
}
</script>

<template>
  <div class="app-shell">
    <header class="top-bar">
      <div class="top-brand">
        <LogoIcon :size="24" />
        <span class="top-title">轻 语</span>
      </div>
      <n-button text class="logout-btn" @click="handleLogout">
        退出
      </n-button>
    </header>

    <main class="main-area">
      <router-view />
    </main>

    <footer class="bottom-dock">
      <UploadDock />
    </footer>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(160deg, #0f172a 0%, #1e293b 30%, #312e81 70%, #1e1b4b 100%);
  color: #e2e8f0;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.top-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #e2e8f0;
}

.top-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 6px;
  color: #f1f5f9;
  text-shadow: 0 2px 12px rgba(129, 140, 248, 0.3);
}

.logout-btn {
  color: #94a3b8 !important;
  font-size: 13px;
  letter-spacing: 1px;
}

.logout-btn:hover {
  color: #e2e8f0 !important;
}

.main-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  padding-bottom: 100px;
}

.bottom-dock {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
}
</style>
