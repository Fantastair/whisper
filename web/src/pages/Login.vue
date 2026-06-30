<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { NInput, NButton, NCard, useMessage } from 'naive-ui'
import LogoIcon from '../components/LogoIcon.vue'

const router = useRouter()
const auth = useAuthStore()
const message = useMessage()

const password = ref('')
const error = ref('')

const inputTheme = {
  color: 'transparent',
  colorFocus: 'transparent',
  border: '1px solid transparent',
  borderFocus: '1px solid transparent',
  borderHover: '1px solid transparent',
  borderRadius: '0',
  textColor: '#e2e8f0',
  placeholderColor: '#64748b',
  caretColor: '#818cf8',
  paddingLeft: '4px',
  paddingRight: '4px',
}

async function handleLogin() {
  if (!password.value) {
    error.value = '请输入密码'
    return
  }
  error.value = ''
  try {
    await auth.login(password.value)
    message.success('登录成功')
    router.push('/upload')
  } catch {
    error.value = '密码错误，请重试'
  }
}
</script>

<template>
  <div class="login-page">
    <!-- 装饰背景 -->
    <div class="bg-decoration">
      <div class="circle c1" />
      <div class="circle c2" />
      <div class="circle c3" />
    </div>

    <div class="login-wrapper">
      <!-- Logo 区域 -->
      <div class="brand">
        <div class="logo-icon">
          <LogoIcon :size="72" />
        </div>
        <h1 class="brand-name">轻 语</h1>
        <p class="brand-tagline">说者有意 · 听者无心</p>
      </div>

      <!-- 登录卡片 -->
      <n-card class="login-card" :bordered="false">
        <n-input
          v-model:value="password"
          type="password"
          placeholder="请输入密钥"
          size="large"
          clearable
          :theme-overrides="inputTheme"
          :input-props="{ autocomplete: 'current-password' }"
          @keyup.enter="handleLogin"
        >
          <template #prefix>
            <img src="/key.svg" alt="" class="key-svg" />
          </template>
        </n-input>

        <div v-if="error" class="error-msg" @click="error = ''">
          <span class="error-icon">⚠</span>
          {{ error }}
          <span class="error-close">×</span>
        </div>

        <n-button
          type="primary"
          size="large"
          block
          round
          :loading="auth.loading"
          class="login-btn"
          @click="handleLogin"
        >
          {{ auth.loading ? '验证中...' : '进入轻语' }}
        </n-button>
      </n-card>

      <div class="footer-note">
        <span>本网站为私人使用，本项目已开源，可自行部署</span>
        <a href="https://github.com/your-username/whisper-tools" target="_blank" class="github-link" title="GitHub">
          <img src="/GitHub.svg" alt="GitHub" class="github-icon" />
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(160deg, #0f172a 0%, #1e293b 30%, #312e81 70%, #1e1b4b 100%);
  padding: 24px;
  position: relative;
  overflow: hidden;
}

/* 装饰背景圆 */
.bg-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
}
.c1 {
  width: 400px;
  height: 400px;
  background: #818cf8;
  top: -100px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}
.c2 {
  width: 300px;
  height: 300px;
  background: #c084fc;
  bottom: -80px;
  left: -60px;
  animation: float 10s ease-in-out infinite reverse;
}
.c3 {
  width: 200px;
  height: 200px;
  background: #6366f1;
  top: 50%;
  left: 50%;
  animation: float 12s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(20px, -20px) scale(1.05); }
  66% { transform: translate(-10px, 15px) scale(0.95); }
}

.login-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 380px;
}

/* Logo 区域 */
.brand {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  margin-bottom: 16px;
  color: #e2e8f0;
  animation: breathe 3s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.08); opacity: 0.8; }
}

.brand-name {
  font-size: 36px;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: 8px;
  margin: 0;
  text-shadow: 0 2px 20px rgba(129, 140, 248, 0.3);
}

.brand-tagline {
  font-size: 14px;
  color: #94a3b8;
  margin-top: 8px;
  letter-spacing: 4px;
}

/* 登录卡片 */
.login-card {
  width: 100%;
  background: rgba(255, 255, 255, 0.06) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  border-radius: 48px !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* 输入框底线样式 (背景/边框由 theme-overrides 控制) */

/* Naive UI 边框层 : 隐藏，用手动底线替代 */
.login-card :deep(.n-input__border),
.login-card :deep(.n-input__state-border) {
  display: none !important;
}

/* wrapper 底部横线 */
.login-card :deep(.n-input-wrapper) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
  padding-bottom: 4px !important;
}

/* 聚焦时底线高亮 */
.login-card :deep(.n-input--focus .n-input-wrapper) {
  border-bottom-color: rgba(129, 140, 248, 0.6) !important;
}

.login-card :deep(.n-input__placeholder) {
  color: #64748b !important;
}

.input-icon {
  font-size: 16px;
  line-height: 1;
}

.key-svg {
  width: 18px;
  height: 18px;
  opacity: 0.55;
}

/* 自定义错误提示 */
.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
  padding: 10px 14px;
  border-radius: 10px;
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.error-msg:hover {
  background: rgba(239, 68, 68, 0.18);
}

.error-icon {
  font-size: 14px;
  flex-shrink: 0;
}

.error-close {
  margin-left: auto;
  font-size: 16px;
  opacity: 0.6;
  transition: opacity 0.15s;
}

.error-close:hover {
  opacity: 1;
}

.login-btn {
  margin-top: 20px;
  height: 48px;
  font-size: 16px;
  letter-spacing: 4px;
  font-weight: 600;
  background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
  border: none !important;
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.login-btn:active {
  transform: translateY(0);
}

.footer-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #475569;
  font-size: 12px;
  margin-top: 24px;
  letter-spacing: 1px;
}

.github-link {
  display: inline-flex;
  align-items: center;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.9;
}

.github-icon {
  width: 20px;
  height: 20px;
}
</style>
