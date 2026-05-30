from app.api.v1 import restaurant_router
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config.database import (
    engine,
    Base
)

from app.api.v1.api import api_router
from app.core.database import Base
from app.core.database import engine
 


# =====================================================
# IMPORT MODELS
# =====================================================

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
    delivery_partner,
    Plan,
    Feature,
    Subscription
)
from app.api.v1.customer.feedback_router import (
    router as feedback_router
)
from app.api.v1.customer.customer_home_router import (
    router as customer_home_router
)
from app.api.v1.customer.food_router import(
    router as food_router
)
from app.api.v1.customer.invoice_router import(
    router as invoice_router
)
from app.api.v1.customer.order_router import(
    router as order_router
)
from app.api.v1.customer.payment_router import(
    router as payment_router
)
from app.api.v1.recommendation_router import(
    router as recommendation_router
)
from app.api.v1.router import(
    router as router
)
from app.api.v1.super_admin_router import(
    router as super_admin_router
)
from app.api.v1.user_preference_router import(
    router as user_preference_router
)
from app.api.v1.restaurant.api_router import(
    router as api_router
)
from app.api.v1.restaurant.auth_router import(
    router as auth_router
)
from app.api.v1.restaurant_router import router as restaurant_router
from app.routes.plans import router as plans_router
from app.routes.features import router as features_router
from app.routes.subscriptions import router as subscriptions_router
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

app.include_router(feedback_router)
app.include_router(customer_home_router)
app.include_router(food_router)
app.include_router(invoice_router)
app.include_router(order_router)
app.include_router(payment_router)

app.include_router(recommendation_router)

app.include_router(super_admin_router)
app.include_router(user_preference_router)
app.include_router(api_router)
app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(plans_router)
 
app.include_router(features_router)
 
app.include_router(subscriptions_router)
# =====================================================
# ROOT API
# =====================================================

@app.get("/")
async def root():
    return {
        "message": "AI Recommendation Backend Running"
    }