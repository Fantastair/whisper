from fastapi import APIRouter, Depends
from app.models.database import get_db
from app.models.schemas import TaskOut, TaskDetailOut
from app.routers.upload import require_auth

router = APIRouter(prefix="/api/tasks", tags=["任务"])


@router.get("", response_model=list[TaskOut])
async def list_tasks(
    db=Depends(get_db),
    _=Depends(require_auth),
):
    async with db.execute(
        "SELECT id, filename, status, created_at, updated_at FROM tasks ORDER BY created_at DESC"
    ) as cursor:
        rows = await cursor.fetchall()
    return [dict(r) for r in rows]


@router.get("/{task_id}", response_model=TaskDetailOut)
async def get_task(
    task_id: str,
    db=Depends(get_db),
    _=Depends(require_auth),
):
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cursor:
        row = await cursor.fetchone()
    if not row:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="任务不存在")
    return dict(row)
