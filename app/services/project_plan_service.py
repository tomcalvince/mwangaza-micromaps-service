from __future__ import annotations

import mimetypes

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.project_plan_asset import ProjectPlanAsset
from app.db.repositories.project_plan_repository import ProjectPlanRepository
from app.schemas.project_plan import ProjectPlanImageResponse
from app.services.storage_service import StorageService


class ProjectPlanService:
    def __init__(self, db: AsyncSession):
        self.repository = ProjectPlanRepository(db)
        self.storage = StorageService()
        self.db = db

    def _validate_upload(
        self, content_type: str | None, size: int, filename: str | None = None
    ) -> str:
        resolved = content_type
        if not resolved and filename:
            resolved = mimetypes.guess_type(filename)[0]
        if resolved == "image/jpg":
            resolved = "image/jpeg"
        if resolved not in StorageService.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image type. Allowed: {sorted(StorageService.ALLOWED_CONTENT_TYPES)}",
            )
        if size > settings.PLAN_IMAGE_MAX_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Image exceeds maximum size of {settings.PLAN_IMAGE_MAX_BYTES} bytes",
            )
        return resolved

    def _to_response(self, asset: ProjectPlanAsset) -> ProjectPlanImageResponse:
        return ProjectPlanImageResponse(
            project_id=asset.project_id,
            object_key=asset.object_key,
            content_type=asset.content_type,
            original_filename=asset.original_filename,
            size_bytes=asset.size_bytes,
            uploaded_at=asset.uploaded_at,
            download_url=self.storage.get_presigned_url(asset.object_key),
        )

    async def upload_plan_image(
        self, project_id: int, file: UploadFile
    ) -> ProjectPlanImageResponse:
        file_bytes = await file.read()
        content_type = self._validate_upload(
            file.content_type, len(file_bytes), file.filename
        )

        existing = await self.repository.get_by_project_id(project_id)
        if existing:
            self.storage.delete(existing.object_key)

        object_key = self.storage.upload(
            project_id=project_id,
            file_bytes=file_bytes,
            content_type=content_type,
            filename=file.filename,
        )
        asset = await self.repository.upsert(
            project_id=project_id,
            object_key=object_key,
            content_type=content_type,
            original_filename=file.filename,
            size_bytes=len(file_bytes),
        )
        await self.db.commit()
        await self.db.refresh(asset)
        return self._to_response(asset)

    async def get_plan_image(self, project_id: int) -> ProjectPlanImageResponse:
        asset = await self.repository.get_by_project_id(project_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No plan image found for project {project_id}",
            )
        return self._to_response(asset)

    async def delete_plan_image(self, project_id: int) -> None:
        asset = await self.repository.get_by_project_id(project_id)
        if not asset:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No plan image found for project {project_id}",
            )
        self.storage.delete(asset.object_key)
        await self.repository.delete(asset)
        await self.db.commit()
