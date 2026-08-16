from pydantic import BaseModel, Field

#Defines product-related data + validation
class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100
    )

    price: float = Field(
        gt=0
    )

    description: str = Field(
        min_length=2,
        max_length=500
    )


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    price: float | None = Field(
        default=None,
        gt=0
    )

    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=500
    )


class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    description: str