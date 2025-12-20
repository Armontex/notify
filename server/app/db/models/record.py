from __future__ import annotations
from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import VARCHAR, ForeignKey, func, Integer, event
from ..base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .notification import Notification
    from .user import User


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer,
                                         ForeignKey("users.id"),
                                         nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR(255), default="Новая запись")
    content: Mapped[str] = mapped_column(VARCHAR(10000),
                                         nullable=False,
                                         default='')
    created_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False,
                                                 default=func.now(),
                                                 onupdate=func.now())

    user: Mapped[User] = relationship("User",
                                      back_populates="records",
                                      lazy="selectin")
    notification: Mapped[Notification | None] = relationship(
        "Notification",
        back_populates="record",
        uselist=False,
        lazy="selectin")


@event.listens_for(Record, "before_update", propagate=True)
def update_record_updated_at(mapper, connection, target):
    target.updated_at = datetime.now(UTC)
