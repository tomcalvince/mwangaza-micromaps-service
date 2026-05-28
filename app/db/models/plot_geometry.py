from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.db.models.geometry_history import GeometryHistory


class PlotGeometry(Base):
    __tablename__ = "plot_geometries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    external_plot_id: Mapped[int] = mapped_column(Integer, nullable=False)
    polygon_points: Mapped[dict] = mapped_column(JSONB, nullable=False)
    label_position: Mapped[dict] = mapped_column(JSONB, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    history: Mapped[list[GeometryHistory]] = relationship(
        "GeometryHistory",
        back_populates="plot_geometry",
        cascade="all, delete-orphan"
    )