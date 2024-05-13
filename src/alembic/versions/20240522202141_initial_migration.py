"""Initial migration

Revision ID: a6b594b1ec36
Revises:
Create Date: 2024-05-13 20:21:41.905546

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "a6b594b1ec36"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "address",
        sa.Column("country", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("city", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("street", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_address_id"), "address", ["id"], unique=False)
    op.create_table(
        "client",
        sa.Column("client_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("client_surname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("birthday", sa.Date(), nullable=False),
        sa.Column("gender", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("registration_date", sa.DateTime(), nullable=False),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("address_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["address.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_client_id"), "client", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_client_id"), table_name="client")
    op.drop_table("client")
    op.drop_index(op.f("ix_address_id"), table_name="address")
    op.drop_table("address")
    # ### end Alembic commands ###
