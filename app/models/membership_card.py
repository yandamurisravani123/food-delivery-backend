from uuid import uuid4
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class Membership(Base):
    __tablename__ = "memberships"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    member_code = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    plan_name = mapped_column(
        String,
        default="Premium"
    )

    is_active = mapped_column(
        Boolean,
        default=True
    )

    member_since = mapped_column(
        DateTime,
        server_default=func.now()
    )

    next_billing_date = mapped_column(
        DateTime,
        nullable=True
    )

    created_at = mapped_column(
        DateTime,
        server_default=func.now()
    )