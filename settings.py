from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DB_URL: str
    API_ID: int
    API_HASH: str
    TDATA_PATH: str
    OPENAI_API_KEY: str

    redis_host: str
    redis_port: int
    redis_db: int
    redis_password: str

    class Config:
        env_file = ".env"

settings = Settings()