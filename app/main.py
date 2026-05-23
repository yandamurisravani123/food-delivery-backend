from fastapi import FastAPI

from app.api.v1.admin.super_admin import (
    router as super_admin
)
from app.api.v1.auth import router as auth
from app.api.v1.restaurant.router import (
    router as restaurant_router
)
from app.api.v1.cart.router import (
    router as cart_router
)
from app.api.v1.customer_discovery_router import (
    router as customer_discovery_router
)

from app.api.v1.customer_home_router import (
    router as home_feed_router
)

from app.config.database import (
    engine,
    Base
)

from app.core.redis_client import (
    connect_redis,
    close_redis
)

from app.models import user  # noqa


app = FastAPI(
    title="Food Delivery Backend"
)


# ==========================
# INCLUDE ROUTERS
# ==========================

app.include_router(
    auth,
    prefix="/api/v1"
)

app.include_router(
    super_admin,
    prefix="/api/v1"
)

app.include_router(
    restaurant_router
)

app.include_router(
    cart_router
)

app.include_router(
    cart_router,
    tags=["Add To Cart"]
)


# CUSTOMER DISCOVERY ROUTER
app.include_router(
    customer_discovery_router
)

app.include_router(
    home_feed_router
)


# ==========================
# STARTUP
# ==========================

@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    await connect_redis()


# ==========================
# SHUTDOWN
# ==========================

@app.on_event("shutdown")
async def shutdown():

    await close_redis()