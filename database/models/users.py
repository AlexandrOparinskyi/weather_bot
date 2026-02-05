from datetime import datetime
from typing import Optional

from sqlalchemy import func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_banned: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=func.now())

    user_settings = relationship("UserSetting",
                                 back_populates="user",
                                 uselist=False,
                                 lazy="joined")
    user_schedules = relationship("UserSchedule",
                                  back_populates="user",
                                  lazy="selectin")
