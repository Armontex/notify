import pytest
from datetime import datetime, timedelta, UTC
from sqlalchemy.exc import IntegrityError
from app.db.models import Notification, Record, User
from app.db.models.enums import RepeatStatus
from app.core.security.password import hash_password


def test_create_notification(session):
    user = User(username="TestUser", hash_password=hash_password("pwd"))
    record = Record(user=user, title="My Note")
    session.add_all([user, record])
    session.commit()
    session.refresh(record)

    notify_time = datetime.now(UTC) + timedelta(minutes=10)
    notification = Notification(record=record, notify_on=notify_time)
    session.add(notification)
    session.commit()
    session.refresh(notification)

    assert notification.id is not None
    assert notification.record == record
    assert notification.repeat == RepeatStatus.OFF
    assert notification.sent_at is None
    assert notification.notify_on.replace(tzinfo=None) == notify_time.replace(
        tzinfo=None)


def test_record_notification_relationship(session):
    user = User(username="Dana", hash_password=hash_password("pwd"))
    record = Record(user=user)
    notify_time = datetime.now(UTC)
    notification = Notification(record=record, notify_on=notify_time)

    session.add_all([user, record, notification])
    session.commit()
    session.refresh(record)
    session.refresh(notification)

    assert record.notification == notification
    assert notification.record == record


def test_notification_unique_record_id(session):
    user = User(username="UniqueTest", hash_password=hash_password("pwd"))
    record = Record(user=user)
    session.add_all([user, record])
    session.commit()

    notify_time = datetime.now(UTC)
    notification1 = Notification(record=record, notify_on=notify_time)
    session.add(notification1)
    session.commit()

    notification2 = Notification(record=record,
                                 notify_on=notify_time + timedelta(minutes=5))
    session.add(notification2)

    with pytest.raises(IntegrityError):
        session.commit()
