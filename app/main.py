from fastapi import FastAPI

# =========================
# Database
# =========================

from app.config.database import (
    engine,
    Base
)

# =========================
# Redis
# =========================

from app.core.redis_client import (
    connect_redis,
    close_redis
)

# =========================
# Models
# =========================
# IMPORTANT:
# Use direct imports to avoid circular import issues

import app.models.user
import app.models.restaurant
import app.models.cuisine
import app.models.recent_search
import app.models.banner
import app.models.user_location
import app.models.filter
import app.models.flash_deal
import app.models.offer
import app.models.menu
import app.models.review

# =========================
# NEW MODELS
# =========================

import app.models.menu_item
import app.models.extra
import app.models.preference
import app.models.cart
import app.models.cart_extra
import app.models.cart_preference
import app.models.special_instruction

# =========================
# Auth Routers
# =========================

from app.api.v1.auth import (
    router as auth_router
)

# =========================
# Admin Routers
# =========================

from app.api.v1.admin.super_admin import (
    router as super_admin_router
)

# =========================
# Customer Routers
# =========================

from app.api.v1.customer.home import (
    router as home_router
)

from app.api.v1.customer.search import (
    router as search_router
)

from app.api.v1.customer.restaurant import (
    router as restaurant_router
)

from app.api.v1.customer.cuisine import (
    router as cuisine_router
)

from app.api.v1.customer.recent_search import (
    router as recent_search_router
)

from app.api.v1.customer.flash_deal import (
    router as flash_router
)

from app.api.v1.customer.offer import (
    router as offer_router
)

from app.api.v1.customer.map import (
    router as map_router
)

from app.api.v1.customer.filter import (
    router as filter_router
)

# =========================
# NEW CUSTOMIZATION ROUTERS
# =========================

from app.api.v1.customer.customization import (
    router as customization_router
)

from app.api.v1.customer.extras import (
    router as extras_router
)

from app.api.v1.customer.preferences import (
    router as preferences_router
)

from app.api.v1.customer.cart import (
    router as cart_router
)

from app.api.v1.customer.checkout import (
    router as checkout_router
)

# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="Food Delivery Backend",
    version="1.0.0"
)

# =========================
# Include Routers
# =========================

# Auth
app.include_router(
    auth_router,
    prefix="/api/v1"
)

# Super Admin
app.include_router(
    super_admin_router,
    prefix="/api/v1"
)

# Home
app.include_router(
    home_router,
    prefix="/api/v1"
)

# Search
app.include_router(
    search_router,
    prefix="/api/v1"
)

# Restaurant
app.include_router(
    restaurant_router,
    prefix="/api/v1"
)

# Cuisine
app.include_router(
    cuisine_router,
    prefix="/api/v1"
)

# Recent Search
app.include_router(
    recent_search_router,
    prefix="/api/v1"
)

# Flash Deals
app.include_router(
    flash_router,
    prefix="/api/v1"
)

# Offers
app.include_router(
    offer_router,
    prefix="/api/v1"
)

# Map
app.include_router(
    map_router,
    prefix="/api/v1"
)

# Filter
app.include_router(
    filter_router,
    prefix="/api/v1"
)

# =========================
# CUSTOMIZATION ROUTERS
# =========================

# Customization
app.include_router(
    customization_router,
    prefix="/api/v1/customer",
    tags=["Customization"]
)

# Extras
app.include_router(
    extras_router,
    prefix="/api/v1/customer",
    tags=["Extras"]
)

# Preferences
app.include_router(
    preferences_router,
    prefix="/api/v1/customer",
    tags=["Preferences"]
)

# Cart
app.include_router(
    cart_router,
    prefix="/api/v1/customer",
    tags=["Cart"]
)

# Checkout
app.include_router(
    checkout_router,
    prefix="/api/v1/customer",
    tags=["Checkout"]
)

# =========================
# Startup Event
# =========================

@app.on_event("startup")
async def startup():

    print("🚀 Starting Backend...")

    # Create Database Tables
    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    print("✅ Database Connected")

    # Connect Redis
    await connect_redis()

    print("✅ Redis Connected")

# =========================
# Shutdown Event
# =========================

@app.on_event("shutdown")
async def shutdown():

    print("🛑 Shutting Down Backend...")

    # Close Redis
    await close_redis()

    print("✅ Redis Connection Closed")

# =========================
# Root Endpoint
# =========================

@app.get("/")
async def root():

    return {
        "message": "Food Delivery Backend Running Successfully"
    }