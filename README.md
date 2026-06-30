# Whisper Tools 🎙️

个人语音转文本工具站 —— 通过 Web 上传音频，利用远端 GPU 机器运行 Whisper 转写，再经 LLM 矫正总结后邮件发送报告。

## 架构概览

```.
用户上传音频 → Web 前端 → FastAPI 后端
    ↓
Syncthing 同步文件夹 (服务器端)
    ↓ (自动同步)
Syncthing 同步文件夹 (Windows 游戏本)
    ↓ (Watchdog 监听)
Whisper 转写 → 结果写回同步文件夹
    ↓ (自动同步回服务器)
FastAPI 调用 DeepSeek API 矫正 + 总结
    ↓
邮件发送报告
```

## 项目结构

```.
whisper-tools/
├── web/               # 前端 (Vue 3 + Vite + Naive UI)
├── server/            # 后端 (FastAPI)
├── windows-agent/     # Windows 端 (Whisper 转写守护程序)
└── deploy/            # 部署配置
```

## 快速开始

### 1. 后端

```bash
cd server
cp .env.example .env   # 编辑 .env 填入你的配置
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. 前端

```bash
cd web
npm install
npm run dev           # 开发模式
npm run build         # 构建生产版本
```

### 3. Windows 端

```bash
cd windows-agent
pip install -r requirements.txt
python whisper_watcher.py
```

## 配置说明

所有敏感信息通过 `.env` 文件管理，参考 `server/.env.example`。

| 配置项 | 说明 |
| ------ | ---- |
| `APP_PASSWORD` | Web 登录密码 |
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 |
| `SMTP_*` | 邮件发送配置 |
| `MAIL_TO` | 报告接收邮箱 |

## 技术栈

- **前端**: Vue 3 + Vite + Naive UI + Pinia + Vue Router
- **后端**: FastAPI + SQLite + DeepSeek API
- **Windows 端**: Python + Watchdog + Whisper (openai-whisper)
- **同步**: Syncthing
