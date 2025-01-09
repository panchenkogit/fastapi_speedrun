from sqlalchemy.ext.asyncio import AsyncSession, async_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import SQL_DB

Base = declarative_base()

engine = create_async_engine(SQL_DB)

async_session = async_sessionmaker(bind=engine, class_= AsyncSession, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
