from fastapi import FastAPI
from contextlib import asynccontextmanager
from pathlib import Path
import importlib

from sqlalchemy import text
from app.config.database import Base, engine
from app.core.redis_client import connect_redis, close_redis

# AUTO-IMPORT ALL MODELS (so SQLAlchemy registers all tables)

models_dir = Path(__file__).resolve().parent / "models"
for model_file in sorted(models_dir.glob("*.py")):
    if model_file.stem != "__init__":
        try:
            importlib.import_module(f"app.models.{model_file.stem}")
        except Exception as e:
            print(f"Warning: could not import model {model_file.stem}: {e}")


# ROUTERS — Auth
from app.api.v1.customer.auth import router as auth_router

# ROUTERS — Admin
from app.api.v1.admin.super_admin import router as super_admin_router

# ROUTERS — Restaurant
from app.api.v1.restaurant.router import router as restaurant_router

# ROUTERS — Base Customer (home, search, cuisine, etc.)
from app.api.v1.customer.home import router as home_router
from app.api.v1.customer.search import router as search_router
from app.api.v1.customer.restaurant import router as customer_restaurant_router
from app.api.v1.customer.cuisine import router as cuisine_router
from app.api.v1.customer.recent_search import router as recent_search_router
from app.api.v1.customer.flash_deal import router as flash_router
from app.api.v1.customer.offer import router as offer_router
from app.api.v1.customer.map import router as map_router
from app.api.v1.customer.filter import router as filter_router
from app.api.v1.customer.customization import router as customization_router
from app.api.v1.customer.extras import router as extras_router
from app.api.v1.customer.preferences import router as preferences_router
from app.api.v1.customer.checkout import router as checkout_router
from app.api.v1.customer.review import router as review_router
from app.api.v1.customer.premium import router as premium_router
from app.api.v1.customer.tracking import router as tracking_router
from app.api.v1.customer.rewards import router as rewards_router

# =====================================================
# ROUTERS — Pranathi Features (LEV-167)
# =====================================================
from app.api.v1.customer.feedback import router as feedback_router
from app.api.v1.customer.customer_home_router import router as customer_home_router
from app.api.v1.customer.food_router import router as food_router
from app.api.v1.customer.invoice_router import router as invoice_router
from app.api.v1.customer.order_router import router as order_router
from app.api.v1.customer.payment_router import router as payment_router
from app.api.v1.customer.recommendation_router import router as recommendation_router
from app.api.v1.customer.user_preference import router as user_preference_router
from app.api.v1.customer.plans import router as plans_router
from app.api.v1.customer.features import router as features_router
from app.api.v1.customer.subscriptions import router as subscriptions_router
from app.api.v1.customer.wallet_router import router as wallet_router
from app.api.v1.customer.refund_router import router as refund_router
from app.api.v1.customer.tracking_router import router as tracking_detail_router
from app.api.v1.customer.notification_router import router as notification_router
from app.api.v1.driver.router import router as driver_router

# =====================================================
# ROUTERS — Sravani Features (LEV-165)
# =====================================================
from app.api.v1.customer.cart_router import router as cart_router
from app.api.v1.order_tracking import router as order_tracking_router
from app.api.v1.delivery_notification_router import router as delivery_notification_router
from app.api.v1.payment_method import router as payment_method_router
from app.api.v1.rating_router import router as rating_router
from app.api.v1.order_preparation_router import router as preparation_router
from app.api.v1.savings_router import router as savings_router
from app.api.v1.recommendation_router import router as ai_recommendation_router
from app.api.v1.customer.customer_discovery import router as customer_discovery_router
from app.api.v1.customer.customer_rating import router as customer_rating_router


