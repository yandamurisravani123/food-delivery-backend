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


class RewardTransaction(Base):
    __tablename__ = "reward_transactions"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    points = mapped_column(
        Integer,
        nullable=False
    )

    transaction_type = mapped_column(
        String,
        nullable=False
    )  # EARNED / REDEEMED

    description = mapped_column(
        String,
        nullable=False
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )