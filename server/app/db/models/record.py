from __future__ import annotations

from .notification import Notification
from .user import User
from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, func, Integer


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), default="Новая запись")
    content: Mapped[str] = mapped_column(String(10000), default='')
    created_at: Mapped[DateTime] = mapped_column(nullable=False,
                                                 default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(nullable=False,
                                                 default=func.now(),
                                                 onupdate=func.now())
    
    user: Mapped[User] = relationship(User, back_populates="records")
    notification: Mapped[Notification] = relationship(Notification, back_populates="record")