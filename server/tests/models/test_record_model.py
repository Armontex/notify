from datetime import datetime
from app.db.models import Record, User, Notification
from app.core.security.password import hash_password


def test_create_record(session):
    user = User(username="Alice", hash_password=hash_password("secret"))
    session.add(user)
    session.commit()
    session.refresh(user)

    record = Record(user=user, title="Test Record", content="Some content")
    session.add(record)
    session.commit()
    session.refresh(record)

    assert record.id is not None
    assert record.title == "Test Record"
    assert record.content == "Some content"
    assert isinstance(record.created_at, datetime)
    assert isinstance(record.updated_at, datetime)
    assert record.user == user
    assert record.notification is None


def test_user_record_relationship(session):
    user = User(username="Bob", hash_password=hash_password("pass"))
    record1 = Record(title="Note 1", user=user)
    record2 = Record(title="Note 2", user=user)

    session.add(user)
    session.add_all([record1, record2])
    session.commit()
    session.refresh(user)

    assert len(user.records) == 2
    assert record1 in user.records
    assert record2 in user.records


def test_record_updated_at_on_change(session):
    user = User(username="Charlie", hash_password=hash_password("123"))
    record = Record(user=user, title="Original")
    session.add_all([user, record])
    session.commit()
    session.refresh(record)

    original_updated_at = record.updated_at
    record.title = "Updated"
    session.commit()
    session.refresh(record)

    assert record.updated_at > original_updated_at


def test_record_notification_relation(session):
    user = User(username="Dana", hash_password=hash_password("pwd"))
    record = Record(user=user)
    notification = Notification(record=record,
                                notify_on=datetime(year=2025, month=12,
                                                   day=31))

    session.add_all([user, record, notification])
    session.commit()
    session.refresh(record)
    session.refresh(notification)

    assert record.notification == notification
    assert notification.record == record