# APP LIFESPAN

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS user_preferences CASCADE"))
        await conn.run_sync(Base.metadata.create_all)

        alter_statements = [
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) NOT NULL DEFAULT 'pending'",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_time TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()",
            "ALTER TABLE orders DROP COLUMN IF EXISTS user_id",
            "ALTER TABLE orders DROP COLUMN IF EXISTS restaurant_id",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id UUID",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS restaurant_id UUID",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS food_name VARCHAR(255)",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS cuisine VARCHAR(100)",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS start_time TIMESTAMP WITH TIME ZONE",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS completed_at TIMESTAMP WITH TIME ZONE",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS prep_time INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS is_urgent BOOLEAN NOT NULL DEFAULT FALSE",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_address TEXT",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS courier_name VARCHAR(255)",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS courier_rating VARCHAR(50)",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS special_instructions TEXT",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS packaging_notes TEXT",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS cutlery_required BOOLEAN NOT NULL DEFAULT TRUE",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS subtotal DOUBLE PRECISION NOT NULL DEFAULT 0.0",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_fee DOUBLE PRECISION NOT NULL DEFAULT 0.0",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS tax_percent DOUBLE PRECISION NOT NULL DEFAULT 0.0",
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total DOUBLE PRECISION NOT NULL DEFAULT 0.0",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_trending BOOLEAN NOT NULL DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS is_top_rated BOOLEAN NOT NULL DEFAULT FALSE",
            "ALTER TABLE restaurants ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP WITH TIME ZONE",
            "ALTER TABLE user_preferences ALTER COLUMN user_id TYPE UUID USING user_id::text::uuid",
            "ALTER TABLE user_preferences ALTER COLUMN id TYPE UUID USING id::text::uuid",
        ]

        for stmt in alter_statements:
            try:
                await conn.execute(text(stmt))
            except Exception:
                pass

    print("Database Connected")

    redis_available = await connect_redis()

    if redis_available:
        print("Redis Connected")
    else:

        print(" Redis not available, continuing without Redis")


    # REQUIRED
    yield

    await close_redis()
    print("Redis Disconnected")


# FASTAPI APP

app = FastAPI(
    title="Food Delivery Backend",
    version="1.0.0",
    description="Merged backend: base + pranathi-LEV-167 + sravani-165",
    debug=True,
    lifespan=lifespan
)


# INCLUDE ALL ROUTERS

# Auth
app.include_router(auth_router, prefix="/api/v1")

# Admin
app.include_router(super_admin_router, prefix="/api/v1")

# Restaurant
app.include_router(restaurant_router, prefix="/api/v1")

# ---- Base Customer Routers ----
app.include_router(home_router, prefix="/api/v1", tags=["Home"])
app.include_router(search_router, prefix="/api/v1")
app.include_router(customer_restaurant_router, prefix="/api/v1")
app.include_router(cuisine_router, prefix="/api/v1")
app.include_router(recent_search_router, prefix="/api/v1")
app.include_router(flash_router, prefix="/api/v1")
app.include_router(offer_router, prefix="/api/v1")
app.include_router(map_router, prefix="/api/v1")
app.include_router(filter_router, prefix="/api/v1")
app.include_router(customization_router, prefix="/api/v1/customer", tags=["Customization"])
app.include_router(extras_router, prefix="/api/v1/customer", tags=["Extras"])
app.include_router(preferences_router, prefix="/api/v1/customer", tags=["Preferences"])
app.include_router(checkout_router, prefix="/api/v1/customer", tags=["Checkout"])
app.include_router(review_router, prefix="/api/v1/customer", tags=["Reviews"])
app.include_router(premium_router)
app.include_router(tracking_router)
app.include_router(rewards_router)

# ---- Pranathi Customer Routers ----
app.include_router(feedback_router)
app.include_router(customer_home_router)
app.include_router(food_router)
app.include_router(invoice_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(recommendation_router)
app.include_router(user_preference_router)
app.include_router(plans_router)
app.include_router(features_router)
app.include_router(subscriptions_router)
app.include_router(wallet_router)
app.include_router(refund_router)
app.include_router(tracking_detail_router)
app.include_router(notification_router)
app.include_router(driver_router)

# ---- Sravani Routers ----
app.include_router(cart_router)
app.include_router(order_tracking_router, prefix="/api/v1")
app.include_router(delivery_notification_router, prefix="/api/v1")
app.include_router(payment_method_router, prefix="/api/v1")
app.include_router(rating_router, prefix="/api/v1")
app.include_router(preparation_router, prefix="/api/v1")
app.include_router(savings_router, prefix="/api/v1")
app.include_router(ai_recommendation_router, prefix="/api/v1")
app.include_router(customer_discovery_router)
app.include_router(customer_rating_router)


# ROOT

@app.get("/")
async def root():
    return {
        "message": "Food Delivery Backend Running Successfully",
        "version": "1.0.0 (merged: base + pranathi-LEV-167 + sravani-165)"
    }