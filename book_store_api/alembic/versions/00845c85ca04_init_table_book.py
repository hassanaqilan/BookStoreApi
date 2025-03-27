"""Init table Book

Revision ID: 00845c85ca04
Revises: 53eb441d8b85
Create Date: 2025-03-23 10:27:55.587062

"""

from datetime import datetime
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column

# revision identifiers, used by Alembic.
revision: str = "00845c85ca04"
down_revision: Union[str, None] = "53eb441d8b85"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "book",
        Column("id", sa.Integer, primary_key=True, autoincrement=True),
        Column("title", sa.String, nullable=False),
        Column("author", sa.String, nullable=False),
        Column("is_borrowed", sa.Boolean, default=False),
        Column("borrowed_date", sa.DateTime, nullable=True),
        Column("borrowed_by", sa.Integer, nullable=True),
        Column("created_at", sa.DateTime, default=datetime.today()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("book")
