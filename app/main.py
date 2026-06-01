from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.database import (
    engine,
    Base
)

from app.api.v1.api import api_router

# IMPORT MODELS

from app.models import (
    notification,
    user,
    order,
    food,
    user_preference,
    cart,
    checkout,
    invoice,
    invoice_item,
    restaurant,
    payment,
    delivery_partner
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

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    print("✅ Database Connected")

    await connect_redis()

    print("✅ Redis Connected")

    yield

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
# INCLUDE ALL ROUTERS
# =====================================================

app.include_router(api_router)

# =====================================================
# ROOT API
# =====================================================

@app.get("/")
async def root():
    return {
        "message": "AI Recommendation Backend Running"
    }