from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash(password:str):
    pwd_context.hash(password)