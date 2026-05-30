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


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    reward_name = mapped_column(
        String,
        nullable=False
    )

    points_used = mapped_column(
        Integer,
        nullable=False
    )

    status = mapped_column(
        String,
        default="REDEEMED"
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )