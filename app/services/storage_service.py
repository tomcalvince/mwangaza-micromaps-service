from __future__ import annotations

import mimetypes
from pathlib import PurePosixPath
import boto3
from botocore.client import Config

from app.core.config import settings


class StorageService:
    ALLOWED_CONTENT_TYPES = frozenset(
        {"image/png", "image/jpeg", "image/jpg", "image/webp"}
    )

    def __init__(self) -> None:
        config = Config(
            signature_version="s3v4",
            s3={"addressing_style": settings.S3_ADDRESSING_STYLE},
        )
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION,
            config=config,
        )
        self._bucket = settings.S3_BUCKET
        self._prefix = settings.S3_PREFIX.rstrip("/")

    def _object_key(self, project_id: int, filename: str | None, content_type: str) -> str:
        suffix = PurePosixPath(filename).suffix if filename else mimetypes.guess_extension(content_type)
        if not suffix:
            suffix = ".bin"
        unique_name = f"plan{suffix}"
        return f"{self._prefix}/{project_id}/{unique_name}"

    def upload(
        self,
        project_id: int,
        file_bytes: bytes,
        content_type: str,
        filename: str | None,
    ) -> str:
        object_key = self._object_key(project_id, filename, content_type)
        self._client.put_object(
            Bucket=self._bucket,
            Key=object_key,
            Body=file_bytes,
            ContentType=content_type,
        )
        return object_key

    def delete(self, object_key: str) -> None:
        self._client.delete_object(Bucket=self._bucket, Key=object_key)

    def get_presigned_url(self, object_key: str) -> str:
        return self._client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self._bucket, "Key": object_key},
            ExpiresIn=settings.S3_PRESIGNED_URL_EXPIRY_SECONDS,
        )
