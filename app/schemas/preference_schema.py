from pydantic import BaseModel


class SelectPreferenceSchema(BaseModel):
    cart_id: int
    preference_id: int