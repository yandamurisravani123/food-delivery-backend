from pydantic import BaseModel


class AddCustomizedItemSchema(BaseModel):
    item_id: int
    quantity: int


class UpdateQuantitySchema(BaseModel):
    cart_id: int
    quantity: int