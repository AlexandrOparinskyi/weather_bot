from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode


async def check_enter_time(message: Message, dialog_manager: DialogManager):
    i18n = dialog_manager.middleware_data.get("i18n")

    if not message.text:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(i18n.error.time.text())
        return False

    time_str = message.text.strip()

    try:
        # Вариант 1: Формат "ЧЧ:ММ" (12:30)
        if ':' in time_str:
            time_parts = time_str.split(':')
            if len(time_parts) != 2:
                dialog_manager.show_mode = ShowMode.NO_UPDATE
                await message.answer(i18n.error.time.text())
                return False

            hour_str, minute_str = time_parts

            # Проверяем что обе части - цифры
            if not (hour_str.isdigit() and minute_str.isdigit()):
                dialog_manager.show_mode = ShowMode.NO_UPDATE
                await message.answer(i18n.error.time.text())
                return False

            hour = int(hour_str)
            minute = int(minute_str)

            # Проверяем длину минут (должны быть 2 цифры)
            if len(minute_str) != 2:
                dialog_manager.show_mode = ShowMode.NO_UPDATE
                await message.answer(i18n.error.time.text())
                return False

        # Вариант 2: Только число (7, 12, 23)
        elif time_str.isdigit():
            hour = int(time_str)
            minute = 0  # Устанавливаем минуты по умолчанию

            # Автоматически форматируем минуты как "00"
            minute_str = "00"

        else:
            dialog_manager.show_mode = ShowMode.NO_UPDATE
            await message.answer(i18n.error.time.text())
            return False

        # Проверяем диапазоны для любого формата
        if hour < 0 or hour > 23:
            dialog_manager.show_mode = ShowMode.NO_UPDATE
            await message.answer(i18n.error.time.text())
            return False

        if minute < 0 or minute > 59:
            dialog_manager.show_mode = ShowMode.NO_UPDATE
            await message.answer(i18n.error.time.text())
            return False

        # Все проверки пройдены
        return True

    except ValueError:
        dialog_manager.show_mode = ShowMode.NO_UPDATE
        await message.answer(i18n.error.time.text())
        return False


