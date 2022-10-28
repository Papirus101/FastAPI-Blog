import os
import aiofiles
import aioredis
import settings
from datetime import datetime
from datetime import date
from fastapi import HTTPException, Request


def get_user_token(request: Request) -> str:
    token = ''
    if settings.AUTH_TYPE == 'data':
        _, token = request.headers.get('Authorization').split()
    elif settings.AUTH_TYPE == 'cookie':
           token = request.cookies.get('Authorization')
           if token is None or len(token) < 1:
               raise HTTPException(403)
           _, token = token.split()
    return token


async def get_redis():
    redis = await aioredis.from_url(f"redis://{os.getenv('REDIS_HOST')}")
    return redis


async def write_post_image(image, category):
    ext = image.filename.split('.')[-1]
    filename = str(int(datetime.timestamp(datetime.now())))
    year = date.today().year
    month = date.today().month
    file_path = settings.POST_PHOTO_PATH.format(category=category, year=year, month=month, filename=filename, ext=ext)
    directory = '/'.join(file_path.split('/')[:-1])
    if not os.path.isdir(directory):
        os.makedirs(directory)
    async with aiofiles.open(file_path, "wb") as out_file:
            photo_content = await image.read()
            await out_file.write(photo_content)
    return file_path