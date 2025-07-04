import os

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH_ENV = os.path.join(BASE_DIR, ".env")


class Settings(BaseSettings):
    # TODO: Change to production values
    DB_NAME: str = "balances"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "admin"
    DB_PORT: int = 5432
    DB_HOST: str = "localhost"

    model_config = SettingsConfigDict(env_file=PATH_ENV, env_file_encoding="utf-8")

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()