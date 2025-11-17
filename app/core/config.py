from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Investment Platform"
    
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    # Email
    AWS_SES_REGION: str = "us-east-1"
    EMAIL_SENDER: str

    # Whitelist de dominios corporativos
    DOMAIN_WHITELIST: list[str] = ["blackrock.com", "jpmorgan.com"]

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()
