from typing import Optional
from pydantic import BaseModel, field_validator


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        orm_mode = True

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value <= 3:
            raise ValueError("Price must be greater than 3")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value


class ItemRead(ItemCreate):
    id: int

    class Config:
        orm_mode = True


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value is not None and value <= 3:
            raise ValueError("Price must be greater than 3")
        return value

    class Config:
        orm_mode = True
