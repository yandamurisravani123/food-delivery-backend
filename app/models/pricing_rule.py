from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid


class PricingRule(Base):

    __tablename__ = "pricing_rules"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    menu_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.id")
    )

    rule_name = Column(String(255), nullable=False)

    adjustment_type = Column(String(50))  
    # percentage / fixed

    adjustment_value = Column(Float)

    start_date = Column(String(50))

    end_date = Column(String(50))

    active_days = Column(String(100), nullable=True)

    is_active = Column(Boolean, default=True)