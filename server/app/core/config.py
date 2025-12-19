from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from .constants import ENV_PATH, BASE_DIR


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
    )

    DB_URL: str
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str

settings = Settings()  # type: ignore

if settings.DB_URL.startswith("sqlite:///"):
    relative_path = settings.DB_URL.removeprefix("sqlite:///")
    settings.DB_URL = f"sqlite:///{BASE_DIR / relative_path}"
