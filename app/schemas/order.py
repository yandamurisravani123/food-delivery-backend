from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    food_name: str
    cuisine: str
    order_time: str


class OrderResponse(BaseModel):
    id: int
    user_id: int
    food_name: str
    cuisine: str
    order_time: str

    class Config:
        from_attributes = True