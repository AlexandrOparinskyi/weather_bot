from typing import Dict

from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorHub
from sqlalchemy.dialects.mssql.aioodbc import dialect

from bot.utils import (get_weekdays_text,
                       get_user_by_id,
                       get_schedule)
from database import Weekday


async def getter_setting_home(i18n: TranslatorHub,
                              event_from_user: User,
                              **kwargs) -> Dict[str, str]:
    user = await get_user_by_id(event_from_user.id)
    weekdays = await get_weekdays_text(user)
    notification_days_setting = i18n.setting.notification.days.button()
    home_message = i18n.settings.home.text(
        username=user.first_name,
        current_city=user.user_settings.city,
        current_timezone=user.user_settings.timezone,
        weekdays=weekdays
    )

    return {"home_message": home_message,
            "notification_days_setting": notification_days_setting,
            "time_setting": i18n.setting.time.button(),
            "location_setting": i18n.setting.location.button()}


async def getter_notification_setting(i18n: TranslatorHub,
                                      event_from_user: User,
                                      **kwargs) -> Dict[str, str]:
    user = await get_user_by_id(event_from_user.id)
    day_buttons = list(sorted(user.user_schedules,
                              key=lambda item: item.day_of_week.value))

    return {"setting_notification_text": i18n.settings.notification.text(),
            "buttons": day_buttons,
            "enable_weekdays_button": i18n.enable.weekdays.button(),
            "disable_weekdays_button": i18n.disable.weekdays.button(),
            "back_button": i18n.back.button()}


async def getter_location_setting(i18n: TranslatorHub,
                                  event_from_user: User,
                                  **kwargs) -> Dict[str, str]:
    user = await get_user_by_id(event_from_user.id)
    setting_location_text = i18n.setting.location.text(
        current_city=user.user_settings.city
    )

    return {"setting_location_text": setting_location_text,
            "back_button": i18n.back.button()}


async def getter_time_setting(i18n: TranslatorHub,
                              event_from_user: User,
                              **kwargs) -> Dict[str, str]:
    user = await get_user_by_id(event_from_user.id)
    schedules = list(sorted(user.user_schedules,
                            key=lambda item: item.day_of_week.value))
    schedule = get_schedule(schedules)

    return {"setting_time_text": i18n.setting.time.text(schedule=schedule),
            "back_button": i18n.back.button(),
            "buttons": schedules,
            "toggle_time_days_button": i18n.toggle.time.days.button()}


async def getter_full_time_setting(i18n: TranslatorHub,
                                   event_from_user: User,
                                   **kwargs) -> Dict[str, str]:
    buttons = [(i, i) for i in ["6:00", "6:30", "7:00", "7:30", "8:00",
                                "8:30", "9:00", "9:30", "10:00", "12:00",
                                "15:00", "18:00"]]

    return {"setting_full_day_time_text": i18n.setting.full.day.time.text(),
            "back_button": i18n.back.button(),
            "buttons": buttons,}


async def getter_time_day_setting(i18n: TranslatorHub,
                                  event_from_user: User,
                                  dialog_manager: DialogManager,
                                  **kwargs) -> Dict[str, str]:
    user = await get_user_by_id(event_from_user.id)
    schedules = list(sorted(user.user_schedules,
                            key=lambda item: item.day_of_week.value))

    num_day = int(dialog_manager.dialog_data.get("num_day"))
    day = schedules[num_day]
    hours, minutes  = day.notification_time.hour, day.notification_time.minute

    setting_day_time_text = i18n.setting.day.time.text(
        day_name=day.day_of_week.display_name,
        current_time=f"{hours}:{minutes:02d}"
    )
    buttons = [(i, i) for i in ["6:00", "6:30", "7:00", "7:30", "8:00",
                                "8:30", "9:00", "9:30", "10:00", "12:00",
                                "15:00", "18:00"]]

    return {"setting_day_time_text": setting_day_time_text,
            "back_button": i18n.back.button(),
            "buttons": buttons}
