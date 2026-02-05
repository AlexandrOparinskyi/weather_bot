from database import User


async def get_weekdays_text(user: User) -> str:
    """
    Создает текст из дней недели текущего пользователя по его настройкам
    :param user: User
    :return: str
    """
    text = ""

    days = list(sorted(user.user_schedules,
                       key=lambda x: x.day_of_week.value))

    for day in days:
        hours = day.notification_time.hour
        minutes = day.notification_time.minute
        time_str = f"{hours}:{minutes:02d}"
        text += (f"• {day.status_icon} {day.day_of_week.display_name}: "
                 f"{time_str}\n")

    return text
