import uuid

from sqlalchemy import UUID, Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import mapped_column
from app.config.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DeliveryAgent(Base):
    __tablename__ = "delivery_agents"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)

    vehicle_type = Column(String(50), nullable=False)
    vehicle_number = Column(String(50), nullable=False)

    driving_license_number = Column(String(100), nullable=False)
    aadhaar_number = Column(String(20), nullable=False)

    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)

    profile_image = Column(String(255), nullable=True)

    status = Column(String(20), nullable=False, default="pending")
    is_active = Column(Boolean, nullable=False, default=False)

    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())