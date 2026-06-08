from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.user import User


async def require_role(role: str):
    async def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to {role} role",
            )
        return current_user
    return _checker


async def require_restaurant(current_user=Depends(get_current_user)):
    from app.models.restaurant import Restaurant
    if not isinstance(current_user, Restaurant):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Restaurant access only",
        )
    return current_user


async def require_customer(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access only",
        )
    return current_user