from pydantic import BaseModel
from uuid import UUID


class AddToCartSchema(BaseModel):
    menu_item_id: UUID
    quantity: int = 1


class CartResponse(BaseModel):
    id: UUID
    customer_id: UUID
    menu_item_id: UUID
    quantity: int

    class Config:
        from_attributes = True