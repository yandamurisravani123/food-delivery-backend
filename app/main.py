from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.database import (
    engine,
    Base
)

# =====================================================
# IMPORT MODELS
# =====================================================

from app.models import (
    user,
    order,
    food,
    user_preference,
    cart
)

# =====================================================
# ROUTERS
# =====================================================

from app.api.v1.admin.super_admin import (
    router as super_admin
)

from app.api.v1.auth import (
    router as auth
)

from app.api.v1.order_router import (
    router as order_router
)

from app.api.v1.food_router import (
    router as food_router
)

from app.api.v1.user_preference import (
    router as preference_router
)

from app.api.v1.recommendation_router import (
    router as recommendation_router
)

from app.api.v1.customer_discovery_router import (
    router as customer_discovery_router
)

from app.api.v1.cart_router import (
    router as cart_router
)

# =====================================================
# REDIS
# =====================================================

from app.core.redis_client import (
    connect_redis,
    close_redis
)

# =====================================================
# APP LIFESPAN
# =====================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    # CREATE DATABASE TABLES
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print("✅ Database Connected")

    # CONNECT REDIS
    await connect_redis()

    print("✅ Redis Connected")

    yield

    # CLOSE REDIS
    await close_redis()

    print("❌ Redis Disconnected")


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Food Delivery Backend",
    lifespan=lifespan
)

# =====================================================
# INCLUDE ROUTERS
# =====================================================

app.include_router(
    auth,
    prefix="/api/v1"
)

app.include_router(
    super_admin,
    prefix="/api/v1"
)

app.include_router(
    order_router
)

app.include_router(
    food_router
)

app.include_router(
    preference_router
)

app.include_router(
    recommendation_router,
    prefix="/api/v1"
)

app.include_router(
    customer_discovery_router,
    prefix="/api/v1"
)

app.include_router(
    cart_router,
    prefix="/api/v1"
)

# =====================================================
# ROOT API
# =====================================================

@app.get("/")
async def root():
    return {
        "message": "AI Recommendation Backend Running"
    }