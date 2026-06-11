import uuid

from sqlalchemy import (
    Column,
    String,
    Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class DeliveryNotification(Base):

    __tablename__ = "delivery_notification"

    notification_id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    order_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False
    )

    title = mapped_column(
        String,
        nullable=False
    )

    message = mapped_column(
        String,
        nullable=False
    )

    notification_type = mapped_column(
        String,
        default="delivery_update"
    )
    # delivery_update
    # arrived
    # preparing
    # out_for_delivery
    # delivered

    is_read = mapped_column(
        Boolean,
        default=False
    )