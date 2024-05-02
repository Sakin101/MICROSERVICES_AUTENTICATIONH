from sqlalchemy import VARCHAR,Column,Integer
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import HTTPBearer

bearer_scheme=HTTPBearer()

Base=declarative_base()


class Users(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True)
    email_address=Column(VARCHAR(255),unique=True)
    password=Column(VARCHAR(255))
