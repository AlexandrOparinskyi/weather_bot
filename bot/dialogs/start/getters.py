from typing import Dict

from aiogram.types import User
from fluentogram import TranslatorHub


async def getter_start(i18n: TranslatorHub,
                       event_from_user: User,
                       **kwargs) -> Dict[str, str]:
    username = event_from_user.first_name

    return {"start_message": i18n.start.message.text(username=username),
            "continue_button": i18n.acquaintance.button()}


async def getter_info_setting(i18n: TranslatorHub,
                              **kwargs) -> Dict[str, str]:
    return {"info_message": i18n.start.info.setting.text(),
            "setting_button": i18n.settings.button(),
            "skip_button": i18n.skip.button()}


async def getter_skip_settings(i18n: TranslatorHub,
                               **kwargs) -> Dict[str, str]:
    return {"skip_setting_message": i18n.start.skip.setting.message.text()}
