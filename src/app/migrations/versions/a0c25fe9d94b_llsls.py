"""llsls

Revision ID: a0c25fe9d94b
Revises: f22bca481bdb
Create Date: 2022-06-22 03:24:01.958599

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel             # NEW


# revision identifiers, used by Alembic.
revision = 'a0c25fe9d94b'
down_revision = 'f22bca481bdb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('metric', sa.Column('repo', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('metric', 'repo')
    # ### end Alembic commands ###
