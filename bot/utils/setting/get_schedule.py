from typing import List

from database import UserSchedule


def get_schedule(schedules: List[UserSchedule]) -> str:
    text = ""
    for schedule in schedules:
        hours = schedule.notification_time.hour
        minutes = schedule.notification_time.minute
        time_str = f"{hours}:{minutes:02d}"
        text += f"• {schedule.day_of_week.display_name} - {time_str}\n"

    return text
