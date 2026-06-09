from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.config.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), nullable=False)

    amount = Column(Float, nullable=False)

    payment_method = Column(String, nullable=False)

    status = Column(String, default="Pending")