import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, func
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    restaurant_name = Column(String(150), nullable=False, index=True)
    owner_name = Column(String(100), nullable=False)
    owner_email = Column(String(255), nullable=False, index=True)
    owner_phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)

    restaurant_phone = Column(String(20), nullable=False)
    cuisine_types = Column(String(255), nullable=True)

    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    opening_time = Column(String(20), nullable=True)
    closing_time = Column(String(20), nullable=True)

    gst_number = Column(String(50), nullable=True)
    fssai_number = Column(String(50), nullable=True)

    logo_url = Column(String(255), nullable=True)

    is_draft = Column(Boolean, default=True)
    status = Column(String(20), nullable=False, default="pending")
    is_active = Column(Boolean, nullable=False, default=False)

    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)

    bank_account_holder = Column(String(150), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)

    gst_certificate = Column(String(255), nullable=True)
    fssai_license_file = Column(String(255), nullable=True)
    cancelled_cheque = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())