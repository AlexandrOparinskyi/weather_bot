from datetime import time

from sqlalchemy import insert, select, update

from database import get_async_session, UserSchedule, Weekday


async def create_user_schedule(user_id: int) -> None:
    created_values = [
        {"user_id": user_id,
         "day_of_week": day}
        for day in Weekday
    ]

    async with get_async_session() as session:
        await session.execute(insert(UserSchedule), created_values)
        await session.commit()


async def toggle_notification_status(user_id: int,
                                     day_of_week: int) -> None:
    async with get_async_session() as session:
        weekday_enum = Weekday(day_of_week)

        day = await session.scalar(select(UserSchedule).where(
            UserSchedule.user_id == user_id,
            UserSchedule.day_of_week == weekday_enum
        ))

        if day:
            day.is_enabled = not day.is_enabled
            await session.commit()


async def toggle_time_notification(user_id: int,
                                   day_of_week: int,
                                   n_time: str) -> None:
    async with get_async_session() as session:
        try:
            hour, minute = n_time.split(':')
        except ValueError:
            hour = n_time
            minute = 0
        weekday_enum = Weekday(day_of_week)
        notification_time = time(int(hour), int(minute))

        await session.execute(update(UserSchedule).where(
            UserSchedule.user_id == user_id,
            UserSchedule.day_of_week == weekday_enum
        ).values(
            notification_time=notification_time
        ))
        await session.commit()


async def toggle_full_time_notification(user_id: int,
                                        n_time: str) -> None:
    async with get_async_session() as session:
        try:
            hour, minute = n_time.split(':')
        except ValueError:
            hour = n_time
            minute = 0
        notification_time = time(int(hour), int(minute))

        schedules = await session.scalars(select(UserSchedule).where(
            UserSchedule.user_id == user_id
        ))

        for schedule in schedules:
            schedule.notification_time = notification_time

        await session.commit()


async def enable_weekdays(user_id: int) -> None:
    async with get_async_session() as session:
        schedules = await session.scalars(select(UserSchedule).where(
            UserSchedule.user_id == user_id
        ))

        for schedule in schedules:
            schedule.is_enabled = True

        await session.commit()


async def disable_weekdays(user_id: int) -> None:
    async with get_async_session() as session:
        schedules = await session.scalars(select(UserSchedule).where(
            UserSchedule.user_id == user_id
        ))

        for schedule in schedules:
            schedule.is_enabled = False

        await session.commit()
