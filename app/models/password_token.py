import uuid
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from app.config.database import Base


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    entity_type = mapped_column(String(30), nullable=False)   # user / restaurant / delivery_agent
    entity_id = mapped_column(UUID(as_uuid=True), nullable=False, index=True)

    token_hash = mapped_column(String(64), nullable=False, index=True)
    expires_at = mapped_column(DateTime(timezone=True), nullable=False)

    is_used = mapped_column(Boolean, nullable=False, default=False)
    used_at = mapped_column(DateTime(timezone=True), nullable=True)

    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())