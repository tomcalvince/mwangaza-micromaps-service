# Project-level endpoints: summary and plan image storage (RustFS).
from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.project_plan import ProjectPlanImageResponse
from app.services.plot_service import PlotService
from app.services.project_plan_service import ProjectPlanService

router = APIRouter(prefix="/projects", tags=["projects"])


def get_plot_service(db: AsyncSession = Depends(get_db)) -> PlotService:
    return PlotService(db)


def get_project_plan_service(db: AsyncSession = Depends(get_db)) -> ProjectPlanService:
    return ProjectPlanService(db)


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


@router.post(
    "/{project_id}/plan-image",
    response_model=ProjectPlanImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_plan_image(
    project_id: int,
    file: UploadFile = File(...),
    service: ProjectPlanService = Depends(get_project_plan_service),
):
    return await service.upload_plan_image(project_id, file)


@router.get("/{project_id}/plan-image", response_model=ProjectPlanImageResponse)
async def get_plan_image(
    project_id: int,
    service: ProjectPlanService = Depends(get_project_plan_service),
):
    return await service.get_plan_image(project_id)


@router.delete("/{project_id}/plan-image", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan_image(
    project_id: int,
    service: ProjectPlanService = Depends(get_project_plan_service),
):
    await service.delete_plan_image(project_id)
