from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column
from bot.db.core import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    language: Mapped[str] = mapped_column(default="en")
