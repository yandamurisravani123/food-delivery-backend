from pydantic import BaseModel
from uuid import UUID

class OrderCreate(BaseModel):
    user_id: UUID
    food_name: str
    cuisine: str
    order_time: str


class OrderResponse(BaseModel):
    id: int
    user_id: UUID
    food_name: str
    cuisine: str
    order_time: str

    class Config:
        from_attributes = True