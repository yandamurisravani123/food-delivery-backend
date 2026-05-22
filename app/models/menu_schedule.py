from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
import uuid


class MenuSchedule(Base):

    __tablename__ = "menu_schedules"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    menu_item_id = Column(
        UUID(as_uuid=True),
        ForeignKey("menu_items.id")
    )

    day_of_week = Column(String(20))

    start_time = Column(String(20))

    end_time = Column(String(20))

    service_name = Column(String(100))