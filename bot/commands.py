from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="start")
    ]  # add your commands here

    return await bot.set_my_commands(
        commands,
        BotCommandScopeDefault()  # or another scope https://core.telegram.org/type/BotCommandScope
    )
