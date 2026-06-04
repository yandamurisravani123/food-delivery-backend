from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.config.database import Base


class DeliveryAgent(Base):
    __tablename__ = "delivery_agents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)

    vehicle_type = Column(String(50), nullable=False)
    vehicle_number = Column(String(50), nullable=False)

    driving_license_number = Column(String(100), nullable=False)
    aadhaar_number = Column(String(20), nullable=False)

    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)

    profile_image = Column(String(255))

    # --------------------------
    # AVAILABILITY
    # --------------------------

    is_active = Column(Boolean, default=False)

    is_auto_accept = Column(Boolean, default=False)

    working_radius_km = Column(Integer, default=10)

    accept_cod = Column(Boolean, default=True)

    accept_bulk_orders = Column(Boolean, default=False)

    accept_fragile_items = Column(Boolean, default=True)

    accept_long_distance = Column(Boolean, default=False)

    vehicle_mode = Column(
        String(50),
        default="Electric Scooter"
    )

    # --------------------------
    # BREAK MANAGEMENT
    # --------------------------

    is_on_break = Column(Boolean, default=False)

    today_break_time = Column(
        String,
        default="0m"
    )

    goal_completion = Column(
        Integer,
        default=0
    )

    deliveries_completed = Column(
        Integer,
        default=0
    )

    # --------------------------
    # LICENSE DOCUMENTS
    # --------------------------

    license_front_url = Column(String)

    license_back_url = Column(String)

    is_license_uploaded = Column(
        Boolean,
        default=False
    )

    license_status = Column(
        String,
        default="pending"
    )

    # --------------------------
    # VERIFICATION
    # --------------------------

    verification_status = Column(
        String,
        default="not_submitted"
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    status = Column(
        String(20),
        default="pending"
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

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

# =====================================================
# DRIVER DASHBOARD STATS
# =====================================================


class DriverStats(Base):
    __tablename__ = "driver_stats"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    delivery_agent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("delivery_agents.id"),
        nullable=False
    )

    # Earnings
    today_earnings = Column(Float, default=0)
    estimated_earnings = Column(Float, default=0)

    # Goals
    daily_goal = Column(Float, default=200)
    weekly_hours = Column(Float, default=0)

    # Orders
    completed_orders = Column(Integer, default=0)
    total_orders = Column(Integer, default=0)

    # Performance
    rating = Column(Float, default=5.0)
    acceptance_rate = Column(Float, default=100)

    # Audit
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

# =====================================================
# ACTIVE ORDER
# =====================================================

class DriverOrder(Base):
    __tablename__ = "driver_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    delivery_agent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("delivery_agents.id"),
        nullable=False
    )

    restaurant_name = Column(String)

    drop_distance = Column(Float)

    status = Column(
        String,
        default="assigned"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# =====================================================
# SHIFT
# =====================================================




class DriverShift(Base):
    __tablename__ = "driver_shifts"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    delivery_agent_id = Column(UUID(as_uuid=True),ForeignKey("delivery_agents.id"),nullable=False)
    title = Column(String,nullable=False)
    start_time = Column(String,nullable=False)
    end_time = Column(String,nullable=False)
    estimated_earning = Column(Float,default=0)
    is_booked = Column(Boolean,default=False)
    demand_tag = Column(String,nullable=True)
    status = Column(String,default="upcoming")

# =====================================================
# PEAK HOUR BONUS
# =====================================================

class PeakHourBonus(Base):
    __tablename__ = "peak_hour_bonus"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    bonus_amount = Column(Float, default=2.50)

    active = Column(Boolean, default=True)

    expires_in_minutes = Column(Integer, default=42)


# =====================================================
# EARNING BOOST
# =====================================================

class EarningsBoost(Base):
    __tablename__ = "earnings_boost"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    zone_name = Column(String)

    boost_percentage = Column(Integer)

    active = Column(Boolean, default=True)



class DriverChallenge(Base):
    __tablename__ = "driver_challenges"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)

    delivery_agent_id = Column(UUID(as_uuid=True),ForeignKey("delivery_agents.id"),nullable=False)

    title = Column(String)
    description = Column(String)

    reward_amount = Column(Float)


class DriverHotspot(Base):
    __tablename__ = "driver_hotspots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    zone_name = Column(String)

    bonus_amount = Column(Float)


# Break Management
is_on_break = Column(Boolean, default=False)
break_minutes = Column(Integer, default=15)