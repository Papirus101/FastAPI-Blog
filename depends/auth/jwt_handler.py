import time
import os
from fastapi import HTTPException

import jwt
from jwt.algorithms import get_default_algorithms

from db.queries.users import get_user_by_login

from load_config import auth_config, Auth


async def token_response(token: str, expires: int) -> dict:
    return {
        'access_token': token,
        'expires': expires
    }


async def signJWT(user_info: str) -> dict:
    config: Auth = auth_config()
    token = jwt.encode(
        {
            'user_info': user_info,
            'expires': int(time.time() + 7200)
        },
        config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM)
    return await token_response(token, int(time.time() + 7200))


async def decodeJWT(token: str) -> str | None:
    config: Auth = auth_config()
    if isinstance(token, list):
        token = token[0]
    token = token.encode('utf-8')
    decode_token = jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
    return decode_token if decode_token['expires'] >= time.time() else None


async def get_user_by_token(token, db_session):
    user_login = await get_login_by_token(token)
    return await get_user_by_login(db_session, user_login)


async def get_login_by_token(token: str) -> str:
    config: Auth = auth_config()
    if isinstance(token, list):
        token = token[1]
    token = token.encode('utf-8')
    decode_token = jwt.decode(token, config.JWT_SECRET, config.JWT_ALGORITHM)
    if decode_token.get('user_info') is None:
        raise HTTPException(403)
    return decode_token['user_info']

