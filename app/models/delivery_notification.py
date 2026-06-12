import uuid
from datetime import datetime

from sqlalchemy import (
    UUID,
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import mapped_column, relationship

from app.config.database import Base


class DeliveryNotification(Base):
    __tablename__ = "delivery_notifications"

    notification_id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True
    )
    order_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    order = relationship("Order", back_populates="notifications")