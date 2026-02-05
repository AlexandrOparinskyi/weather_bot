from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Select, Row
from aiogram_dialog.widgets.text import Format

from bot.states import SettingsState
from .filters import check_enter_time
from .getters import (getter_setting_home,
                      getter_notification_setting,
                      getter_location_setting,
                      getter_time_setting,
                      getter_time_day_setting,
                      getter_full_time_setting)
from .handlers import (notification_days_setting,
                       toggle_day_notification,
                       enable_weekdays_button,
                       disable_weekdays_button,
                       back_button_to_home,
                       time_setting,
                       location_setting,
                       send_location,
                       error_send_location,
                       back_button_to_day_time_setting,
                       select_day_setting,
                       select_time_setting,
                       select_full_time,
                       toggle_full_time,
                       enter_time_setting,
                       enter_full_time_setting)

settings_dialog = Dialog(
    Window(
        Format("{home_message}"),
        Button(Format("{notification_days_setting}"),
               id="notification_days_setting",
               on_click=notification_days_setting),
        Button(Format("{time_setting}"),
               id="time_setting",
               on_click=time_setting),
        Button(Format("{location_setting}"),
               id="location_setting",
               on_click=location_setting),
        getter=getter_setting_home,
        state=SettingsState.home
    ),
    Window(
        Format("{setting_notification_text}"),
        Group(Select(id="days_toggle",
                     item_id_getter=lambda x: x.day_of_week.value,
                     items="buttons",
                     text=Format("{item.status_icon} "
                                 "{item.day_of_week.short_name}"),
                     on_click=toggle_day_notification),
              width=4),
        Row(Button(Format("{enable_weekdays_button}"),
                   id="enable_weekdays_button",
                   on_click=enable_weekdays_button),
            Button(Format("{disable_weekdays_button}"),
                   id="disable_weekdays_button",
                   on_click=disable_weekdays_button)),
        Button(Format("{back_button}"),
               id="back_button",
               on_click=back_button_to_home),
        getter=getter_notification_setting,
        state=SettingsState.notification_setting
    ),
    Window(
        Format("{setting_location_text}"),
        MessageInput(func=send_location,
                     content_types=ContentType.LOCATION),
        MessageInput(func=error_send_location,
                     content_types=ContentType.ANY),
        Button(Format("{back_button}"),
               id="back_button",
               on_click=back_button_to_home),
        getter=getter_location_setting,
        state=SettingsState.location_setting
    ),
    Window(
        Format("{setting_time_text}"),
        Select(text=Format("{item.day_of_week.short_name}"),
               id="day_of_week",
               item_id_getter=lambda x: x.day_of_week.value,
               items="buttons",
               on_click=select_day_setting),
        Button(text=Format("{toggle_time_days_button}"),
               id="toggle_time_days_button",
               on_click=select_full_time),
        Button(Format("{back_button}"),
               id="back_button",
               on_click=back_button_to_home),
        getter=getter_time_setting,
        state=SettingsState.time_setting
    ),
    Window(
        Format("{setting_full_day_time_text}"),
        MessageInput(func=enter_full_time_setting,
                     filter=check_enter_time,
                     content_types=ContentType.TEXT),
        Group(Select(text=Format("{item[0]}"),
                     id="time",
                     item_id_getter=lambda x: x[1],
                     items="buttons",
                     on_click=toggle_full_time),
              width=4),
        Button(Format("{back_button}"),
               id="back_button",
               on_click=back_button_to_day_time_setting),
        getter=getter_full_time_setting,
        state=SettingsState.time_full_setting
    ),
    Window(
        Format("{setting_day_time_text}"),
        MessageInput(func=enter_time_setting,
                     filter=check_enter_time,
                     content_types=ContentType.TEXT),
        Group(Select(text=Format("{item[0]}"),
                     id="time",
                     item_id_getter=lambda x: x[1],
                     items="buttons",
                     on_click=select_time_setting),
              width=4),
        Button(Format("{back_button}"),
               id="back_button",
               on_click=back_button_to_day_time_setting),
        getter=getter_time_day_setting,
        state=SettingsState.time_day_setting
    )
)
