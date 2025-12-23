import pytest
from sqlalchemy.exc import IntegrityError
from app.db.repos import UserRepository
from app.core.security.password import hash_password, verify_password
from app.core.exc import UserNotFoundError


async def test_create_user(session):
    user_repo = UserRepository(session)

    username = "SomeUsername"
    password = "somePassword"
    hashed = hash_password(password)

    user = await user_repo.create(username, hashed)

    assert user.id is not None
    assert user.username == username
    assert user.telegram_id is None
    assert verify_password(password, user.hash_password)
    assert user.register_at is not None
    assert user.records == []


async def test_create_multiple_users_with_one_username(session):
    user_repo = UserRepository(session)

    username = "Dodo"
    password1 = hash_password("pswrd1")
    password2 = hash_password("pswrd2")

    await user_repo.create(username, password1)

    with pytest.raises(IntegrityError):
        await user_repo.create(username, password2)


async def test_get_by_id(session):
    user_repo = UserRepository(session)
    user = await user_repo.create("name", hash_password("password"))
    user2 = await user_repo.get_by_id(user.id)

    assert user2 is not None

    assert user.id == user2.id
    assert user.telegram_id == user2.telegram_id
    assert user.hash_password == user2.hash_password
    assert user.register_at == user2.register_at
    assert user.records == user2.records


async def test_get_unknown_by_id(session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_id(0)
    assert user is None


async def test_get_by_username(session):
    user_repo = UserRepository(session)
    user = await user_repo.create("name", hash_password("password"))
    user2 = await user_repo.get_by_username(user.username)

    assert user2 is not None


async def test_get_by_unknown_username(session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_username("some")
    assert user is None


async def test_set_telegram_id(session):
    user_repo = UserRepository(session)
    user = await user_repo.create("name", hash_password("password"))
    tg_id = 123
    await user_repo.set_telegram_id(user, tg_id)
    assert user.telegram_id == tg_id


async def test_set_telegram_id_by_id(session):
    user_repo = UserRepository(session)
    user = await user_repo.create("name", hash_password("password"))
    tg_id = 123
    await user_repo.set_telegram_id_by_id(user.id, tg_id)
    await session.refresh(user)

    assert user.telegram_id == tg_id


async def test_set_telegram_id_by_unknown_id(session):
    user_repo = UserRepository(session)

    with pytest.raises(UserNotFoundError):
        await user_repo.set_telegram_id_by_id(0, 1)
