import settings
import json

from fastapi import APIRouter, Response, HTTPException, Body, Depends, Request
from db.queries.users import get_user_by_login, insert_new_client, update_user_data

from depends.auth.jwt_bearer import OAuth2PasswordBearerCookie
from depends.auth.password_hash import hash_password, validate_password
from depends.auth.jwt_handler import signJWT, get_login_by_token
from db.session import get_session
from models.user_model import TokenScheme, UserBaseScheme, UserLoginScheme, UserRegisterScheme, UserUpdateSheme
from utils.utils import get_redis, get_user_token

users_router = APIRouter(
        prefix='/user',
        tags=['users']
        )

@users_router.post('/create_user', status_code=201, response_model=TokenScheme)
async def user_signup(response: Response, user: UserRegisterScheme = Body(),
        session = Depends(get_session)):
    user.password = await hash_password(user.password)
    new_user = await insert_new_client(session, **user.__dict__)
    if new_user is not None and 'error' in new_user:
        raise HTTPException(400, new_user)
    token = await signJWT(user.login)
    if settings.AUTH_TYPE == 'cookie':
        response.set_cookie('Authorization', f"Bearer {token['access_token']}")
    return {'Authorization': f"Bearer {token['access_token']}"}


@users_router.post('/login', status_code=200, response_model=TokenScheme)
async def user_login(response: Response, user: UserLoginScheme = Body(),
        db_session = Depends(get_session)):
    user_db = await get_user_by_login(db_session, user.login)
    if not await validate_password(user.password, user_db.password):
        raise HTTPException(400, 'Login or password is not valid')
    token = await signJWT(user.login)
    if settings.AUTH_TYPE == 'cookie':
        response.set_cookie('Authorization', f"Bearer {token['access_token']}")
    return {'Authorization': f"Bearer {token['access_token']}"}


@users_router.patch('/update_user', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def user_update_data(request: Request, response: Response, user: UserUpdateSheme = Body(),
        db_session = Depends(get_session), redis = Depends(get_redis)):
    user_data = {k:v for k, v in user.__dict__.items() if v is not None}
    if 'password' in user_data:
        user_data['password'] = await hash_password(user_data['password'])
    user_token = get_user_token(request)
    user_login = await get_login_by_token(user_token)
    await update_user_data(db_session, user_login, **user_data)
    await redis.delete(user_login)
    if 'login' in user_data:
        user_token = await signJWT(user_data['login'])
        user_token = user_token['access_token']
        if settings.AUTH_TYPE == 'cookie':
            response.set_cookie('Authorization', f"Bearer {user_token}")
    return {'Authorization': f"Bearer {user_token}"}


@users_router.get('/get_user', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def get_user(request: Request, redis = Depends(get_redis),
        session = Depends(get_session)):
    user_token = get_user_token(request)
    user_login = await get_login_by_token(user_token)
    cache = await redis.get(user_login)
    if cache is not None:
        return json.loads(cache)
    user = await get_user_by_login(session, user_login)
    user = dict(user)
    del user['password']
    await redis.set(user_login, json.dumps(dict(user)))
    return user

@users_router.get('/logout', status_code=200, dependencies=[Depends(OAuth2PasswordBearerCookie())])
async def logout_user(response: Response):
    if settings.AUTH_TYPE == 'cookie':
        response.delete_cookie('Authorization')
    return {'bye': 'bye'}
