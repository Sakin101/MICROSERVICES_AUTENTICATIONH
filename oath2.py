import os
import dotenv
from jose import JWTError,jwt
from datetime import datetime,timedelta
#SECREAT_KEY
#Algorithm
#Expiration-time


env_path=dotenv.find_dotenv()

dotenv.load_dotenv(override=True)

SECREAT_KEY=os.getenv("SECREAT_KEY")
ALGORITHM=os.getenv("ALGORITHM")
EXPIRATION_DATE=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now()+timedelta(minutes=int(EXPIRATION_DATE))
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECREAT_KEY,algorithm=ALGORITHM)
    return token