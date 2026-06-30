from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from datetime import datetime, timedelta
from app.config import settings
from app.models.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["认证"])


def create_token() -> str:
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_expire_hours)
    payload = {"exp": expire, "sub": "admin"}
    secret = settings.jwt_secret or settings.app_password
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> bool:
    try:
        secret = settings.jwt_secret or settings.app_password
        jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        return True
    except Exception:
        return False


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    if body.password != settings.app_password:
        raise HTTPException(status_code=401, detail="密码错误")
    return TokenResponse(token=create_token())
