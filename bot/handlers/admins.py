from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from config import Config, load_config

admin_router = Router()
config: Config = load_config()


@admin_router.message(Command(commands="send_mailing"))
async def send_mailing(message: Message,
                       dialog_manager: DialogManager):
    if message.from_user.id != config.tg_bot.admin_id:
        return

