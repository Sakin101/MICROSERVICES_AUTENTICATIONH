"""Autentication module"""

import logging.config
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from database import session
import models, schemas
import logging
from utils import get_hash, verify
import oath2


logging.basicConfig(filename="server_error.log", encoding="utf-8", level=logging.ERROR)

app = FastAPI()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.post("/user")
def add_user(user: schemas.User, db=Depends(get_db)):
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
        print(user.password)
        new_user = models.Users(email_address=user.email, password=user.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"user": user.email}
    except Exception as e:
        logging.error("ERROR OCCURED %s", e)
        raise HTTPException(status_code=500)


@app.post("/user/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user_credentials = (
        db.query(models.Users)
        .filter(user.username == models.Users.email_address)
        .first()
    )
    if not user_credentials:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential"
        )
    if not verify(user.password, user_credentials.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    return {"token": oath2.create_access_token(user_credentials.email_address, True)}


@app.get("/user/{user_email}", response_model=schemas.ReturnUser)
def get_user(user_email: str, db=Depends(get_db)):
    user = (
        db.query(models.Users).filter(models.Users.email_address == user_email).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@app.post("/validate")
async def validate(user=Depends(oath2.get_user)):
    return user


