from sqlalchemy import (
    Column,
    Integer,
    String,
    Float
)

from app.config.database import Base


class DeliveryPartner(Base):

    __tablename__ = "delivery_partners"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    phone = Column(String)

    vehicle_type = Column(String)

    vehicle_number = Column(String)

    current_latitude = Column(Float)

    current_longitude = Column(Float)

    availability_status = Column(
        String,
        default="AVAILABLE"
    )