import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Address(Base):

    __tablename__ = "addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    label = Column(String(100), nullable=True)

    address_line1 = Column(String(255), nullable=False)

    address_line2 = Column(String(255), nullable=True)

    city = Column(String(100), nullable=True)

    state = Column(String(100), nullable=True)

    pincode = Column(String(20), nullable=True)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    is_default = Column(Boolean, default=False)
