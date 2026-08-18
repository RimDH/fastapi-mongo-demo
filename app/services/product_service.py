from bson import ObjectId
from fastapi import HTTPException, status

from app.database.mongodb import products_collection
from app.schemas.product import (
    ProductCreate,
    ProductUpdate
)


def format_product(product: dict) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "description": product["description"]
    }


async def create_product(
    product: ProductCreate,
    current_user: dict
):
    product_document = {
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "created_by": current_user["_id"]
    }

    result = await products_collection.insert_one( #MongoDB driver directly, not an ODM.
        product_document
    )

    created_product = (
        await products_collection.find_one(
            {
                "_id": result.inserted_id
            }
        )
    )

    return format_product(created_product)


async def get_products():
    products = []

    cursor = products_collection.find()

    async for product in cursor:
        products.append(
            format_product(product)
        )

    return products


async def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )

    product = await products_collection.find_one(
        {
            "_id": ObjectId(product_id)
        }
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return format_product(product)


async def update_product(
    product_id: str,
    product: ProductUpdate
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )

    existing_product = (
        await products_collection.find_one(
            {
                "_id": ObjectId(product_id)
            }
        )
    )

    if existing_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    update_data = product.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )

    await products_collection.update_one(
        {
            "_id": ObjectId(product_id)
        },
        {
            "$set": update_data
        }
    )

    updated_product = (
        await products_collection.find_one(
            {
                "_id": ObjectId(product_id)
            }
        )
    )

    return format_product(updated_product)


async def delete_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
        )

    result = await products_collection.delete_one(
        {
            "_id": ObjectId(product_id)
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )