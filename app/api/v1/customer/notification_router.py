from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.schemas.notification import (
    NotificationCreateSchema,
    NotificationResponseSchema
)
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.post(
    "/create",
    response_model=NotificationResponseSchema
)
async def create_notification(
    data: NotificationCreateSchema,
    db: AsyncSession = Depends(get_db)
):
    return await NotificationService.create_notification(
        db,
        data
    )

@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponseSchema]
)
async def get_notifications(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    return await NotificationService.get_notifications(
        db,
        user_id
    )