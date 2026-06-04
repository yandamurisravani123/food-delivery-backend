from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.config.database import Base


class OrderPreparation(Base):
    __tablename__ = "order_preparations"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), unique=True)

    current_stage = Column(String, default="ORDER_RECEIVED")
    progress_percent = Column(Integer, default=0)

    estimated_ready_time = Column(DateTime, nullable=True)
    chef_note = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)