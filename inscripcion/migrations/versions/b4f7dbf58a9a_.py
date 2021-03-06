"""empty message

Revision ID: b4f7dbf58a9a
Revises: 32d8259ad0ad
Create Date: 2018-05-19 22:11:49.044028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4f7dbf58a9a'
down_revision = '32d8259ad0ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre_usuario', sa.String(length=64), nullable=True),
    sa.Column('hashed_password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_nombre_usuario'), 'usuarios', ['nombre_usuario'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_usuarios_nombre_usuario'), table_name='usuarios')
    op.drop_table('usuarios')
    # ### end Alembic commands ###
