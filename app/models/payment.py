from sqlalchemy import Column, String, Float, DateTime,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

import uuid

from app.config.database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id = Column(Integer, nullable=False)

    user_id = Column(UUID(as_uuid=True), nullable=False)

    payment_method = Column(String, nullable=False)

    payment_status = Column(String, default="SUCCESS")

    amount = Column(Float, nullable=False)

    transaction_id = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )