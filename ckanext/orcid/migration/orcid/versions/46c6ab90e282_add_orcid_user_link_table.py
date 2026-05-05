"""Add orcid_user_link table

Revision ID: 46c6ab90e282
Revises:
Create Date: 2026-05-04 18:00:04.026537
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "46c6ab90e282"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "orcid_user_link",
        sa.Column("orcid_id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("user.id"), nullable=False),
        sa.Column("access_token", sa.String, nullable=False),
        sa.Column(
            "created",
            sa.DateTime,
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
    )


def downgrade():
    op.drop_table("orcid_user_link")
