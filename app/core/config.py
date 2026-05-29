# Reads the .env file and sets environment variables

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ENVIRONMENT: str = "development"

    # RustFS / S3-compatible object storage
    S3_ENDPOINT_URL: str
    S3_BUCKET: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_REGION: str = "us-east-1"
    S3_PREFIX: str = "project-plans"
    S3_ADDRESSING_STYLE: str = "path"
    S3_PRESIGNED_URL_EXPIRY_SECONDS: int = 900

    PLAN_IMAGE_MAX_BYTES: int = 10_485_760

    class Config:
        env_file = ".env"


settings = Settings()  # pyright: ignore[reportCallIssue]
