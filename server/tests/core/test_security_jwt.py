import pytest
import secrets
from datetime import timedelta
from app.core.config import settings
from app.core.security.jwt import jwt_service, JWTService

def create_other_jwt_service() -> JWTService:
    secret_key = secrets.token_hex(32)
    return JWTService(
        secret_key=secret_key,
        algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

@pytest.mark.parametrize("user_id", [0, 1, 42, 999, 2**31-1])
def test_jwt_valid_ids(user_id):
    token = jwt_service.create_access_token(user_id)
    assert jwt_service.decode_token(token) == user_id


def test_invalid_token():
    token = jwt_service.create_access_token(10)
    broken = token + "abc"

    with pytest.raises(ValueError):
        jwt_service.decode_token(broken)


@pytest.mark.parametrize("token", ["", None])
def test_empty_token(token):
    with pytest.raises(ValueError):
        jwt_service.decode_token(token)


@pytest.mark.parametrize("other_jwt_service", [create_other_jwt_service()])
def test_token_with_wrong_secret(other_jwt_service):
    token = jwt_service.create_access_token(10)
    with pytest.raises(ValueError):
        other_jwt_service.decode_token(token)


def test_expired_token():
    token = jwt_service.create_access_token(user_id=10, expires_in=timedelta(seconds=-1))
    with pytest.raises(ValueError):
        jwt_service.decode_token(token)


