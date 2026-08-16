from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.services.auth_service import (
    login_user,
    register_user
)

#Defines authentication endpoints:
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register(user: UserCreate):
    return await register_user(user)


@router.post(
    "/login",
    response_model=Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return await login_user(
        email=form_data.username,
        password=form_data.password
    )