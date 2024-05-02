import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker
from models import Base
env_path=dotenv.find_dotenv()

dotenv.load_dotenv(override=True)

URL_DATABASE = os.getenv("DATABASE_URL")

engine = create_engine(URL_DATABASE)
session = sessionmaker(autocommit=False,autoflush=False,bind=engine)


Base.metadata.create_all(bind=engine)

