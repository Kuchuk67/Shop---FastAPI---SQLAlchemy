from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import sys

# Конфигурация приложения
# Константы должны быть прописаны в Файле .env

BASE_DIR = Path(__file__)


class Setting(BaseSettings):
   # DB_HOST: str
   # DB_PORT: int
   # DB_NAME: str
   # DB_USER: str
   # DB_PASSWORD: str

    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: int
    POSTGRES_PORT: int

    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_DB: str

    DEBAG: bool

    # url соединения с БД
    # db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # db_url: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FRESH_TOKEN_EXPIRE_MINUTES: int

    # Алгоритм шифрования токена
    ALGORITHM: str

    # Кортеж ролей пользователей
    ROLES: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding="utf8",
        extra="ignore",
        case_sensitive=True,
    )

    @property
    def role(self):
        return tuple(self.ROLES.split(","))

    @property
    def api_prefix(self):
        # версия api
        return "/api/v1"

    @property
    def db_url(self):
        if "main:app" in sys.argv:
            return (
                f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        else:
            return (
                f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.TEST_POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.TEST_POSTGRES_DB}"
            )


setting = Setting()  # type: ignore
