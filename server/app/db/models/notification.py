from __future__ import annotations
from .enums import RepeatStatus
from .user import User
from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func, Integer, Enum


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    record_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("records.id"),
                                           unique=True,
                                           nullable=False)
    notify_on: Mapped[DateTime] = mapped_column(nullable=False,
                                                 default=func.now())
    repeat: Mapped[RepeatStatus] = mapped_column(Enum(RepeatStatus), nullable=False,
                                                 default=RepeatStatus.OFF)
    sent_at: Mapped[DateTime]
    
    record: Mapped[User] = relationship(User, back_populates="notification")
