from aiogram.filters.callback_data import CallbackData


class ExampleData(CallbackData, prefix="example"):
    some_data: str
    user_id: int
