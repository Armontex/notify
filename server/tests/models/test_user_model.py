import pytest
from datetime import datetime
from app.db.models import User, Record
from app.core.security.password import verify_password, hash_password


def test_create_user(session):

    username = "SomeUser"
    password = "Password"

    user = User(username=username, hash_password=hash_password(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.username == username
    assert user.telegram_id is None
    assert verify_password(password, user.hash_password)
    assert user.register_at is not None
    assert user.records == []


def test_user_records_relation(session):
    user = User(username="Alice", hash_password=hash_password("secret"))
    record1 = Record(title="Note 1", user=user)
    record2 = Record(title="Note 2", user=user)

    session.add(user)
    session.add_all([record1, record2])
    session.commit()
    session.refresh(user)

    assert len(user.records) == 2
    assert all(r.user == user for r in user.records)


def test_unique_username(session):
    user1 = User(username="Bob", hash_password=hash_password("p1"))
    user2 = User(username="Bob", hash_password=hash_password("p2"))

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(Exception):
        session.commit()
        session.rollback()


def test_user_defaults(session):
    user = User(username="Charlie", hash_password=hash_password("123"))
    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.telegram_id is None
    assert isinstance(user.register_at, datetime)
