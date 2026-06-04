from pydantic import BaseModel


class CheckoutPreviewSchema(BaseModel):
    cart_id: int