from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoginRequest(BaseModel):
    password: str


class TokenResponse(BaseModel):
    token: str


class TaskOut(BaseModel):
    id: str
    filename: str
    status: str
    created_at: str
    updated_at: str


class TaskDetailOut(TaskOut):
    transcript: Optional[str] = None
    corrected_text: Optional[str] = None
    summary: Optional[str] = None
    report: Optional[str] = None


class UploadResponse(BaseModel):
    task_id: str
    filename: str
