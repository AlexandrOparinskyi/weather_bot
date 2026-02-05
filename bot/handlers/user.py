import asyncio
import logging

from aiogram import Router, Bot
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.services import get_recommendation_message
from bot.states import StartState, SettingsState
from bot.utils import (get_user_by_id,
                       create_user,
                       create_user_setting,
                       create_user_schedule)

user_router = Router()
logger = logging.getLogger(__name__)


@user_router.message(CommandStart())
async def command_start(message: Message,
                        dialog_manager: DialogManager):
    user = await get_user_by_id(message.from_user.id)

    if user is None:
        await create_user(message.from_user.id,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          message.from_user.username)
        await create_user_setting(message.from_user.id)
        await create_user_schedule(message.from_user.id)

        await dialog_manager.start(state=StartState.start)


@user_router.message(Command(commands="settings"))
async def command_settings(message: Message,
                           dialog_manager: DialogManager):
    user = await get_user_by_id(message.from_user.id)

    if user is None:
        return

    await dialog_manager.start(state=SettingsState.home)


@user_router.message(Command(commands="get_recommendations"))
async def get_weather(message: Message,
                      bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING
    )
    status_msg = await message.answer("🌤️ Получаю данные о погоде...")

    try:
        user = await get_user_by_id(message.from_user.id)
        if not user or not user.user_settings.city:
            await message.answer("❌ Укажите город в настройках!")
            return

        typing_task = asyncio.create_task(
            _keep_typing(bot, message.from_user.id)
        )
        text = await get_recommendation_message(user.user_settings.city)
        text = text.replace("###", "***")
        typing_task.cancel()
        await status_msg.delete()
        try:
            if "<b>" in text:
                logger.debug(f"Recommendation send with HTML parse mode")
                await message.answer(text,
                                     parse_mode=ParseMode.HTML)
                return
            elif "**" in text:
                logger.debug(f"Recommendation send with MARKDOWN parse mode")
                await message.answer(text,
                                     parse_mode=ParseMode.MARKDOWN)
                return
            else:
                logger.debug(f"Recommendation send without parse mode")
                await message.answer(text,
                                     parse_mode=None)
                return
        except Exception as err:
            logger.info(f"Parse mode is None: {err}")
            await message.answer(text,
                                 parse_mode=None)
            return
    except Exception as err:
        logger.error(f"Error send recommendation to "
                     f"user {message.from_user.id}: {err}")
        await message.answer("Ошибка получения данных")
        return


async def _keep_typing(bot, chat_id):
    try:
        while True:
            await bot.send_chat_action(
                chat_id=chat_id,
                action=ChatAction.TYPING
            )
            await asyncio.sleep(4)  # Обновляем каждые 4 секунды
    except asyncio.CancelledError:
        pass
    except Exception:
        pass
