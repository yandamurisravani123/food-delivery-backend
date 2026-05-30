from fastapi import APIRouter

from app.api.v1.superadmin_router import (
    router as superadmin_router
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

from app.api.v1.customer_discovery_router import (
    router as customer_discovery_router
)

from app.api.v1.cart_router import (
    router as cart_router
)

from app.api.v1.checkout_router import (
    router as checkout_router
)

from app.api.v1.invoice_router import (
    router as invoice_router
)

from app.api.v1.restaurant_router import (
    router as restaurant_router
)

from app.api.v1.payment_router import (
    router as payment_router
)

from app.api.v1.customer_home_router import (
    router as customer_home_router
)

api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(auth)

api_router.include_router(superadmin_router)

api_router.include_router(order_router)

api_router.include_router(food_router)

api_router.include_router(preference_router)

api_router.include_router(recommendation_router)

api_router.include_router(customer_discovery_router)

api_router.include_router(cart_router)

api_router.include_router(checkout_router)

api_router.include_router(invoice_router)

api_router.include_router(restaurant_router)

api_router.include_router(payment_router)

api_router.include_router(customer_home_router)