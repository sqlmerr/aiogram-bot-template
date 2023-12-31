from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from cachetools import TTLCache


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, throttle_time: float = 1.5):
        self.cache = TTLCache(maxsize=10_000, ttl=throttle_time)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if event.from_user.id in self.cache:
            return
        else:
            self.cache[event.from_user.id] = None

        return await handler(event, data)
