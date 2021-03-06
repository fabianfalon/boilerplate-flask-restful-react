"""empty message

Revision ID: ef1a770ebe95
Revises: 
Create Date: 2017-09-29 14:24:52.951768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ef1a770ebe95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=125), nullable=True),
    sa.Column('description', sa.String(length=125), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('audit_logs')
    op.add_column('audit', sa.Column('action', sa.CHAR(length=1), nullable=True))
    op.add_column('audit', sa.Column('after', sa.Text(), nullable=True))
    op.add_column('audit', sa.Column('before', sa.Text(), nullable=True))
    op.add_column('audit', sa.Column('date', sa.DateTime(), nullable=True))
    op.add_column('audit', sa.Column('object_id', sa.Integer(), nullable=True))
    op.add_column('audit', sa.Column('object_type', sa.String(length=30), nullable=True))
    op.drop_column('audit', 'description')
    op.drop_column('audit', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('audit', sa.Column('name', mysql.VARCHAR(length=125), nullable=True))
    op.add_column('audit', sa.Column('description', mysql.VARCHAR(length=125), nullable=True))
    op.drop_column('audit', 'object_type')
    op.drop_column('audit', 'object_id')
    op.drop_column('audit', 'date')
    op.drop_column('audit', 'before')
    op.drop_column('audit', 'after')
    op.drop_column('audit', 'action')
    op.create_table('audit_logs',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('object_type', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('object_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('before', mysql.TEXT(), nullable=True),
    sa.Column('after', mysql.TEXT(), nullable=True),
    sa.Column('date', mysql.DATETIME(), nullable=True),
    sa.Column('action', mysql.CHAR(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'latin1',
    mysql_engine=u'InnoDB'
    )
    op.drop_table('books')
    # ### end Alembic commands ###
