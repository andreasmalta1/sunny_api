"""Add quotes table

Revision ID: d51f8477490b
Revises: 
Create Date: 2023-01-07 18:00:46.940510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d51f8477490b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "quotes",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
            unique=True,
        ),
        sa.Column("quote", sa.String(), nullable=False),
        sa.Column("character", sa.String(), nullable=False),
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column("episode", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    pass


def downgrade() -> None:
    op.drop_table("quotes")
    pass
