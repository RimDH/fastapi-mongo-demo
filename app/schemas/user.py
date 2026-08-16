from pydantic import BaseModel, EmailStr

#Defines user-related request/response structures + validation
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr