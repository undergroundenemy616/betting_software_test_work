from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DEBUG: bool
    TESTING: bool
    MONGO_DETAILS: str
    MONGO_DB_NAME: str
    MONGO_DB_COLLECTION: str
    SENTRY_DSN: str

    class Config:
        env_file = ".env"


settings = Settings()
