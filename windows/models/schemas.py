from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    password: str


class TokenResponse(BaseModel):
    token: str


class TaskOut(BaseModel):
    id: str
    filename: str
    original_name: str
    file_type: str
    status: str
    file_size: Optional[int] = None
    created_at: str
    updated_at: str


class TaskDetailOut(TaskOut):
    transcript: Optional[str] = None
    corrected_text: Optional[str] = None
    summary: Optional[str] = None
    report: Optional[str] = None
    error_message: Optional[str] = None
    email_sent: bool = False


class UploadResponse(BaseModel):
    task_id: str
    filename: str
