import os
import dotenv
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import schemas

# SECREAT_KEY
# Algorithm
# Expiration-time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

env_path = dotenv.find_dotenv()

dotenv.load_dotenv(override=True)

SECREAT_KEY = os.getenv("SECREAT_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_DATE = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def create_access_token(email, auth):
    expire = datetime.now(datetime.timezone.utc) + timedelta(
        minutes=int(EXPIRATION_DATE)
    )
    to_encode = {"user": email, "exp": expire, "iat": datetime.now(), "admin": auth}
    token = jwt.encode(to_encode, SECREAT_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token=token, key=SECREAT_KEY, algorithms=ALGORITHM)
        email = payload.get("user")
        if email is None:
            raise credential_exception
        return payload
    except JWTError:
        raise credential_exception
    return payload


def get_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(
        token=token,
        credential_exception=HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authorize user",
            headers={"WWW-Autenticate": "Bearer"},
        ),
    )
