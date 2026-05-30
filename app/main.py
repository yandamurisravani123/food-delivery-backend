from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.database import engine, Base

# MODELS
# Import all models
from app.models.user import User
from app.models.driver import Driver
from app.models.restaurant import Restaurant
from app.models.food import Food
from app.models.order import Order
from app.models.ratings import Rating
from app.models.cart import Cart
from app.models.payment_method import PaymentMethod
# ROUTERS
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

# REMOVE THIS IF FILE DOES NOT EXIST
try:
    from app.api.v1.customer_discovery_router import (
        router as customer_discovery_router
    )
    customer_discovery_available = True
except ModuleNotFoundError:
    customer_discovery_available = False


from app.api.v1.cart_router import (
    router as cart_router
)

from app.api.v1.order_tracking import (
    router as order_tracking_router
)

from app.api.v1.delivery_notification_router import (
    router as delivery_notification_router
)

from app.api.v1.payment_method import (
    router as payment_router
)

from app.api.v1.rating_router import (
    router as rating_router
)

# REDIS
from app.core.redis_client import (
    connect_redis,
    close_redis
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # CREATE DATABASE TABLES
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database Connected")

    await connect_redis()
    print("✅ Redis Connected")

    yield

    await close_redis()
    print("❌ Redis Disconnected")


app = FastAPI(
    title="Food Delivery Backend",
    lifespan=lifespan
)

# ROUTERS
app.include_router(
    auth,
    prefix="/api/v1"
)

app.include_router(
    super_admin,
    prefix="/api/v1"
)

app.include_router(order_router)
app.include_router(food_router)
app.include_router(preference_router)

app.include_router(
    recommendation_router,
    prefix="/api/v1"
)

# INCLUDE ONLY IF FILE EXISTS
if customer_discovery_available:
    app.include_router(
        customer_discovery_router,
        prefix="/api/v1"
    )

app.include_router(
    cart_router,
    prefix="/api/v1"
)

app.include_router(
    order_tracking_router,
    prefix="/api/v1"
)

app.include_router(
    delivery_notification_router,
    prefix="/api/v1"
)

app.include_router(
    payment_router,
    prefix="/api/v1"
)

app.include_router(
    rating_router,
    prefix="/api/v1"
)


@app.get("/")
async def root():
    return {
        "message": "AI Recommendation Backend Running"
    }