from aiogram import Router
from .dialogs import admin_dialog

def register_admin_dialog(router: Router):
    router.include_router(admin_dialog)
