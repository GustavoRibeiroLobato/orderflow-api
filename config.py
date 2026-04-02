import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")