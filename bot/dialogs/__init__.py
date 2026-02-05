from aiogram import Router

from .settings import register_settings_dialogs
from .start import register_start_dialogs


def register_dialogs(router: Router):
    register_start_dialogs(router)
    register_settings_dialogs(router)
