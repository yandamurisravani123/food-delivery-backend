from uuid import uuid4
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class MembershipBenefit(Base):
    __tablename__ = "membership_benefits"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    title = mapped_column(String)

    description = mapped_column(String)