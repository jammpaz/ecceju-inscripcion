"""empty message

Revision ID: a795d999adb8
Revises: 77ab2fce2113
Create Date: 2018-06-14 02:56:56.214057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a795d999adb8'
down_revision = '77ab2fce2113'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participantes', sa.Column('monto', sa.Numeric(precision=8, scale=2), nullable=True))
    op.add_column('participantes', sa.Column('numero_deposito', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participantes', 'numero_deposito')
    op.drop_column('participantes', 'monto')
    # ### end Alembic commands ###
