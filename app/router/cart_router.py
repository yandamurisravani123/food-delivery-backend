# from fastapi import APIRouter, Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.config.database import get_db
# from app.schemas.cart import (
#     AddToCartSchema,
#     CartResponse
# )
# from app.services.cart_service import (
#     CartService
# )

# router = APIRouter(
#     prefix="/api/v1/cart",
#     tags=["Cart"]
# )


# @router.post(
#     "/add/{customer_id}",
#     response_model=CartResponse
# )
# async def add_to_cart(
#     customer_id: str,
#     payload: AddToCartSchema,
#     db: AsyncSession = Depends(get_db)
# ):

#     cart_item = await CartService.add_to_cart(
#         db=db,
#         customer_id=customer_id,
#         menu_item_id=payload.menu_item_id,
#         quantity=payload.quantity
#     )

#     return cart_item

# from fastapi import APIRouter

# router = APIRouter()


# @router.post("/add")
# async def add_to_cart():
#     return {"message": "Item added to cart"}


# @router.get("/")
# async def get_cart():
#     return {"message": "Cart fetched"}
