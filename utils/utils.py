from fastapi import HTTPException
import settings
import aioredis
import os


def get_user_token(response) -> str:
    token = ''
    if settings.AUTH_TYPE == 'data':
        _, token = response.headers.get('Authorization').split()
    elif settings.AUTH_TYPE == 'cookie':
        try:
            _, token = response.cookies.get('Authorization').split()
        except AttributeError:
            raise HTTPException(403)
    return token


async def get_redis():
    redis = await aioredis.from_url(f"redis://{os.getenv('REDIS_HOST')}")
    return redis
