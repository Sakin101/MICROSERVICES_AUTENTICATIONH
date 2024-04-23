from pydantic import BaseModel
from pydantic import EmailStr



class User(BaseModel):
    email:EmailStr
    password:str