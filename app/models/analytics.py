import uuid

from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class CampaignAnalytics(Base):
    __tablename__ = "campaign_analytics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    orders = Column(Integer, default=0)
    revenue = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())