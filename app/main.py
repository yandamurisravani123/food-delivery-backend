from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
import importlib
from sqlalchemy import text
from app.core.database import Base, engine


# Import all models so SQLAlchemy metadata includes every table
models_dir = Path(__file__).resolve().parent / "models"
for model_file in models_dir.glob("*.py"):
    if model_file.stem != "__init__":
        importlib.import_module(f"app.models.{model_file.stem}")

from app.api.v1.customer.feedback import router as feedback_router
from app.api.v1.customer.customer_home_router import router as customer_home_router
from app.api.v1.customer.food_router import router as food_router
from app.api.v1.customer.invoice_router import router as invoice_router
from app.api.v1.customer.order_router import router as order_router
from app.api.v1.customer.payment_router import router as payment_router
from app.api.v1.customer.recommendation_router import router as recommendation_router

from app.api.v1.admin.super_admin import router as super_admin_router
from app.api.v1.customer.user_preference import router as user_preference_router
from app.api.v1.restaurant.router import router as restaurant_router
from app.api.auth import router as auth_router

from app.api.v1.customer.plans import router as plans_router
from app.api.v1.customer.features import router as features_router
from app.api.v1.customer.subscriptions import router as subscriptions_router
from app.api.v1.customer.wallet_router import router as wallet_router
from app.api.v1.customer.refund_router import router as refund_router
from app.api.v1.customer.tracking_router import router as tracking_router
from app.core.redis_client import connect_redis, close_redis
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
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) NOT NULL DEFAULT 'pending'"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS start_time TIMESTAMP WITH TIME ZONE"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS prep_time INTEGER NOT NULL DEFAULT 0"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS is_urgent BOOLEAN NOT NULL DEFAULT FALSE"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_address TEXT"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS courier_name VARCHAR(255)"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS courier_rating VARCHAR(50)"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS special_instructions TEXT"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS packaging_notes TEXT"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS cutlery_required BOOLEAN NOT NULL DEFAULT TRUE"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS subtotal DOUBLE PRECISION NOT NULL DEFAULT 0.0"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_fee DOUBLE PRECISION NOT NULL DEFAULT 0.0"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS tax_percent DOUBLE PRECISION NOT NULL DEFAULT 0.0"
            )
        )
        await conn.execute(
            text(
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total DOUBLE PRECISION NOT NULL DEFAULT 0.0"
            )
        )

    print("✅ Database Connected")

    redis_available = await connect_redis()

    if redis_available:
        print("✅ Redis Connected")
    else:
        print("❌ Redis not available, continuing without Redis")

    yield

    await close_redis()

    print("❌ Redis Disconnected")


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="Food Delivery Backend",
    debug=True,
    lifespan=lifespan
)

# =====================================================
# INCLUDE ALL ROUTERS
# =====================================================
api_router = APIRouter()

app.include_router(feedback_router)
app.include_router(customer_home_router)
app.include_router(food_router)
app.include_router(invoice_router)
app.include_router(order_router)
app.include_router(payment_router)

app.include_router(recommendation_router)

app.include_router(super_admin_router)




app.include_router(user_preference_router)

app.include_router(auth_router)
app.include_router(restaurant_router)
app.include_router(plans_router)
 
app.include_router(features_router)
 
app.include_router(subscriptions_router)
app.include_router(wallet_router)
app.include_router(refund_router)
app.include_router(tracking_router)
# =====================================================
# ROOT API
# =====================================================

@app.get("/")
async def root():
    return {
        "message": "AI Recommendation Backend Running"
    }