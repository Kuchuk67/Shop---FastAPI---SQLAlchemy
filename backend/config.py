from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Конфигурация приложения
# Константы должны быть прописаны в Файле .env

BASE_DIR = Path(__file__)

class Setting(BaseSettings):
    # версия api
    api_prefix: str = "/api/v1"

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DEBAG: bool

    # url соединения с БД
    #db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    #db_url: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    SECRET_KEY: str
   
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
    def db_url(self):  
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}/{self.DB_NAME}"
        ) 
    
setting = Setting()
