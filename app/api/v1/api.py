from fastapi import APIRouter
<<<<<<< HEAD

=======
 
>>>>>>> 6da5f03 (testing)
from app.api.v1.restaurant.analytics_router import (
    router as analytics_router
)
from app.api.v1.restaurant.dashboard import router as dashboard_router
<<<<<<< HEAD

api_router = APIRouter()

api_router.include_router(analytics_router)

=======
 
api_router = APIRouter()
 
api_router.include_router(analytics_router)
 
>>>>>>> 6da5f03 (testing)
api_router.include_router(dashboard_router)