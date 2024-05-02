from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional


class User(BaseModel):
    email:EmailStr
    password:str
class ReturnUser(BaseModel):
    email_address:EmailStr
    class Config:
        orm=True
class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str]=None