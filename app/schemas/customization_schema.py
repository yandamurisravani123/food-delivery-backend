from pydantic import BaseModel


class SpecialInstructionSchema(BaseModel):
    instruction: str