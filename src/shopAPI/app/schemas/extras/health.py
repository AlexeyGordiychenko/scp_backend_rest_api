from pydantic import BaseModel, Field


class Health(BaseModel):
    name: str = Field(..., example="ShopAPI")
    version: str = Field(..., example="1.0.0")
    status: str = Field(..., example="OK")
    message: str = Field(..., example="Visit /swagger for documentation.")
