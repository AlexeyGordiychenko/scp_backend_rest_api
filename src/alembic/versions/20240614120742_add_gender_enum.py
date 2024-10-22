"""Add gender enum

Revision ID: 5e7375a47af8
Revises: b4989fb54c75
Create Date: 2024-06-14 12:07:42.230053

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "5e7375a47af8"
down_revision: Union[str, None] = "b4989fb54c75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

gender_type = sa.Enum("female", "male", "other", "not_given", name="gender")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    gender_type.create(op.get_bind())
    op.alter_column(
        "client",
        "gender",
        existing_type=sa.VARCHAR(),
        type_=gender_type,
        existing_nullable=False,
        postgresql_using="gender::gender",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "client",
        "gender",
        existing_type=gender_type,
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    gender_type.drop(op.get_bind())
    # ### end Alembic commands ###
