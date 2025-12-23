from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .base import Repository
from ..models import User
from ...core.exc import UserNotFoundError


class UserRepository(Repository):

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return await self._session.scalar(stmt)

    async def set_telegram_id_by_id(self, user_id: int,
                                    telegram_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User not found: id={user_id}")
        user.telegram_id = telegram_id
        await self._session.flush()

    async def set_telegram_id(self, user: User, telegram_id: int) -> None:
        user.telegram_id = telegram_id
        await self._session.flush()

    async def create(self, username: str, hashed_password: str) -> User:
        user = User(username=username, hash_password=hashed_password)
        self._session.add(user)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise e
        await self._session.refresh(user)
        return user

# TODO: Узнать про Unit-of-work (Система управления транзакциями)