from uuid import UUID

from datetime import datetime

from pydantic import BaseModel


class NotificationCreateSchema(BaseModel):

    user_id: UUID

    title: str

    message: str

    notification_type: str


class NotificationResponseSchema(BaseModel):

    id: UUID

    user_id: UUID

    title: str

    message: str

    notification_type: str

    is_read: bool

    created_at: datetime

    class Config:
        from_attributes = True