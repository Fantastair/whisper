from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # 认证
    app_password: str = ""

    # LLM (DeepSeek)
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"

    # 邮件
    smtp_host: str = ""
    smtp_port: int = 465
    smtp_user: str = ""
    smtp_pass: str = ""
    mail_to: str = ""

    # Syncthing
    sync_audio_dir: str = "./sync_folder/audio"
    sync_results_dir: str = "./sync_folder/results"

    # JWT
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 720  # 30 天

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

# 确保同步目录存在
os.makedirs(settings.sync_audio_dir, exist_ok=True)
os.makedirs(settings.sync_results_dir, exist_ok=True)
