from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, VARCHAR
from ..base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .record import Record


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int | None] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(30),
                                          nullable=False,
                                          unique=True)
    hash_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    register_at: Mapped[datetime] = mapped_column(nullable=False,
                                                  default=func.now())

    records: Mapped[list[Record]] = relationship("Record",
                                                 back_populates="user")
