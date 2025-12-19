from app.db.models.user import User
from app.core.security.password import verify_password, hash_password

def test_create_user(session):

    username = "SomeUser"
    password = "Password"

    user = User(
        username=username,
        hash_password=hash_password(password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id is not None
    assert user.username == username
    assert verify_password(password, user.hash_password) 
    assert user.register_at is not None