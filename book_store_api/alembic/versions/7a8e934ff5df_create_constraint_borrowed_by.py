"""Create constraint borrowed_by

Revision ID: 7a8e934ff5df
Revises: 00845c85ca04
Create Date: 2025-03-23 10:33:09.615319

"""

from typing import Sequence, Union

from alembic import op

# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a8e934ff5df"
down_revision: Union[str, None] = "00845c85ca04"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key(
        "fk_borrowed_by_member_id",
        "book",
        "member",
        ["borrowed_by"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_borrowed_by_member_id", "book")
