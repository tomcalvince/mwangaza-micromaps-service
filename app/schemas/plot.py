# Pydantic requests and responses for plot geometry endpoints, including validation and serialization of geojson data.
from __future__ import annotations
import uuid
from datetime import datetime
from pydantic import BaseModel, field_validator

class PolygonPoint(BaseModel):
    x: float
    y: float

    @field_validator("x", "y")
    @classmethod
    def must_be_normalized(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("Coordinates must be normalized between 0.0 and 1.0")
        return v
    

class LabelPosition(PolygonPoint):
    x: float
    y: float

    @field_validator("x", "y")
    @classmethod
    def must_be_normalized(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("Label position coordinates must be normalized between 0.0 and 1.0")
        return v
    
# ------Request schemas------
class PlotGeometryCreate(BaseModel):
    external_plot_id: int
    polygon_points: list[PolygonPoint]
    label_position: PolygonPoint | None = None

    @field_validator("polygon_points")
    @classmethod
    def must_have_minimum_points(cls, v: list[PolygonPoint] | None) -> list[PolygonPoint] | None:
        if v is not None and len(v) < 3:
            raise ValueError("A polygon must have at least 3 points")
        return v
    
class PlotGeometryUpdate(BaseModel):
    polygon_points: list[PolygonPoint] | None = None
    label_position: PolygonPoint | None = None

    @field_validator("polygon_points")
    @classmethod
    def must_have_minimum_points(cls, v: list[PolygonPoint] | None) -> list[PolygonPoint] | None:
        if v is not None and len(v) < 3:
            raise ValueError("A polygon must have at least 3 points")
        return v
    
# -------Response Schema------
class PlotGeometryResponse(BaseModel):
    id: uuid.UUID
    project_id: int
    external_plot_id: int
    polygon_points: list[PolygonPoint]
    label_position: LabelPosition | None = None
    updated_at: datetime

    model_config = {"from_attributes": True}

class PlotGeometryListResponse(BaseModel):
    project_id: int
    total: int
    plots: list[PlotGeometryResponse]
