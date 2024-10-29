from pydantic import BaseModel


class BaseProduct(BaseModel):
    id: int


class CreateProduct(BaseModel):
    name: str
    description: str | None = None
    price: int
    quantity: int

    class Config:
        from_attributes = True

class ResponseProduct(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True