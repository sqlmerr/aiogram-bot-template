import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentCompileCore

from bot.handlers import register_routers
from bot.middlewares import UserMiddleware, ThrottlingMiddleware
from bot.config import settings

from bot.commands import set_bot_commands
from bot.db import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger()


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.startup.register(
        lambda: logger.info("Bot successfully started")
    )  # or create function with your custom logic

    dp.message.middleware(ThrottlingMiddleware())
    dp.callback_query.middleware(ThrottlingMiddleware())

    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())

    router = register_routers()
    dp.include_router(router)

    i18n_middleware = I18nMiddleware(
        core=FluentCompileCore(path="bot/locales/{locale}/")
    )
    i18n_middleware.setup(dispatcher=dp)

    return dp


async def init_db() -> None:
    mongo = AsyncIOMotorClient(settings.MONGO_URL.get_secret_value())
    await init_beanie(database=mongo.your_db_name, document_models=[User])


async def main():
    logger.info("Initializing MongoDB")
    await init_db()

    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = create_dispatcher()

    await set_bot_commands(bot)

    logger.info("Starting Bot")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def on_webhook_startup(bot: Bot) -> None:
    await init_db()

    await bot.set_webhook(
        f"{settings.BASE_WEBHOOK_URL}{settings.WEBHOOK_PATH}",
        secret_token=settings.WEBHOOK_SECRET,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if settings.use_webhooks:
        bot = Bot(
            token=settings.BOT_TOKEN.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        dp = create_dispatcher()
        dp.startup.register(on_webhook_startup)

        app = web.Application()
        webhook_requests_hander = SimpleRequestHandler(
            dispatcher=dp, bot=bot, secret_token=settings.WEBHOOK_SECRET
        )
        webhook_requests_hander.register(app, path=settings.WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)

        web.run_app(app, host=settings.WEB_SERVER_HOST, port=settings.WEB_SERVER_PORT)
    else:
        asyncio.run(main())
