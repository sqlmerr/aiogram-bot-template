from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.db import User
from src.fluent_loader import get_fluent_localization


class LocalizationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user: User = data["user"]
        try:
            fluent = get_fluent_localization(user.language)
        except (FileNotFoundError, AttributeError):
            fluent = get_fluent_localization("en")

        data["fluent"] = fluent
        return await handler(event, data)
