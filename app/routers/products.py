from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate
)
from app.services.product_service import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product
)

#Defines product endpoints:
router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create(
    product: ProductCreate,
    current_user: Annotated[
        dict, #should be a dict
        Depends(get_current_user) #FastAPI gets it from get_current_user() and put it inside current_user
    ]
):
    return await create_product(
        product,
        current_user
    )


@router.get(
    "/",
    response_model=list[ProductResponse]
)
async def get_all():
    return await get_products()


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
async def get_one(product_id: str):
    return await get_product(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
async def update(
    product_id: str,
    product: ProductUpdate,
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    return await update_product(
        product_id,
        product
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    product_id: str,
    current_user: Annotated[
        dict,
        Depends(get_current_user)
    ]
):
    await delete_product(product_id)

    return None