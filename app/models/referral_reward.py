from uuid import uuid4

from sqlalchemy import (
    Integer,
    DateTime,
    func
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class ReferralReward(Base):
    __tablename__ = "referral_rewards"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    referrer_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    referred_user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    points_awarded = mapped_column(
        Integer,
        default=500
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )