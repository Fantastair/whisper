from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Header, HTTPException
from jose import JWTError, jwt

from windows.config import settings
from windows.models.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["认证"])


def create_token() -> str:
    """生成 JWT Token。"""
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expire_hours)
    payload = {"exp": expire, "sub": "admin"}
    secret = settings.jwt_secret or settings.app_password
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


def verify_token(token: str) -> bool:
    """验证 JWT Token 是否有效。"""
    try:
        secret = settings.jwt_secret or settings.app_password
        jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
        return True
    except JWTError:
        return False


async def require_auth(authorization: str = Header(None)) -> None:
    """依赖项：要求请求携带有效的 JWT Token。"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录")
    token = authorization.removeprefix("Bearer ")
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="登录已过期")


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    """密码登录，返回 JWT Token。"""
    if body.password != settings.app_password:
        raise HTTPException(status_code=401, detail="密码错误")
    return TokenResponse(token=create_token())
