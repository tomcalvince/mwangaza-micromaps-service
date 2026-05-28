from __future__ import annotations
import uuid
from datetime import datetime, timezone
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.plot_geometry import PlotGeometry
from app.db.models.geometry_history import GeometryHistory


class PlotRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_by_project(self, project_id: int) -> list[PlotGeometry]:
        result = await self.db.execute(
            select(PlotGeometry).where(
                and_(
                    PlotGeometry.project_id == project_id,
                    PlotGeometry.is_deleted == False
                )
            )
        )
        return result.scalars().all()

    async def get_by_id(self, plot_id: uuid.UUID, project_id: int) -> PlotGeometry | None:
        result = await self.db.execute(
            select(PlotGeometry).where(
                and_(
                    PlotGeometry.id == plot_id,
                    PlotGeometry.project_id == project_id,
                    PlotGeometry.is_deleted == False
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_by_external_plot_id(self, external_plot_id: int, project_id: int) -> PlotGeometry | None:
        result = await self.db.execute(
            select(PlotGeometry).where(
                and_(
                    PlotGeometry.external_plot_id == external_plot_id,
                    PlotGeometry.project_id == project_id,
                    PlotGeometry.is_deleted == False
                )
            )
        )
        return result.scalar_one_or_none()

    async def create(self, project_id: int, external_plot_id: int, polygon_points: list, label_position: dict | None) -> PlotGeometry:
        plot = PlotGeometry(
            project_id=project_id,
            external_plot_id=external_plot_id,
            polygon_points=[p.model_dump() for p in polygon_points],
            label_position=label_position.model_dump() if label_position else None,
        )
        self.db.add(plot)
        await self.db.flush()
        return plot

    async def save_history(self, plot: PlotGeometry) -> None:
        snapshot = GeometryHistory(
            plot_geometry_id=plot.id,
            polygon_snapshot=plot.polygon_points,
        )
        self.db.add(snapshot)

    async def update(self, plot: PlotGeometry, polygon_points: list | None, label_position: dict | None) -> PlotGeometry:
        await self.save_history(plot)
        if polygon_points is not None:
            plot.polygon_points = [p.model_dump() for p in polygon_points]
        if label_position is not None:
            plot.label_position = label_position.model_dump()
        plot.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        return plot

    async def soft_delete(self, plot: PlotGeometry) -> None:
        await self.save_history(plot)
        plot.is_deleted = True
        await self.db.flush()