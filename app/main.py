# from fastapi import FastAPI
# from app.api.v1.admin.super_admin import router as super_admin
# from app.api.v1.auth import router as auth
# from app.config.database import engine, Base
# from app.core import redis_client
# from app.models import user  # noqa

# app = FastAPI(title="Food Delivery Backend")
# app.include_router(auth, prefix="/api/v1")
# app.include_router(super_admin, prefix="/api/v1")

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @app.on_event("startup")
# async def startup():
#     try:
#         await redis_client.ping()
#         print("✅ Redis connected")
#     except Exception as e:
#         print(f"❌ Redis connection failed: {e}")


from fastapi import FastAPI

from app.api.v1.admin.super_admin import router as super_admin
from app.api.v1.auth import router as auth
#from app.api.v1.restaurant import revenue_router
from app.api.v1.restaurant.router import router as restaurant_router
from app.api.v1.customer.router import (
    router as order_router
)

#from app.api.v1.restaurant.menu.router import router as menu_router
from app.config.database import engine, Base
from app.core.redis_client import (
    connect_redis,
    close_redis
)

from app.models import user  # noqa

from app.api.v1.driver.router import router as driver_router

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

app.include_router(
    order_router
)

app.include_router(driver_router, prefix="/driver", tags=["Driver"])



# RESTAURANT ROUTES
app.include_router(
    restaurant_router,
    prefix="/api/v1"
)
 



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