from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from app.config.database import Base


class DeliveryNotification(Base):

    __tablename__ = "delivery_notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    notification_type = Column(
        String,
        default="delivery_update"
    )
    # delivery_update
    # arrived
    # preparing
    # out_for_delivery
    # delivered

    is_read = Column(
        Boolean,
        default=False
    )