from aiogram import Router

from .user import user_router


def register_routers(router: Router):
    router.include_router(user_router)


__all__ = ["register_routers"]
