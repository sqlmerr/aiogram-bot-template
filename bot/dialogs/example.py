from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


class ExampleDialog(StatesGroup):
    greeting = State()


async def show_alert(c: CallbackQuery, _: Button, manager: DialogManager):
    await c.answer("❗️ Test", show_alert=True, cache_time=0)
    await c.message.delete()
    await manager.done()


ui = Dialog(
    Window(
        Const("<b>📎 Example dialog</b>"),
        Button(Const("Your button text"), id="test_button", on_click=show_alert),
        state=ExampleDialog.greeting,
    ),
)