from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    app_name: str = "Lobachevsky Portal"
    secret_key: str = "CHANGE_ME"  # вынести в env
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = "HS256"

    database_url: PostgresDsn = "postgresql+asyncpg://portal:portal@db:5432/portal"

    ai_api_base_url: str = "https://example.com/ai"
    ai_api_key: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
