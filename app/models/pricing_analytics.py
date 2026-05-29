from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from sqlalchemy.sql import func
import uuid


class PricingAnalytics(Base):

    __tablename__ = "pricing_analytics"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    increase_percentage = Column(Float)

    message = Column(String(500))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )