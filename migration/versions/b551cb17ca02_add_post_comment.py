"""add post comment

Revision ID: b551cb17ca02
Revises: f96a21e4a87a
Create Date: 2022-10-28 16:10:10.398637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b551cb17ca02'
down_revision = 'f96a21e4a87a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('parrent_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parrent_category_id'], ['categories.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('posts', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'categories', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'category_id')
    op.drop_table('categories')
    # ### end Alembic commands ###
