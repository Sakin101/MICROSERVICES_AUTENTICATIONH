from pydantic import BaseModel
from pydantic import EmailStr



class User(BaseModel):
    email:EmailStr
    password:str
class ReturnUser(BaseModel):
    email_address:EmailStr
    class Config:
        orm=True