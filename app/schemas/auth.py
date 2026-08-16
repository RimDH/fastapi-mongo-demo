from pydantic import BaseModel

#Defines authentication responses + validation
class Token(BaseModel):
    access_token: str
    token_type: str