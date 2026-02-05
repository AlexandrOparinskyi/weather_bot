import asyncio
import logging
from math import lgamma

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.states import AdminState
from bot.utils import get_all_users
from config import Config, load_config

config: Config = load_config()
logger = logging.getLogger(__name__)

async def enter_message(message: Message,
                        widget: MessageInput,
                        dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(msg=message.text)

    await dialog_manager.switch_to(state=AdminState.confirm_message)


async def confirm_msg_button(callback: CallbackQuery,
                             button: Button,
                             dialog_manager: DialogManager):
    msg = dialog_manager.dialog_data.get("msg")
    bot: Bot = dialog_manager.middleware_data.get("bot")
    users = await get_all_users()
    counter = 0

    for num, user in enumerate(users, 1):
        if num % 15 == 0:
            await asyncio.sleep(1)
        if user.id == config.tg_bot.admin_id:
            continue
        try:
            await bot.send_message(user.id,
                                   msg)
            counter += 1
        except Exception as err:
            logger.debug(f"User {user.id} id blocked: {err}")
            continue

    await callback.answer(f"Разослано {counter} пользователям")
    await callback.message.delete()
    await dialog_manager.done()
    logger.info(f"MAILING. Message send to {counter} users")
