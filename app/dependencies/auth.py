from typing import Annotated

import jwt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core.config import settings
from app.database.mongodb import users_collection

#This tells FastAPI that your API uses a Bearer token.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)
#FastAPI authentication dependency
#Take the JWT token from the request → verify it → get the user ID 
# → find that user in MongoDB → return the user.
async def get_current_user(
    token: Annotated[
        str,
        Depends(oauth2_scheme) #extracts the token from the Authorization header.
    ] #token should be a string AND FastAPI should get it using oauth2_scheme
):
    #one standard error that will be used whenever authentication fails
    #If the JWT is invalid, expired, incorrectly signed, malformed, etc., 
    #the request is rejected with 401.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        ) #This verifies and decodes the JWT.

        user_id = payload.get("sub") #sub usually means subject = user_id

        if user_id is None: 
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception

    if not ObjectId.is_valid(user_id): #Validate MongoDB ObjectId
        raise credentials_exception

    user = await users_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )

    if user is None:
        raise credentials_exception

    return user

#If everything succeeded, the dependency returns the user.