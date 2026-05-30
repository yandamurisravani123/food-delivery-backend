from fastapi import FastAPI

# DATABASE
from app.config.database import (
    engine,
    Base
)

# REDIS

from app.core.redis_client import (
    connect_redis,
    close_redis
)

# ROUTERS

# AUTH ROUTER
from app.api.v1.auth import router as auth

# SUPER ADMIN ROUTER
from app.api.v1.admin.super_admin import (
    router as super_admin
)

# RESTAURANT ROUTER
from app.api.v1.restaurant.router import (
    router as restaurant_router
)

# RESTAURANT ANALYTICS ROUTER
from app.api.v1.restaurant.analytics_router import (
    router as analytics_router
)

# REVENUE REPORT ROUTER
from app.api.v1.restaurant.revenue_router import (
    router as revenue_router
)

# DASHBOARD ROUTER
from app.api.v1.restaurant.dashboard import (
    router as dashboard_router
)

# =====================================================
# IMPORT ALL MODELS
# =====================================================

# USER MODEL
from app.models import user  # noqa

# RESTAURANT MODEL
from app.models import restaurant  # noqa

# ORDER MODEL
from app.models import order  # noqa

# ORDER ITEMS MODEL
from app.models import order_items  # noqa

# MENU MODEL
from app.models import menu  # noqa

# REVENUE REPORT MODEL
from app.models import revenue_report  # noqa

# FASTAPI APP

app = FastAPI(
    title="Food Delivery Backend",
    version="1.0.0"
)
# INCLUDE ROUTERS

# AUTH ROUTES
app.include_router(
    auth,
    prefix="/api/v1"
)

# SUPER ADMIN ROUTES
app.include_router(
    super_admin,
    prefix="/api/v1"
)

# RESTAURANT ROUTES
app.include_router(
    restaurant_router,
    prefix="/api/v1"
)

# ANALYTICS ROUTES
app.include_router(
    analytics_router,
    prefix="/api/v1"
)

# REVENUE REPORT ROUTES
app.include_router(
    revenue_router,
    prefix="/api/v1"
)

# DASHBOARD ROUTES
app.include_router(
    dashboard_router,
    prefix="/api/v1"
)

# STARTUP EVENT

@app.on_event("startup")
async def startup():

    try:

        # CREATE TABLES
        async with engine.begin() as conn:
            await conn.run_sync(
                Base.metadata.create_all
            )

        print("✅ Database Tables Created")

        # CONNECT REDIS
        await connect_redis()

        print("✅ Redis Connected")

    except Exception as e:

        print("❌ Startup Error:", str(e))

# SHUTDOWN EVENT

@app.on_event("shutdown")
async def shutdown():

    try:

        # CLOSE REDIS
        await close_redis()

        print("❌ Redis Disconnected")

    except Exception as e:

        print("❌ Shutdown Error:", str(e))


