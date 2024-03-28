from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from bot.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.DB_URL.get_secret_value(), echo=settings.echo)
session_maker = async_sessionmaker(engine)
