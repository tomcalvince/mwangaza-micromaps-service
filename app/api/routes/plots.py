# All plot geometry endpoints.
from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.plot import (
    PlotGeometryCreate,
    PlotGeometryUpdate,
    PlotGeometryResponse,
    PlotGeometryListResponse,
)
from app.services.plot_service import PlotService

router = APIRouter(prefix="/projects/{project_id}/plots", tags=["plots"])


def get_plot_service(db: AsyncSession = Depends(get_db)) -> PlotService:
    return PlotService(db)


@router.get("", response_model=PlotGeometryListResponse)
async def get_project_plots(
    project_id: int,
    service: PlotService = Depends(get_plot_service),
):
    plots = await service.get_project_plots(project_id)
    return PlotGeometryListResponse(
        project_id=project_id,
        total=len(plots),
        plots=plots,
    )


@router.get("/{plot_id}", response_model=PlotGeometryResponse)
async def get_plot_geometry(
    project_id: int,
    plot_id: uuid.UUID,
    service: PlotService = Depends(get_plot_service),
):
    return await service.get_plot(project_id, plot_id)


@router.post("", response_model=PlotGeometryResponse, status_code=status.HTTP_201_CREATED)
async def create_plot_geometry(
    project_id: int,
    payload: PlotGeometryCreate,
    service: PlotService = Depends(get_plot_service),
):
    return await service.create_plot(project_id, payload)


@router.put("/{plot_id}", response_model=PlotGeometryResponse)
async def update_plot_geometry(
    project_id: int,
    plot_id: uuid.UUID,
    payload: PlotGeometryUpdate,
    service: PlotService = Depends(get_plot_service),
):
    return await service.update_plot(project_id, plot_id, payload)


@router.delete("/{plot_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plot_geometry(
    project_id: int,
    plot_id: uuid.UUID,
    service: PlotService = Depends(get_plot_service),
):
    await service.delete_plot(project_id, plot_id)