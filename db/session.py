from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from db.base import Base
from settings import ASYNC_DB_LINK, SYNC_DB_LINK

from load_config import db_config, DB

config: DB = db_config()
 
engine = create_async_engine(ASYNC_DB_LINK.format(
    db_user=config.user,
    db_pass=config.password,
    db_host=config.host,
    db_port=config.port,
    db_name=config.db_name
    ))

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

sync_engin = create_engine(SYNC_DB_LINK.format(
    db_user=config.user,
    db_pass=config.password,
    db_host=config.host,
    db_port=config.port,
    db_name=config.db_name
    ))

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
