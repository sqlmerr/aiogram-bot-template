from typing import List, Union
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup


def url_builder(*buttons: List[str], per_row: Union[List[int], int] = 1) -> InlineKeyboardMarkup:
    """easy generation of inline buttons with url

    :argument:
        *buttons (List[str, str])
        per_row (int, optional): how many buttons will be per row? Defaults to 1.

    :example:
        url_builder(
            ["Google", "https://google.com"],
            ["Yandex", "https://ya.ru"],
            per_row=2
        )

    :returns:
        InlineKeyboardMarkup: inline buttons
    """

    b = InlineKeyboardBuilder()
    for btn in buttons:
        b.button(text=btn[0], url=btn[1])

    if isinstance(per_row, int):
        per_row = [per_row]
    b.adjust(*per_row)
    return b.as_markup()


def inline_builder(*buttons: List[str], per_row: Union[List[int], int] = 1) -> InlineKeyboardMarkup:
    """easy generation of inline buttons with callback data

    :argument:
        *buttons (list[str, str])
        per_row (int, optional): how many buttons will be per row? Defaults to 1.

    :example:
        inline_builder(
            ["shop", "open_shop:123456789"],
            ["button", "callback_data"],
            per_row=2
        )

    :returns:
        InlineKeyboardMarkup: inline buttons
    """

    b = InlineKeyboardBuilder()
    for btn in buttons:
        b.button(text=btn[0], callback_data=btn[1])

    if isinstance(per_row, int):
        per_row = [per_row]
    b.adjust(*per_row)
    return b.as_markup()
