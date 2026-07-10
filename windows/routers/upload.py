import os
import uuid

from fastapi import APIRouter, Depends, File, UploadFile

from windows.config import settings
from windows.models.database import get_db
from windows.models.schemas import UploadResponse
from windows.routers.auth import require_auth

router = APIRouter(prefix="/api", tags=["上传"])


@router.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    db=Depends(get_db),
    _=Depends(require_auth),
):
    """上传音频或视频文件，创建任务记录。"""
    task_id = uuid.uuid4().hex[:12]

    # 保留原始扩展名
    original_name = file.filename or "unknown"
    ext = os.path.splitext(original_name)[1] or ".bin"
    safe_name = f"{task_id}{ext}"

    # 保存文件到上传目录
    file_path = os.path.join(settings.upload_dir, safe_name)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 判断文件类型
    file_type = (
        "video"
        if ext.lower() in (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm")
        else "audio"
    )

    # 创建任务记录
    await db.execute(
        "INSERT INTO tasks (id, filename, original_name, file_type, status,"
        " file_size) VALUES (?, ?, ?, ?, ?, ?)",
        (task_id, safe_name, original_name, file_type, "pending", len(content)),
    )
    await db.commit()

    return UploadResponse(task_id=task_id, filename=original_name)
