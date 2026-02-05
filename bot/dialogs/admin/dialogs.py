from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button

from .getters import getter_confirm_msg
from .handlers import enter_message, confirm_msg_button
from bot.states import AdminState

admin_dialog = Dialog(
    Window(
        Const("Введите сообщение"),
        MessageInput(func=enter_message,
                     content_types=ContentType.TEXT),
        state=AdminState.enter_message
    ),
    Window(
        Format("{text}"),
        Button(text=Const("Подтверждаю"),
               id="confirm_button",
               on_click=confirm_msg_button),
        getter=getter_confirm_msg,
        state=AdminState.confirm_message
    )
)