from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Lobachevsky Portal"

    database_url: PostgresDsn = "postgresql+asyncpg://portal:portal@db:5432/portal"

    ai_service_url: str = "http://ai-service:8001"
    websocket_notifier_url: str = "ws://notifier:8002/ws"


settings = Settings()
