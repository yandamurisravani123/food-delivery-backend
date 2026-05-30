from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.notification_repository import (
    NotificationRepository
)


class NotificationService:

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        data
    ):

        return await NotificationRepository.create_notification(
            db,
            data.dict()
        )


    @staticmethod
    async def get_notifications(
        db: AsyncSession,
        user_id
    ):

        return await NotificationRepository.get_user_notifications(
            db,
            user_id
        )