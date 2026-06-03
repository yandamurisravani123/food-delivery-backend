from fastapi import FastAPI

from app.api.v1.admin.super_admin import router as super_admin
from app.api.v1.auth import router as auth
from app.api.v1.restaurant.router import router as restaurant_router
from app.api.v1.customer.router import router as order_router
from app.config.database import engine, Base
from app.core.redis_client import connect_redis, close_redis
from app.core.middleware import LoggingMiddleware
from app.models import user  # noqa
from app.models import restaurant  # noqa

app = FastAPI(title="Food Delivery Backend")

app.add_middleware(LoggingMiddleware)

# Include Routers
app.include_router(auth, prefix="/api/v1")
app.include_router(super_admin, prefix="/api/v1")
app.include_router(restaurant_router)
app.include_router(order_router)


# Startup Event
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await connect_redis()


# Shutdown Event
@app.on_event("shutdown")
async def shutdown():
    await close_redis()