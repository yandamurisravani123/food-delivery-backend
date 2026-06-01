from sqlalchemy import select
 
from sqlalchemy.ext.asyncio import AsyncSession
 
from app.models.notification import Notification
 
 
class NotificationRepository:
 
    @staticmethod
    async def create_notification(
        db: AsyncSession,
        data: dict
    ):
 
        notification = Notification(**data)
 
        db.add(notification)
 
        await db.commit()
 
        await db.refresh(notification)
 
        return notification
 
 
    @staticmethod
    async def get_user_notifications(
        db: AsyncSession,
        user_id
    ):
 
        query = select(Notification).where(
            Notification.user_id == user_id
        )
 
        result = await db.execute(query)
 
        return result.scalars().all()
 