"""Add users table

Revision ID: 4175ae91fbfc
Revises: d51f8477490b
Create Date: 2023-01-07 18:33:51.034084

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4175ae91fbfc"
down_revision = "d51f8477490b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
