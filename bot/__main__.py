import os
import asyncio

from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentCompileCore

from bot.handlers import register_routers
from bot.middlewares import (
    UserMiddleware,
    ThrottlingMiddleware
)
from bot.config import settings

from bot.commands import set_bot_commands
from bot.db import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    logger.info("Initializing MongoDB")
    mongo = AsyncIOMotorClient(settings.MONGO_URL.get_secret_value())
    await init_beanie(database=mongo.your_db_name, document_models=[User])

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(lambda: logger.info("Bot successfully started"))  # or create function with your custom logic

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())

    await set_bot_commands(bot)

    router = register_routers()
    dp.include_router(router)

    i18n_middleware = I18nMiddleware(
        core=FluentCompileCore(
            path="bot/locales/{locale}/"
        )
    )
    i18n_middleware.setup(dispatcher=dp)

    logger.info('Starting Bot')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
