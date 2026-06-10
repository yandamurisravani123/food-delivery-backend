from uuid import UUID
import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from app.config.database import Base
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
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
        Integer,
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