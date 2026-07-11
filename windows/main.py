"""轻语 Windows 端 FastAPI 后端入口。"""

import subprocess
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from windows.config import settings
from windows.routers import auth, tasks, upload

_frpc_process: subprocess.Popen | None = None


def _start_frpc() -> subprocess.Popen | None:
    """启动 frp 客户端隧道。"""
    if not settings.frpc_enabled:
        print("[frpc] 未启用，跳过")
        return None
    if not settings.frpc_bin or not settings.frpc_config:
        print("[frpc] 已启用但未配置二进制路径或配置文件，跳过")
        return None

    from pathlib import Path

    from windows.config import BASE_DIR

    bin_path = Path(settings.frpc_bin)
    cfg_path = Path(settings.frpc_config)
    if not bin_path.is_absolute():
        bin_path = BASE_DIR.parent / bin_path
    if not cfg_path.is_absolute():
        cfg_path = BASE_DIR.parent / cfg_path

    try:
        proc = subprocess.Popen(
            [str(bin_path), "-c", str(cfg_path)],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        print(f"[frpc] 已启动 (PID={proc.pid})")
        return proc
    except FileNotFoundError:
        print(f"[frpc] 未找到二进制文件: {bin_path}")
        return None


def _stop_frpc(proc: subprocess.Popen | None) -> None:
    """停止 frp 客户端。"""
    if proc is None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
        print(f"[frpc] 已停止 (PID={proc.pid})")
    except TimeoutError:
        proc.kill()
        print(f"[frpc] 已强制终止 (PID={proc.pid})")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化数据库，启动 frp 隧道。"""
    from windows.models.database import get_db

    db = await get_db()
    await db.close()

    global _frpc_process
    _frpc_process = _start_frpc()
    yield
    _stop_frpc(_frpc_process)


app = FastAPI(
    title="轻语 API",
    description="语音/视频转文本工具后端 — Windows 端",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS：开发时前端独立端口需要
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(tasks.router)


@app.get("/api/health")
def health():
    """健康检查接口。"""
    return {"status": "ok"}
