from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL")
    API_HASH: str = os.getenv("API_HASH")
    API_ID: int = os.getenv("API_ID")



settings = Settings()