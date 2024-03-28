from loguru import logger

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_i18n import I18nContext

from bot.db import User

router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message, user: User, i18n: I18nContext):
    if not user:
        user = User(
            user_id=message.from_user.id
        )

        await user.insert()
        logger.debug(f"registered new user with id {message.from_user.id}")

    await message.reply(f"<b>Hello, {message.from_user.full_name}</b>")
    await message.answer(i18n.get("example", some="hi"))
