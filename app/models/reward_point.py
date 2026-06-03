from uuid import uuid4

from sqlalchemy import (
    Integer,
    DateTime,
    func
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class RewardPoint(Base):
    __tablename__ = "reward_points"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True
    )

    current_points = mapped_column(
        Integer,
        default=0
    )

    target_points = mapped_column(
        Integer,
        default=5000
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )