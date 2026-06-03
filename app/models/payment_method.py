from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    payment_type = Column(
        String,
        nullable=False
    )

    provider_name = Column(
        String,
        nullable=False
    )

    upi_id = Column(
        String,
        nullable=True
    )

    card_holder_name = Column(
        String,
        nullable=True
    )

    card_number = Column(
        String,
        nullable=True
    )

    expiry_month = Column(
        Integer,
        nullable=True
    )

    expiry_year = Column(
        Integer,
        nullable=True
    )

    wallet_number = Column(
        String,
        nullable=True
    )

    is_default = Column(
        Boolean,
        default=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    user = relationship("User")