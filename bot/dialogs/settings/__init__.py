from aiogram import Router

from .dialogs import settings_dialog


def register_settings_dialogs(router: Router):
    router.include_router(settings_dialog)
