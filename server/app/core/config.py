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
    
    def get_DB_URL(self) -> str:
        return f"sqlite+aiosqlite:///{BASE_DIR / self.DB_URL}"

settings = Settings()  # type: ignore