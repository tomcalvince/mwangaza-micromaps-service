# Business logic for handling plot geometry operations, including validation, transformation, and interaction with the database repository. This service is called by the API routes to perform the necessary operations on plot geometries.
from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.plot_repository import PlotRepository
from app.db.models import PlotGeometry
from app.schemas.plot import PlotGeometryCreate, PlotGeometryUpdate

class PlotService:

    def __init__(self, db: AsyncSession):
        self.repository = PlotRepository(db)
        self.db = db

    async def get_project_plots(self, project_id: int) -> list[PlotGeometry]:
        return await self.repository.get_all_by_project(project_id)
    
    async def create_plot(self, project_id: int, data: PlotGeometryCreate):
        existing = await self.repository.get_all_by_project(project_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Plot geometries already exist for this project. Please update the existing geometry instead of creating a new one."
            )
        plot = await self.repository.create(
            project_id=project_id,
            external_plot_id=data.external_plot_id,
            polygon_points=data.polygon_points,
            label_position=data.label_position
        )

        await self.db.commit()
        await self.db.refresh(plot)
        return plot
    
    async def update_plot(self, project_id: int, plot_id: uuid.UUID, data: PlotGeometryUpdate) -> PlotGeometry:
        plot = await self.repository.get_by_id(plot_id, project_id)
        if not plot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plot geometry {plot_id} not found in project {project_id}"
            )
        plot = await self.repository.update(
            plot=plot,
            polygon_points=data.polygon_points,
            label_position=data.label_position,
        )
        await self.db.commit()
        await self.db.refresh(plot)
        return plot

    async def delete_plot(self, project_id: int, plot_id: uuid.UUID) -> None:
        plot = await self.repository.get_by_id(plot_id, project_id)
        if not plot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plot geometry {plot_id} not found in project {project_id}"
            )
        await self.repository.soft_delete(plot)
        await self.db.commit()