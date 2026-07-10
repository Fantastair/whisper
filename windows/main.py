"""轻语 Windows 端 FastAPI 后端入口。"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from windows.routers import auth, tasks, upload


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化数据库。"""
    from windows.models.database import get_db

    db = await get_db()
    await db.close()
    yield


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
