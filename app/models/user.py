import uuid

from sqlalchemy import UUID, Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column
from app.config.database import Base

class User(Base):
    __tablename__ = "users"
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    full_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="super_admin")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
