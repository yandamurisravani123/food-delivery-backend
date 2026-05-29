from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid


class CustomizationGroup(Base):

    __tablename__ = "customization_groups"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    restaurant_id = Column(
        UUID(as_uuid=True),
        ForeignKey("restaurants.id")
    )

    group_name = Column(String(255), nullable=False)

class CustomizationOption(Base):

    __tablename__ = "customization_options"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customization_groups.id")
    )

    option_name = Column(String(255), nullable=False)

    extra_price = Column(Float, default=0)