from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password
)
from app.database.mongodb import users_collection
from app.schemas.user import UserCreate


async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one(
        {
            "email": user.email
        }
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user_document = {
        "name": user.name,
        "email": user.email,
        "password_hash": hash_password(
            user.password
        )
    }

    result = await users_collection.insert_one(
        user_document
    )

    return {
        "message": "User created successfully",
        "user_id": str(result.inserted_id)
    }


async def login_user(
    email: str,
    password: str
):
    user = await users_collection.find_one(
        {
            "email": email
        }
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    password_is_valid = verify_password(
        password,
        user["password_hash"]
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    access_token = create_access_token(
        str(user["_id"])
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }