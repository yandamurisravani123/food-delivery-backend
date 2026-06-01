from sqlalchemy import (
    Column,
    Integer,
    String
)

from app.config.database import Base





import uuid

from sqlalchemy import (
    Float,
    Boolean
)

from sqlalchemy.dialects.postgresql import UUID


class Filter(Base):

    __tablename__ = "filters"

   
    
    

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

  
    
    title = Column(String)

    
    cuisine = Column(
        String(100),
        nullable=True
    )

    rating = Column(
        Float,
        nullable=True
    )

    delivery_time = Column(
        String(50),
        nullable=True
    )

    is_offer_available = Column(
        Boolean,
        default=False
    )