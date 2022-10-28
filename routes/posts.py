from fastapi import APIRouter, Body, Depends, UploadFile, HTTPException
from db.queries.posts import add_post_images, create_post, get_all_categories, get_all_posts, get_post_by_id, insert_category, update_post
from db.session import get_session
from depends.auth.jwt_handler import get_user

from models.post_model import CreateCategorySheme, CreatePostScheme, EditPostScheme, ListCategoriesScheme, ListPostsSheme, ViewPostScheme

posts_router = APIRouter(
        prefix='/posts',
        tags=['posts']
        )

@posts_router.post('/create_post', response_model=ViewPostScheme, status_code=201)
async def user_signup(
    images: list[UploadFile] | None = None,
    new_post: CreatePostScheme = Body(),
    user: dict = Depends(get_user),
    session = Depends(get_session)
    ):
    post = await create_post(session, user['id'], **dict(new_post))
    await add_post_images(session, images, post.id, new_post.category_id)
    post = await get_post_by_id(session, post.id)
    return post


@posts_router.get('/get_post', status_code=200, response_model=ViewPostScheme)
async def get_post(post_id: int, session = Depends(get_session)):
    post = await get_post_by_id(session, post_id)
    return post


@posts_router.get('/get_posts', response_model=ListPostsSheme, status_code=200)
async def get_posts(category_id: int, page: int = 0, limit: int = 6, session = Depends(get_session)):
    posts = await get_all_posts(session, category_id, page, limit)
    return {'posts': posts}


@posts_router.patch('/update_post', status_code=200, response_model=ViewPostScheme)
async def update_user_post(session = Depends(get_session), user = Depends(get_user), post_edited: EditPostScheme = Body()):
    post_id = post_edited.__dict__.pop('post_id')
    params = {k: v for k, v in post_edited.__dict__.items() if v is not None}
    await update_post(session, post_id, user['id'], **params)
    post = await get_post_by_id(session, post_id)
    return post


@posts_router.get('/get_categories', status_code=200, response_model=ListCategoriesScheme)
async def get_categories(session = Depends(get_session)):
    categoies = await get_all_categories(session)
    return {'categories': categoies}


@posts_router.post('/new_category', status_code=201)
async def create_category(session = Depends(get_session), category: CreateCategorySheme = Body()):
    await insert_category(session, **dict(category))