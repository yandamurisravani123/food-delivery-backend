import uuid

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    func,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, Integer

from app.config.database import Base


class OrderTracking(Base):
    __tablename__ = "order_tracking"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

<<<<<<< HEAD
    order_id = mapped_column(Integer, nullable=False)

=======
    order_id = Column(Integer, nullable=False)
>>>>>>> 81a7d48d016c94dcee7c2e99ad3bb275aa433dca

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