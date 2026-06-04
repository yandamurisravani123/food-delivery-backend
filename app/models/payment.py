import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), nullable=True)

    user_id = Column(UUID(as_uuid=True), nullable=True)

    amount = Column(Float, nullable=False, default=0.0)

    status = Column(String(50), nullable=False, default="pending")

    payment_method = Column(String(100), nullable=True)

    transaction_id = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
