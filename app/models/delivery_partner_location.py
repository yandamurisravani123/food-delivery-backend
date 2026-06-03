import uuid

from sqlalchemy import (
    Float,
    DateTime,
    func
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import mapped_column

from app.config.database import Base


class DeliveryPartnerLocation(Base):
    __tablename__ = "delivery_partner_locations"

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

    latitude = mapped_column(
        Float,
        nullable=False
    )

    longitude = mapped_column(
        Float,
        nullable=False
    )

    updated_at = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )