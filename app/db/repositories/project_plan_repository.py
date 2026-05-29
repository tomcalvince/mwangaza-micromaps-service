from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project_plan_asset import ProjectPlanAsset


class ProjectPlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_project_id(self, project_id: int) -> ProjectPlanAsset | None:
        result = await self.db.execute(
            select(ProjectPlanAsset).where(ProjectPlanAsset.project_id == project_id)
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        project_id: int,
        object_key: str,
        content_type: str,
        original_filename: str | None,
        size_bytes: int,
    ) -> ProjectPlanAsset:
        existing = await self.get_by_project_id(project_id)
        if existing:
            existing.object_key = object_key
            existing.content_type = content_type
            existing.original_filename = original_filename
            existing.size_bytes = size_bytes
            existing.uploaded_at = datetime.now(timezone.utc)
            await self.db.flush()
            return existing

        asset = ProjectPlanAsset(
            project_id=project_id,
            object_key=object_key,
            content_type=content_type,
            original_filename=original_filename,
            size_bytes=size_bytes,
        )
        self.db.add(asset)
        await self.db.flush()
        return asset

    async def delete(self, asset: ProjectPlanAsset) -> None:
        await self.db.delete(asset)
        await self.db.flush()
