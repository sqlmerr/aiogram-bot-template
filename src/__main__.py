import os
import dotenv
import asyncio

from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from src.handlers import register_routers

from src.commands import set_bot_commands
from src.db import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

dotenv.load_dotenv()


async def main():
    logger.info("Initializing MongoDB")
    mongo = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(database=mongo.your_db_name, document_models=[User])

    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    await set_bot_commands(bot)

    router = register_routers()
    dp.include_router(router)

    logger.info('Starting Bot')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
