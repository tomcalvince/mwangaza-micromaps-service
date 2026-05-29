from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ProjectPlanImageResponse(BaseModel):
    project_id: int
    object_key: str
    content_type: str
    original_filename: str | None
    size_bytes: int
    uploaded_at: datetime
    download_url: str

    model_config = {"from_attributes": True}
