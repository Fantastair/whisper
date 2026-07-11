from fastapi import APIRouter, Depends, HTTPException

from windows.models.database import get_db
from windows.models.schemas import TaskDetailOut, TaskOut
from windows.routers.auth import require_auth

router = APIRouter(prefix="/api/tasks", tags=["任务"])


@router.get("", response_model=list[TaskOut])
async def list_tasks(
    db=Depends(get_db),
    _=Depends(require_auth),
):
    """获取所有任务列表，按创建时间倒序。"""
    async with db.execute(
        "SELECT id, filename, original_name, file_type, status, file_size,"
        " created_at, updated_at FROM tasks ORDER BY created_at DESC"
    ) as cursor:
        rows = await cursor.fetchall()
    return [dict(r) for r in rows]


@router.get("/{task_id}", response_model=TaskDetailOut)
async def get_task(
    task_id: str,
    db=Depends(get_db),
    _=Depends(require_auth),
):
    """获取单个任务的详细信息。"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="任务不存在")
    return dict(row)


@router.post("/{task_id}/retry")
async def retry_task(
    task_id: str,
    db=Depends(get_db),
    _=Depends(require_auth),
):
    """重试失败的任务，将状态重置为 pending。"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="任务不存在")
    if row["status"] != "failed":
        raise HTTPException(status_code=400, detail="只有失败的任务可以重试")

    await db.execute(
        "UPDATE tasks SET status = ?, error_message = NULL WHERE id = ?",
        ("pending", task_id),
    )
    await db.commit()
    return {"detail": "任务已重置为 pending"}


@router.post("/{task_id}/resend-email")
async def resend_email(
    task_id: str,
    db=Depends(get_db),
    _=Depends(require_auth),
):
    """重新发送邮件（将 emailed 状态重置为 completed 触发重新发送）。"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="任务不存在")
    if row["status"] != "emailed":
        raise HTTPException(status_code=400, detail="只有已发送邮件的任务可以重新发送")

    await db.execute(
        "UPDATE tasks SET status = ?, email_sent = 0 WHERE id = ?",
        ("completed", task_id),
    )
    await db.commit()
    return {"detail": "任务已重置为 completed，Agent 将重新发送邮件"}


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    db=Depends(get_db),
    _=Depends(require_auth),
):
    """删除任务记录。"""
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="任务不存在")

    await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await db.commit()
    return {"detail": "任务已删除"}
