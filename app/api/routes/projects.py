# POSTS /projects/{id} registration if needed, and GET /projects/{id} for fetching project details
from __future__ import annotations
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.plot_service import PlotService

router = APIRouter(prefix="/projects", tags=["projects"])


def get_plot_service(db: AsyncSession = Depends(get_db)) -> PlotService:
    return PlotService(db)


@router.get("/{project_id}/summary")
async def get_project_summary(
    project_id: int,
    service: PlotService = Depends(get_plot_service),
):
    plots = await service.get_project_plots(project_id)
    return {
        "project_id": project_id,
        "mapped_plots": len(plots),
    }