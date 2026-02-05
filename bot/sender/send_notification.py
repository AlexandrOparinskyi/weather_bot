from datetime import datetime
import time
from aiogram import Bot
from aiogram.enums import ParseMode
from asyncpg.pgproto.pgproto import timedelta

from bot.services import get_recommendation_message
from bot.utils import get_all_users
from database.models import User, Weekday
import logging


async def send_scheduled_notification(bot: Bot, user: User) -> bool:
    """
    Отправляет уведомление пользователю, если включены уведомления на сегодня
    """
    try:
        # Проверяем, есть ли настройки у пользователя
        if not user.user_settings:
            return False

        # Проверяем, включены ли вообще уведомления
        if not user.user_settings.notifications_enabled:
            return False

        # Получаем текущий день недели
        current_weekday = Weekday(datetime.now().weekday())

        # Ищем расписание на сегодня
        today_schedule = None
        for schedule in user.user_schedules:
            if schedule.day_of_week == current_weekday:
                today_schedule = schedule
                break

        # Если нет расписания на сегодня или отключено
        if not today_schedule or not today_schedule.is_enabled:
            return False

        # Получаем рекомендации по погоде
        message_text = await get_recommendation_message(
            user.user_settings.city
        )

        # Отправляем сообщение
        await bot.send_message(
            chat_id=user.id,
            text=message_text,
            parse_mode=ParseMode.MARKDOWN
        )

        return True

    except Exception as e:
        logging.error(f"❌ Ошибка отправки уведомления пользователю "
                      f"{user.id}: {e}")
        return False


async def should_send_notification_now(user: User) -> bool:
    """
    Проверяет, нужно ли отправлять уведомление прямо сейчас
    """
    try:
        # Проверяем базовые условия
        if not user.user_settings or not user.user_settings.notifications_enabled:
            return False

        # Текущий день и время
        now_utc = datetime.utcnow()  # Берём время UTC
        current_weekday = Weekday(now_utc.weekday())

        # Извлекаем смещение (например, "UTC+3" -> 3)
        timezone_offset = int(user.user_settings.timezone.split("+")[1])

        # Прибавляем смещение к UTC
        user_local_time = now_utc + timedelta(hours=timezone_offset)
        current_time = user_local_time.time().replace(second=0, microsecond=0)

        # Ищем расписание на сегодня
        for schedule in user.user_schedules:
            logging.info(schedule.notification_time)
            if (schedule.day_of_week == current_weekday and
                    schedule.is_enabled and
                    schedule.notification_time == current_time):
                logging.info("true")
                return True

        return False

    except Exception as e:
        logging.error(f"❌ Ошибка проверки уведомления: {e}")
        return False


# Пример использования в планировщике
async def check_and_send_notifications(bot: Bot):
    """
    Функция для планировщика: проверяет всех пользователей и отправляет уведомления
    """
    users = await get_all_users()  # Получаем всех пользователей
    sent_count = 0
    for i, user in enumerate(users):
        logging.info(f"Пользователь {i}")
        if i % 20 == 0:
            time.sleep(1)
        if await should_send_notification_now(user):
            if await send_scheduled_notification(bot, user):
                sent_count += 1

    logging.info(f"📨 Отправлено уведомлений: {sent_count}")
    return sent_count
