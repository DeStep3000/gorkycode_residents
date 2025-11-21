from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    app_name: str = "Lobachevsky Portal"

    database_url: PostgresDsn = "postgresql+asyncpg://portal:portal@db:5432/portal"

    ai_service_url: str = "http://ai-service:8001"
    websocket_notifier_url: str = "ws://notifier:8002/ws"

    class Config:
        env_file = ".env"


settings = Settings()
