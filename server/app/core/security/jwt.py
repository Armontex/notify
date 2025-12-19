from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError


class JWTService:

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        access_token_expire_minutes: int,
    ):
        self.__secret_key = secret_key
        self.__algorithm = algorithm
        self.__expire_minutes = timedelta(minutes=access_token_expire_minutes)

    def create_access_token(self, user_id: int, expires_in: timedelta | None = None) -> str:
        payload = {
            "sub": str(user_id),
            "iat": datetime.now(UTC),
            "exp":
            datetime.now(UTC) + (expires_in if expires_in else self.__expire_minutes),
        }
        return jwt.encode(payload,
                          self.__secret_key,
                          algorithm=self.__algorithm)

    def decode_token(self, token: str) -> int:
        if not token or not isinstance(token, str):
            raise ValueError("Token is empty")
        
        try:
            payload = jwt.decode(
                token,
                self.__secret_key,
                algorithms=[self.__algorithm],
            )
            return int(payload["sub"])
        except (JWTError, KeyError, ValueError):
            raise ValueError("Invalid token")


from ..config import settings

jwt_service = JWTService(
    secret_key=settings.SECRET_KEY.get_secret_value(),
    algorithm=settings.JWT_ALGORITHM,
    access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

