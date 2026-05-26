import uuid
import enum

from sqlalchemy import (
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class PaymentMethod(str, enum.Enum):
    COD = "COD"
    UPI = "UPI"
    CARD = "CARD"
    WALLET = "WALLET"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payment_methods"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # users.id is UUID
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    # orders.id is Integer
    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    payment_method = Column(
        Enum(PaymentMethod),
        nullable=False
    )

    payment_status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING
    )

    amount = Column(
        Float,
        nullable=False
    )