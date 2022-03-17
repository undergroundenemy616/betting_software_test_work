import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY: str
    DEBUG: bool
    TESTING: bool
    MONGO_DETAILS: str
    MONGO_DB_NAME: str
    MONGO_DB_COLLECTION: str

    class Config:
        env_file = ".env"


settings = Settings()
