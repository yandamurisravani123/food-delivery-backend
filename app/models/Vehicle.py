import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    driver_id = Column(
    UUID(as_uuid=True),
    ForeignKey("delivery_agents.id"),   
    nullable=False
   )
    vehicle_type = Column(String)
    registration_number = Column(String)

    rc_front_url = Column(String)
    rc_back_url = Column(String)

    insurance_url = Column(String)
    vehicle_photo_url = Column(String)

    status = Column(String, default="not_submitted")
    
    status = Column(String, default="pending")