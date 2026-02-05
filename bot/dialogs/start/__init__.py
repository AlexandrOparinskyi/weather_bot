from aiogram import Router

from .dialogs import start_dialog


def register_start_dialogs(router: Router):
    router.include_router(start_dialog)
