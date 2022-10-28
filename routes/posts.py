from fastapi import APIRouter, Body, Depends, UploadFile
from db.queries.posts import create_post, get_all_categories, get_all_posts, get_post_by_id, insert_category, update_post
from db.session import get_session
from depends.auth.jwt_bearer import OAuth2PasswordBearerCookie
from depends.auth.jwt_handler import get_user

from models.post_model import CategoryViewSheme, CreateCategorySheme, CreatePostScheme, EditPostScheme, ListCategoriesScheme, ListPostsSheme, ViewPostScheme

posts_router = APIRouter(
        prefix='/posts',
        tags=['posts']
        )

@posts_router.post('/create_post', response_model=ViewPostScheme, status_code=201, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def user_signup(new_post: CreatePostScheme = Body(), user: dict = Depends(get_user), session = Depends(get_session)):
    post = await create_post(session, user['id'], **dict(new_post))
    post = await get_post_by_id(session, post.id)
    return post


@posts_router.get('/get_post', status_code=200, response_model=ViewPostScheme, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def get_post(post_id: int, session = Depends(get_session)):
    post = await get_post_by_id(session, post_id)
    return post


@posts_router.get('/get_posts', response_model=ListPostsSheme, status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def get_posts(page: int = 0, limit: int = 6, session = Depends(get_session)):
    posts = await get_all_posts(session, page, limit)
    return {'posts': posts}


@posts_router.patch('/update_post', status_code=200, response_model=ViewPostScheme, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def update_user_post(session = Depends(get_session), user = Depends(get_user), post_edited: EditPostScheme = Body()):
    post_id = post_edited.__dict__.pop('post_id')
    params = {k: v for k, v in post_edited.__dict__.items() if v is not None}
    await update_post(session, post_id, user['id'], **params)
    post = await get_post_by_id(session, post_id)
    return post


@posts_router.get('/get_categories', status_code=200, response_model=ListCategoriesScheme, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def get_categories(session = Depends(get_session)):
    categoies = await get_all_categories(session)
    return {'categories': categoies}


@posts_router.post('/new_category', status_code=201, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def create_category(session = Depends(get_session), category: CreateCategorySheme = Body()):
    await insert_category(session, **dict(category))