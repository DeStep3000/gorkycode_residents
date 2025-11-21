# db/config.py

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: AnyUrl

    # аналог Config в pydantic v1
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",      # <--- ВАЖНО: игнорируем лишние переменные

    )


settings = Settings()
