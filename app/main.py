
from fastapi import FastAPI

from app.models import restaurant
from app.models import user

from app.api.v1.admin.super_admin import router as super_admin
from app.api.v1.auth import router as auth
from app.api.v1.restaurant.router import router as restaurant_router

from app.config.database import engine, Base
from app.core.redis_client import (
    connect_redis,
    close_redis
)

app = FastAPI(
    title="Food Delivery Backend"
)

# Include Routers
app.include_router(
    auth,
    prefix="/api/v1"
)

app.include_router(
    super_admin,
    prefix="/api/v1"
)

app.include_router(restaurant_router)

# Startup Event
@app.on_event("startup")
async def startup():

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all
        )

    # Connect Redis
    await connect_redis()


# Shutdown Event
@app.on_event("shutdown")
async def shutdown():

    # Close Redis
    await close_redis()

