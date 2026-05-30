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
<<<<<<< HEAD


class Campaign(Base):
    __tablename__ = "campaigns"

=======
 
 
class Campaign(Base):
    __tablename__ = "campaigns"
 
>>>>>>> 6da5f03 (testing)
    id = Column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
    index=True
)
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    restaurant_id = Column(
    UUID(as_uuid=True),
    ForeignKey("restaurants.id")
)
    title = Column(String(255), nullable=False)
<<<<<<< HEAD

    description = Column(Text)

=======
 
    description = Column(Text)
 
>>>>>>> 6da5f03 (testing)
    campaign_type = Column(
    PgEnum(CampaignType, name="campaign_type_enum"),
    nullable=False
)
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    status = Column(
    PgEnum(CampaignStatus, name="campaign_status_enum"),
    default=CampaignStatus.SCHEDULED
)
    discount_percentage = Column(Float, nullable=True)
<<<<<<< HEAD

    target_customers = Column(Integer, default=0)

    reach_count = Column(Integer, default=0)

    clicks = Column(Integer, default=0)

    orders = Column(Integer, default=0)

    revenue_generated = Column(Float, default=0)

=======
 
    target_customers = Column(Integer, default=0)
 
    reach_count = Column(Integer, default=0)
 
    clicks = Column(Integer, default=0)
 
    orders = Column(Integer, default=0)
 
    revenue_generated = Column(Float, default=0)
 
>>>>>>> 6da5f03 (testing)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    is_active = Column(Boolean, default=True)
<<<<<<< HEAD

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

=======
 
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
 
>>>>>>> 6da5f03 (testing)
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    auto_apply = Column(
        Boolean,
        default=False
    )
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
    minimum_discount = Column(
        Float,
        default=0
    )
<<<<<<< HEAD



class KeywordBid(Base):
    __tablename__ = "keyword_bids"

    id = Column(Integer, primary_key=True)

=======
 
 
 
class KeywordBid(Base):
    __tablename__ = "keyword_bids"
 
    id = Column(Integer, primary_key=True)
 
>>>>>>> 6da5f03 (testing)
    campaign_id = Column(
    UUID(as_uuid=True),
    ForeignKey("campaigns.id")
    )
<<<<<<< HEAD

    keyword = Column(String)   # "Italian Pasta"
    category = Column(String)  # "Healthy Bowls"

    current_bid = Column(Float, default=0.5)
    suggested_bid = Column(Float, default=1.0)

    views = Column(Integer, default=0)
    rank = Column(Integer, default=0)


class Banner(Base):
    __tablename__ = "banners"

=======
 
    keyword = Column(String)   # "Italian Pasta"
    category = Column(String)  # "Healthy Bowls"
 
    current_bid = Column(Float, default=0.5)
    suggested_bid = Column(Float, default=1.0)
 
    views = Column(Integer, default=0)
    rank = Column(Integer, default=0)
 
 
class Banner(Base):
    __tablename__ = "banners"
 
>>>>>>> 6da5f03 (testing)
    id = Column(Integer, primary_key=True)
    campaign_id = Column(
    UUID(as_uuid=True),
    ForeignKey("campaigns.id")
    )
<<<<<<< HEAD

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

=======
 
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
 
>>>>>>> 6da5f03 (testing)
    created_at = Column(DateTime)