from __future__ import annotations
from .record import Record
from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, func, DateTime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30),
                                          nullable=False,
                                          unique=True)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    register_at: Mapped[DateTime] = mapped_column(
        nullable=False, default=func.now())

    records: Mapped[list[Record]] = relationship(Record, back_populates="user")