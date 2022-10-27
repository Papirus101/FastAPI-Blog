from db.models.post import Post
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from db.models.user import User

from exceptions.db_exc import NotFoundException, NotOwnerException

async def create_post(db_session, author_id: int, **kwargs):
    new_post = Post(author_id=author_id, **kwargs)
    db_session.add(new_post)
    await db_session.commit()
    return new_post


async def get_post_by_id(db_session, post_id: int):
    sql = select(Post).where(Post.id == post_id)
    data = await db_session.execute(sql)
    try:
        post = data.one()
    except NoResultFound:
        raise NotFoundException('post was not found')
    return post[0]


async def get_all_posts(db_session, page: int = 0, limit: int = 6):
    sql = select(Post).join(User, Post.author_id == User.id).limit(limit).offset(page * limit)
    data = await db_session.execute(sql)
    posts = data.all()
    return [row[0].__dict__ for row in posts]


async def get_post_owner(db_session, post_id: int):
    sql = select(Post.author_id).where(Post.id == post_id)
    try:
        data = await db_session.execute(sql)
        post = data.one()
    except NoResultFound:
        raise NotFoundException('Post was not found')
    return post


async def update_post(db_session, post_id: int, user_id: int, **kwargs):
    post_owner = await get_post_owner(db_session, post_id)
    if post_owner.author_id != user_id:
        raise NotOwnerException
    sql = update(Post).values(**kwargs).where(Post.id == post_id)
    await db_session.execute(sql)
    await db_session.commit()