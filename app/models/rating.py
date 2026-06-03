import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())