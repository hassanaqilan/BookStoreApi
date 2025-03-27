"""Init table Member

Revision ID: 53eb441d8b85
Revises:
Create Date: 2025-03-23 10:23:13.930163

"""

from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column

# revision identifiers, used by Alembic.
revision: str = "53eb441d8b85"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "member",
        Column("id", sa.Integer, primary_key=True),
        Column("name", sa.String, nullable=False),
        Column("email", sa.String, unique=True, nullable=False),
        Column("created_at", sa.DateTime, default=datetime.today()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("member")
