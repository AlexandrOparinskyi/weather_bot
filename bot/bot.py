import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fluentogram import TranslatorHub

from bot.dialogs import register_dialogs
from bot.handlers import register_routers
from bot.middlewares import TranslatorRunnerMiddleware
from .sender import check_and_send_notifications

logger = logging.getLogger(__name__)


async def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()

    # Проверяем каждую минуту (можно изменить на нужный интервал)
    scheduler.add_job(
        check_and_send_notifications,
        'cron',
        minute='*',
        args=[bot]
    )

    scheduler.start()


async def main(
        token: str,
        hub: TranslatorHub,
        storage: RedisStorage | MemoryStorage = MemoryStorage()
) -> None:
    bot: Bot = Bot(token=token,
                   default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher(storage=storage)

    dp.update.middleware(TranslatorRunnerMiddleware())

    await bot.set_my_commands(
        commands=[
            BotCommand(
                command="settings",
                description="🔔 Настройки уведомлений"
            ),
            BotCommand(
                command="get_recommendations",
                description="❓ В чем сегодня идти"
            )
        ]
    )

    register_routers(dp)
    register_dialogs(dp)
    setup_dialogs(dp)

    try:
        await setup_scheduler(bot)
        await dp.start_polling(bot, _translator_hub=hub)
    except Exception as e:
        logger.error(f"Bot dont started: {e}")
