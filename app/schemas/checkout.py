from pydantic import BaseModel
from datetime import date, time


class CheckoutCreate(BaseModel):

    user_id: str

    address: str

    delivery_date: date

    delivery_time: time

    payment_method: str

    subtotal: float

    delivery_fee: float


class CheckoutResponse(BaseModel):

    id: str

    message: str