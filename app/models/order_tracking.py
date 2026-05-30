import uuid

from sqlalchemy import (
    String,
    DateTime,
    func,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import mapped_column

from app.config.database import Base


class OrderTracking(Base):
    __tablename__ = "order_tracking"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    delivery_partner_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    status = mapped_column(
        String,
        nullable=False
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )