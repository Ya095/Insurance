"""create tariff table

Revision ID: 31c760d0b707
Revises: 
Create Date: 2024-11-18 10:07:37.869364

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "31c760d0b707"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tariffs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cargo_type", sa.String(), nullable=False),
        sa.Column("rate", sa.Float(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tariffs")),
        sa.UniqueConstraint(
            "cargo_type",
            "rate",
            "start_date",
            name=op.f("uq_tariffs_cargo_type"),
        ),
    )
    op.create_index(
        "idx_cargo_date", "tariffs", ["cargo_type", "start_date"], unique=False
    )


def downgrade() -> None:
    op.drop_index("idx_cargo_date", table_name="tariffs")
    op.drop_table("tariffs")
