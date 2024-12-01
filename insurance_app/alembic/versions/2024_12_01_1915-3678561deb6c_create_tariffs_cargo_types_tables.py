"""create tariffs, cargo_types tables

Revision ID: 3678561deb6c
Revises: 
Create Date: 2024-12-01 19:15:11.739348

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3678561deb6c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cargo_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cargo_types")),
    )
    op.create_index(
        op.f("ix_cargo_types_name"), "cargo_types", ["name"], unique=True
    )
    op.create_table(
        "tariffs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("cargo_type", sa.Integer(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cargo_type"],
            ["cargo_types.id"],
            name=op.f("fk_tariffs_cargo_type_cargo_types"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tariffs")),
        sa.UniqueConstraint(
            "cargo_type",
            "rate",
            "start_date",
            name=op.f("uq_tariffs_cargo_type"),
        ),
    )


def downgrade() -> None:
    op.drop_table("tariffs")
    op.drop_index(op.f("ix_cargo_types_name"), table_name="cargo_types")
    op.drop_table("cargo_types")
