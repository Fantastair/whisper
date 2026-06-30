import uuid
import os
from fastapi import APIRouter, UploadFile, File, Depends
from app.config import settings
from app.models.database import get_db
from app.models.schemas import UploadResponse
from app.routers.auth import verify_token
from fastapi import Header, HTTPException

router = APIRouter(prefix="/api", tags=["上传"])


async def require_auth(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录")
    token = authorization.removeprefix("Bearer ")
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="登录已过期")


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    db=Depends(get_db),
    _=Depends(require_auth),
):
    task_id = uuid.uuid4().hex[:12]
    # 保留原始扩展名
    ext = os.path.splitext(file.filename or ".audio")[1] or ".audio"
    safe_name = f"{task_id}{ext}"

    # 保存到 Syncthing 同步目录
    file_path = os.path.join(settings.sync_audio_dir, safe_name)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 创建任务记录
    await db.execute(
        "INSERT INTO tasks (id, filename, original_name, status) VALUES (?, ?, ?, ?)",
        (task_id, safe_name, file.filename or safe_name, "pending"),
    )
    await db.commit()

    return UploadResponse(task_id=task_id, filename=file.filename or safe_name)
