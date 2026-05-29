"""multi plot unique index and project plan assets

Revision ID: a1b2c3d4e5f6
Revises: 9cd5f8362b0b
Create Date: 2026-05-28 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "9cd5f8362b0b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "uq_plot_geometries_project_external_active",
        "plot_geometries",
        ["project_id", "external_plot_id"],
        unique=True,
        postgresql_where=sa.text("is_deleted = false"),
    )
    op.create_table(
        "project_plan_assets",
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("object_key", sa.String(length=512), nullable=False),
        sa.Column("content_type", sa.String(length=128), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=True),
        sa.Column("size_bytes", sa.BigInteger(), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("project_id"),
    )


def downgrade() -> None:
    op.drop_table("project_plan_assets")
    op.drop_index(
        "uq_plot_geometries_project_external_active",
        table_name="plot_geometries",
    )
