# app/models/savings.py

import uuid

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.config.database import Base


class UserSavings(Base):
    __tablename__ = "user_savings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
    )

    total_saved = Column(Float, default=0.0)

    delivery_fee_saved = Column(Float, default=0.0)
    discount_saved = Column(Float, default=0.0)
    wallet_credit_saved = Column(Float, default=0.0)

    monthly_goal = Column(Float, default=100.0)
    monthly_saved = Column(Float, default=0.0)

    tier = Column(String, default="Silver")
    percentile = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())