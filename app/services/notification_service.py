from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.notifications import Notification
from app.schemas.notification import NotificationCreateSchema


class NotificationService:

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        data: NotificationCreateSchema
    ) -> Notification:

        notification = Notification(
            user_id=data.user_id,
            title=data.title,
            message=data.message,
            notification_type=data.notification_type
        )

        db.add(notification)
        await db.commit()
        await db.refresh(notification)

        return notification

    @staticmethod
    async def get_notifications(
        db: AsyncSession,
        user_id: str
    ) -> list:

        result = await db.execute(
            select(Notification).where(
                Notification.user_id == user_id
            ).order_by(Notification.created_at.desc())
        )

        return result.scalars().all()