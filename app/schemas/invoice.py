from pydantic import BaseModel

from typing import List


class InvoiceItemCreate(BaseModel):

    item_name: str

    description: str

    quantity: int

    price: float


class InvoiceCreate(BaseModel):

    order_id: str

    restaurant_name: str

    restaurant_gstin: str

    customer_gstin: str

    delivery_fee: float

    items: List[InvoiceItemCreate]


class InvoiceResponse(BaseModel):

    invoice_id: str

    invoice_number: str

    total_amount: float

    message: str