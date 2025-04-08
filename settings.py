from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL: str
    API_ID: int
    API_HASH: str
    TDATA_PATH: str

    class Config:
        env_file = ".env"

settings = Settings()