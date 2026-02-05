from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserSetting(Base):
    __tablename__ = 'user_settings'

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id",
                                                    ondelete="CASCADE"),
                                         unique=True)

    city: Mapped[Optional[str]] = mapped_column(default="Москва",
                                                nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(default="UTC+3",
                                                    nullable=True)
    notifications_enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime,
                                                 default=func.now(),
                                                 onupdate=func.now())

    user = relationship("User", back_populates="user_settings")
