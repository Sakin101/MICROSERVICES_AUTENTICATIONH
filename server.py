"""Autentication module"""

import logging.config
from fastapi import FastAPI, HTTPException, Depends
from database import session
import models, schemas
from sqlalchemy.orm import Session
import mysql
import logging
from utils import get_hash


logging.basicConfig(filename="server_error.log", encoding="utf-8", level=logging.ERROR)

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.post("/login/")
def login(user: schemas.User, db=Depends(get_db)):
    email_check = db.query(models.Users).filter(
        models.Users.email_address == user.email
    )
    if not email_check:
        raise HTTPException(
            detail="Email already exists",
            status_code=HTTPException(status_code=409, detail="Email already exisits"),
        )

    try:
        hash_password = get_hash(user.password)
        user.password = hash_password
        new_user = models.Users(email_address=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"user": user.email, "password": user.password}
    except Exception as e:
        logging.error("ERROR OCCURED %s", e)
        raise HTTPException(status_code=500)


@app.get("/user/{user}")
def get_user(user, db=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email_address == user).first()
    print(user)
    return user
