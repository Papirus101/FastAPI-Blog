"""set default category post

Revision ID: b541a172a223
Revises: b551cb17ca02
Create Date: 2022-10-28 16:11:00.179094

"""
from alembic import op
import sqlalchemy as sa

from db.models.post import Post, Category

# revision identifiers, used by Alembic.
revision = 'b541a172a223'
down_revision = 'b551cb17ca02'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)
    
    first_category = Category(name='Общая категория')
    session.add(first_category)
    session.commit()
    
    for post in session.query(Post):
        post.category_id = first_category.id
    session.commit()
    
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'category_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
