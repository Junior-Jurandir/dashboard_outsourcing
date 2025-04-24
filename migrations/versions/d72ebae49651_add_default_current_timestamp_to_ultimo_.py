"""Add default current_timestamp to ultimo_update column in users table

Revision ID: d72ebae49651
Revises: 19b27422e62b
Create Date: 2025-04-23 20:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d72ebae49651"
down_revision = "19b27422e62b"
branch_labels = None
depends_on = None


def upgrade():
    # Alter 'ultimo_update' column to set default current timestamp
    op.alter_column(
        "users",
        "ultimo_update",
        existing_type=sa.DateTime(timezone=6),
        server_default=sa.text("CURRENT_TIMESTAMP"),
        existing_nullable=False,
    )


def downgrade():
    # Remove default from 'ultimo_update' column
    op.alter_column(
        "users",
        "ultimo_update",
        existing_type=sa.DateTime(timezone=6),
        server_default=None,
        existing_nullable=False,
    )
