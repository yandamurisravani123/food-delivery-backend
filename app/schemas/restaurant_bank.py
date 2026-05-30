from uuid import UUID
from pydantic import BaseModel, Field


class RestaurantBankRequest(BaseModel):

    restaurant_id: UUID

    bank_account_holder: str = Field(...)

    bank_account_number: str = Field(...)

    confirm_account_number: str = Field(...)

    ifsc_code: str = Field(...)