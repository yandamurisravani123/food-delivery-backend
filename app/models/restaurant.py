import uuid

from typing import Optional
from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Float
)

from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Restaurant(Base):

    __tablename__ = "restaurants"

    
    # Primary Key
   
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

   
    # Basic Restaurant Details
    
    restaurant_name = Column(
        String(150),
        nullable=False,
        index=True
    )
logo_url = Column(
    String(255),
    nullable=True
)


    cuisine_types = Column(
        String(255),
        nullable=True
    )

    
    # Owner Details
   

    owner_name = Column(
        String(100),
        nullable=False
    )

    owner_email = Column(
        String(255),
        nullable=False,
        unique=True,
        index=True
    )

    owner_phone = Column(
        String(20),
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    
    # Restaurant Contact


    restaurant_phone = Column(
        String(20),
        nullable=False
    )

    
    # Address Details
    

    address_line1 = Column(
        String(255),
        nullable=False
    )

    address_line2 = Column(
        String(255),
        nullable=True
    )

    city = Column(
        String(100),
        nullable=False,
        index=True
    )

    state = Column(
        String(100),
        nullable=False
    )

    pincode = Column(
        String(20),
        nullable=False
    )

   
    # Geo Location
    

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )

    
    # Restaurant Timings
    

    opening_time = Column(
        String(20),
        nullable=True
    )

    closing_time = Column(
        String(20),
        nullable=True
    )

    
    # Legal Details
  

    gst_number = Column(
        String(50),
        nullable=True
    )

    fssai_number = Column(
        String(50),
        nullable=True
    )

   
    # Restaurant Status
    

    status = Column(
        String(20),
        nullable=False,
        default="pending"
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=False
    )

    
    # Home Page Flags

    is_trending = Column(
        Boolean,
        nullable=False,
        default=False
    )

    is_top_rated = Column(
        Boolean,
        nullable=False,
        default=False
    )

    approved_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True
    )

    approved_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # Timestamps
    

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )