from sqlalchemy.ext.asyncio import AsyncSession


class NotificationService:

    @staticmethod
    async def create_notification(
        db: AsyncSession,
        data
    ):
        # Placeholder implementation: save notification data
        return {
            "notification_id": None,
            "title": data.title,
            "message": data.message,
            "user_id": data.user_id,
            "status": "created"
        }

    @staticmethod
    async def get_notifications(
        db: AsyncSession,
        user_id: str
    ):
        # Placeholder implementation: return an empty list
        return []
