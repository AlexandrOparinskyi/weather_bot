from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from bot.states import StartState, SettingsState


async def continue_button_to_view_info_setting(callback: CallbackQuery,
                                               button: Button,
                                               dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartState.info_setting)


async def start_skip_button(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager):
    await dialog_manager.switch_to(state=StartState.skip_setting)


async def start_setting_button(callback: CallbackQuery,
                               button: Button,
                               dialog_manager: DialogManager):
    await dialog_manager.start(state=SettingsState.home)
