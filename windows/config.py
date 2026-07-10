import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    # 认证
    app_password: str = ""
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 720  # 30 天

    # Cherry Studio API
    cherry_studio_url: str = "http://localhost:8002/v1"
    cherry_model: str = "default"

    # SMTP 邮件
    smtp_host: str = ""
    smtp_port: int = 465
    smtp_user: str = ""
    smtp_pass: str = ""
    mail_to: str = ""

    # 路径
    upload_dir: str = str(BASE_DIR / "uploads")
    archive_dir: str = "D:\\whisper-archive"
    db_path: str = str(BASE_DIR / "whisper_tools.db")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

# 确保必要目录存在
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.archive_dir, exist_ok=True)
