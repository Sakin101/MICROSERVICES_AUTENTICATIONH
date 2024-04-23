from sqlalchemy import VARCHAR,Column
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base

Base=declarative_base()


class Users(Base):
    __tablename__="user"

    email_address=Column(VARCHAR(255),primary_key=True)
    password=Column(VARCHAR(255))
