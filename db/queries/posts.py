from db.models.post import Category, Post, PostPhoto, UserPostsLikes
from sqlalchemy import select, update, insert, desc
from sqlalchemy.exc import NoResultFound
from db.models.user import User

from exceptions.db_exc import NotFoundException, NotOwnerException
from utils.utils import write_post_image

async def create_post(db_session, author_id: int, **kwargs):
    new_post = Post(author_id=author_id, **kwargs)
    db_session.add(new_post)
    await db_session.commit()
    return new_post


async def add_post_images(db_session, images: list, post_id: int, category_id: int):
    if not images:
        return
    for image in images:
        photo_pass = await write_post_image(image, category_id)
        db_session.add(PostPhoto(post_id=post_id, photo=photo_pass))
    await db_session.commit()
        

async def get_post_by_id(db_session, post_id: int):
    sql = select(Post).where(Post.id == post_id)
    data = await db_session.execute(sql)
    try:
        post = data.unique()
    except NoResultFound:
        raise NotFoundException('post was not found')
    return post.one()[0]


async def get_all_posts(db_session, category_id: int, page: int = 0, limit: int = 6):
    sql = select(Post).join(
        User, Post.author_id == User.id
        ).where(
            Post.category_id == category_id
            ).limit(limit).offset(page * limit).order_by(desc(Post.created_at))
    data = await db_session.execute(sql)
    posts = data.unique().all()
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
    
    
async def get_children_categories(db_session, category):
    child_list = []
    childs = await db_session.execute(category[0].children_categories)
    for category in childs:
        child_list.append(
            {
                'name': category[0].name,
                'id': category[0].id,
                'children_categories': await get_children_categories(db_session, category)
            }
        )
    return child_list if child_list else None
    
    
async def get_all_categories(db_session):
    sql = select(Category).where(Category.parrent_category_id == None)
    data = await db_session.execute(sql)
    categories = data.unique()
    if not categories:
        raise NotFoundException('Categories was not found')
    categories_list = []
    for category in categories:
        categories_list.append(
            {
                'name': category[0].name,
                'id': category[0].id,
                'children_categories': await get_children_categories(db_session, category)
            }
        )
    return categories_list


async def insert_category(db_session, name: str, parrent_category: int | None = None):
    new_category = Category(name=name, parrent_category_id=parrent_category)
    db_session.add(new_category)
    await db_session.commit()
    
    
async def like_post_by_id(db_session, post_id: int, user_id: int):
    sql = UserPostsLikes(user_id=user_id, post_id=post_id)
    db_session.add(sql)
    await db_session.commit()