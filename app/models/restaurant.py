import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Float, func, Integer, Text
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.config.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
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

    orders = relationship("Order", back_populates="restaurant")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), nullable=False)
    ingredient_name = Column(String)
    category = Column(String)
    stock_units = Column(Float)
    unit = Column(String)
    min_threshold = Column(Float, default=10)
    current_price = Column(Float)
    last_price = Column(Float)
    price_change = Column(Float)
    is_out_of_stock = Column(Boolean, default=False)
    minimum_stock = Column(Float, default=10)
    is_low_stock = Column(Boolean, default=False)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    waste_logs = relationship("IngredientWaste", back_populates="ingredient")


class IngredientWaste(Base):
    __tablename__ = "ingredient_waste"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))
    units_spoiled = Column(Integer)
    reason = Column(Text)
    loss_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    ingredient = relationship("Ingredient", back_populates="waste_logs")


class MenuIngredient(Base):
    __tablename__ = "menu_ingredients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    menu_item_id = Column(UUID(as_uuid=True), ForeignKey("menu_items.id"))
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))
    quantity_required = Column(Float)


class InventoryAdjustment(Base):
    __tablename__ = "inventory_adjustments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ingredient_id = Column(UUID(as_uuid=True))
    ingredient_name = Column(String)
    previous_quantity = Column(Float)
    new_quantity = Column(Float)
    reason = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class InventoryAlert(Base):
    __tablename__ = "inventory_alerts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"))
    ingredient_id = Column(UUID(as_uuid=True), ForeignKey("ingredients.id"))
    alert_type = Column(String)
    message = Column(String)
    current_stock = Column(Float)
    threshold_value = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
