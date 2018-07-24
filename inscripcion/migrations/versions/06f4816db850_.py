"""empty message

Revision ID: 06f4816db850
Revises: a13dcf7ce176
Create Date: 2018-07-24 17:44:28.973804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06f4816db850'
down_revision = 'a13dcf7ce176'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('preventas_camiseta', sa.Column('cedula', sa.String(length=10), nullable=False))


def downgrade():
    op.drop_column('preventas_camiseta', 'cedula')
