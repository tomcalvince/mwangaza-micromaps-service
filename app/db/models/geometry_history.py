from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.db.models.plot_geometry import PlotGeometry


class GeometryHistory(Base):
    __tablename__ = "geometry_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plot_geometry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("plot_geometries.id"),
        nullable=False,
        index=True
    )
    polygon_snapshot: Mapped[dict] = mapped_column(JSONB, nullable=False)
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    plot_geometry: Mapped[PlotGeometry] = relationship(
        "PlotGeometry",
        back_populates="history"
    )