from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

from app.config.settings import settings


def create_access_token(subject: str, role: str, user_id: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    payload: Dict[str, Any] = {
        "sub": subject,
        "user_id": user_id,
        "role": role,
        "type": "access",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


def verify_token(token: str) -> dict:
    try:
        payload = decode_access_token(token)
        if payload.get("type") != "access":
            raise ValueError("Invalid token type")
        return payload
    except (JWTError, ValueError) as exc:
        raise ValueError("Could not validate token") from exc
