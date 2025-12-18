from ..base import Base
from datetime import datetime, UTC
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30),
                                          nullable=False,
                                          unique=True)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    register_at: Mapped[datetime] = mapped_column(
        nullable=False, default=lambda: datetime.now(UTC))
