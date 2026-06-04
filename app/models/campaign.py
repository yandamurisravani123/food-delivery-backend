from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Text
)
from sqlalchemy import Enum as PgEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.config.database import Base
from app.utils.enums import CampaignType, CampaignStatus
 
 
class Campaign(Base):
    __tablename__ = "campaigns"
 
    id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
    index=True
)
 
    restaurant_id = Column(
    UUID(as_uuid=True),
    ForeignKey("restaurants.id")
)
    title = Column(String(255), nullable=False)
 
    description = Column(Text)
 
    campaign_type = Column(
    PgEnum(CampaignType, name="campaign_type_enum"),
    nullable=False
)
 
    status = Column(
    PgEnum(CampaignStatus, name="campaign_status_enum"),
    default=CampaignStatus.SCHEDULED
)
    discount_percentage = Column(Float, nullable=True)
 
    target_customers = Column(Integer, default=0)
 
    reach_count = Column(Integer, default=0)
 
    clicks = Column(Integer, default=0)
 
    orders = Column(Integer, default=0)
 
    revenue_generated = Column(Float, default=0)
 
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
 
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    is_active = Column(Boolean, default=True)
 
    total_budget = Column(Float, default=0)
    daily_budget = Column(Float, default=0)
 
    smart_bidding = Column(Boolean, default=False)
 
    restaurant = relationship("Restaurant")
 
 
 
 
class FlashOffer(Base):
    __tablename__ = "flash_offers"
 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
 
    title = Column(String)
 
    start_time = Column(String)
    end_time = Column(String)
 
    surge_multiplier = Column(Float)
 
    free_delivery = Column(Boolean, default=False)
 
    is_active = Column(Boolean, default=True)
 
 
 
class OfferControl(Base):
 
    __tablename__ = "offer_controls"
 
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
 
    auto_apply = Column(
        Boolean,
        default=False
    )
 
    minimum_discount = Column(
        Float,
        default=0
    )
 
 
 
class KeywordBid(Base):
    __tablename__ = "keyword_bids"
 
    id = Column(Integer, primary_key=True)
 
    campaign_id = Column(
    UUID(as_uuid=True),
    ForeignKey("campaigns.id")
    )
 
    keyword = Column(String)   # "Italian Pasta"
    category = Column(String)  # "Healthy Bowls"
 
    current_bid = Column(Float, default=0.5)
    suggested_bid = Column(Float, default=1.0)
 
    views = Column(Integer, default=0)
    rank = Column(Integer, default=0)
 
 
class Banner(Base):
    __tablename__ = "banners"
 
    id = Column(Integer, primary_key=True)
    campaign_id = Column(
    UUID(as_uuid=True),
    ForeignKey("campaigns.id")
    )
 
    image_url = Column(String)
    target_url = Column(String)
 
    start_date = Column(String)
    end_date = Column(String)
 
    status = Column(String, default="PENDING")
 
 
 
class Budget(Base):
    __tablename__ = "budgets"
 
    id = Column(Integer, primary_key=True)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"))
 
    daily_limit = Column(Float, default=0)
    total_budget = Column(Float, default=0)
    spent = Column(Float, default=0)
 
 
class AuditLog(Base):
    __tablename__ = "audit_logs"
 
    id = Column(Integer, primary_key=True)
 
    campaign_id = Column(ForeignKey("campaigns.id"))
 
    action = Column(String)
 
    created_at = Column(DateTime)