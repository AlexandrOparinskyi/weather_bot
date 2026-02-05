from aiogram import Router

from .user import user_router
from .admins import admin_router


def register_routers(router: Router):
    router.include_router(user_router)
    router.include_router(admin_router)


__all__ = ["register_routers"]
