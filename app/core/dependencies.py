from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.config.security import token_fingerprint
from app.config.settings import settings
from app.core.redis_client import redis_client
from app.repositories.auth_repository import AuthRepository
from app.models.user import User

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    token_key = f"blacklist:{token_fingerprint(token)}"
    if await redis_client.get(token_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been logged out",
        )

    user_id = payload.get("sub")
    entity_type = payload.get("entity_type")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    if entity_type == "user":
        user = await AuthRepository.get_user_by_id(session, UUID(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user

    if entity_type == "restaurant":
        restaurant = await AuthRepository.get_restaurant_by_id(session, UUID(user_id))
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Restaurant not found",
            )
        return restaurant

    if entity_type == "delivery_agent":
        delivery_agent = await AuthRepository.get_delivery_agent_by_id(session, UUID(user_id))
        if not delivery_agent:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Delivery agent not found",
            )
        return delivery_agent

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token entity type",
    )


async def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access only",
        )
    return current_user