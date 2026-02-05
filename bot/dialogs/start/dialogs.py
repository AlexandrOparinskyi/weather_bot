from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from bot.states import StartState
from .getters import (getter_start,
                      getter_info_setting,
                      getter_skip_settings)
from .handlers import (continue_button_to_view_info_setting,
                       start_skip_button,
                       start_setting_button)

start_dialog = Dialog(
    Window(
        Format("{start_message}"),
        Button(Format("{continue_button}"),
               id="button_view_info_setting",
               on_click=continue_button_to_view_info_setting),
        getter=getter_start,
        state=StartState.start
    ),
    Window(
        Format("{info_message}"),
        Button(Format("{setting_button}"),
               id="setting_button",
               on_click=start_setting_button),
        Button(Format("{skip_button}"),
               id="skip_button",
               on_click=start_skip_button),
        getter=getter_info_setting,
        state=StartState.info_setting
    ),
    Window(
        Format("{skip_setting_message}"),
        getter=getter_skip_settings,
        state=StartState.skip_setting
    )
)
