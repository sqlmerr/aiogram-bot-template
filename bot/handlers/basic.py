import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import DialogManager

from aiogram_i18n import I18nContext

from bot.db import User
from bot.dialogs.example import ExampleDialog

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message, user: User, i18n: I18nContext):
    if not user:
        user = User(user_id=message.from_user.id)

        await user.insert()
        logger.debug(f"registered new user with id {message.from_user.id}")
    await message.reply(
        f"<b>Hello, {message.from_user.full_name}</b>.\nTo start dialog run click button below",
        reply_markup=InlineKeyboardBuilder()
        .button(text="Open dialog", callback_data="open_dialog")
        .as_markup(),
    )
    await message.answer(i18n.get("example", some="hi"))

    # To set locale with i18n use:
    #   await i18n.set_locale("ru")
    # To get locale use:
    #   i18n.core.get_locale()


@router.callback_query(F.data == "open_dialog")
async def dialog(callback: CallbackQuery, dialog_manager: DialogManager):
    await callback.answer("Opening dialog...")
    logger.debug(f"opening dialog for user {callback.from_user.id}")
    await dialog_manager.start(ExampleDialog.greeting)
