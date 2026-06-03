from pydantic import BaseModel


class SelectExtraSchema(BaseModel):
    cart_id: int
    extra_id: int