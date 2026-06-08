<<<<<<< HEAD

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


=======
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c
from fastapi import FastAPI

from app.api.v1.admin.super_admin import router as super_admin
from app.api.v1.auth import router as auth
from app.api.v1.restaurant.router import router as restaurant_router
<<<<<<< HEAD
from app.api.v1.customer.router import (
    router as order_router
)
#from app.api.v1.restaurant.menu.router import router as menu_router


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

=======
from app.api.v1.customer.router import router as order_router
from app.config.database import engine, Base
from app.core.redis_client import connect_redis, close_redis
from app.core.middleware import LoggingMiddleware
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c
from app.models import user  # noqa
from app.models import restaurant  # noqa

<<<<<<< HEAD

app = FastAPI(
    title="Food Delivery Backend"
)

=======
app = FastAPI(title="Food Delivery Backend")

app.add_middleware(LoggingMiddleware)
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c

# Include Routers
app.include_router(auth, prefix="/api/v1")
app.include_router(super_admin, prefix="/api/v1")
app.include_router(restaurant_router)
<<<<<<< HEAD

app.include_router(
    order_router
)
#app.include_router(menu_router)
app.include_router(
    order_router
)
=======
app.include_router(order_router)

>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c

# Startup Event
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await connect_redis()


# Shutdown Event
@app.on_event("shutdown")
async def shutdown():
<<<<<<< HEAD

    # Close Redis

    await close_redis()

    await close_redis()


=======
    await close_redis()
>>>>>>> 457d15f18d9f3ed7a3ecb61d552797cd208b570c
