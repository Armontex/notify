from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Enum
from ..base import Base
from .enums import RepeatStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .record import Record


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    record_id: Mapped[int] = mapped_column(Integer,
                                           ForeignKey("records.id"),
                                           unique=True,
                                           nullable=False)
    notify_on: Mapped[datetime] = mapped_column(nullable=False)
    repeat: Mapped[RepeatStatus] = mapped_column(Enum(RepeatStatus),
                                                 nullable=False,
                                                 default=RepeatStatus.OFF)
    sent_at: Mapped[datetime | None]

    record: Mapped[Record] = relationship("Record",
                                          back_populates="notification",
                                          uselist=False,
                                          lazy="selectin")
