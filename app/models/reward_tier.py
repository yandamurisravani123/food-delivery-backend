from uuid import uuid4

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    func
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class RewardTier(Base):
    __tablename__ = "reward_tiers"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    tier_name = mapped_column(
        String,
        nullable=False,
        unique=True
    )

    min_points = mapped_column(
        Integer,
        nullable=False
    )

    max_points = mapped_column(
        Integer,
        nullable=False
    )

    reward_amount = mapped_column(
        Integer,
        nullable=False
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )