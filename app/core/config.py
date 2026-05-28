# Reads the .env file and sets environment variables

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    ENVIRONMENT: str = "development"
    # Add other configuration variables as needed

    class Config:
        env_file = ".env"  

settings = Settings() # pyright: ignore[reportCallIssue]