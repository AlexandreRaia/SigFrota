import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


def _get_asyncpg_url() -> str:
    # Use SQLite for development if no PostgreSQL config
    use_sqlite = os.environ.get("USE_SQLITE", "true").lower() == "true"
    if use_sqlite:
        db_path = os.environ.get("SQLITE_DB_PATH", "sigfrota.db")
        return f"sqlite+aiosqlite:///{db_path}"
    
    pg_host = os.environ.get("PGHOST")
    pg_port = os.environ.get("PGPORT", "5432")
    pg_user = os.environ.get("PGUSER")
    pg_password = os.environ.get("PGPASSWORD")
    pg_database = os.environ.get("PGDATABASE")
    if pg_host and pg_user and pg_password and pg_database:
        return f"postgresql+asyncpg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
    return "postgresql+asyncpg://sigfrota:sigfrota_dev@localhost:5432/sigfrota"


def _get_allowed_origins() -> str:
    replit_domain = os.environ.get("REPLIT_DEV_DOMAIN", "")
    origins = ["http://localhost:5000", "http://localhost:5173", "http://localhost:3000"]
    if replit_domain:
        origins.append(f"https://{replit_domain}")
    return ",".join(origins)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "SigFrota API"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True

    # Use ASYNCPG_DATABASE_URL to avoid pydantic-settings auto-reading DATABASE_URL
    ASYNCPG_DATABASE_URL: str = _get_asyncpg_url()

    SECRET_KEY: str = "dev-secret-key-troque-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    ALLOWED_ORIGINS_STR: str = _get_allowed_origins()

    MEDIA_DIR: str = "media"
    MAX_UPLOAD_SIZE_MB: int = 10

    @property
    def DATABASE_URL(self) -> str:
        return self.ASYNCPG_DATABASE_URL

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS_STR.split(",") if o.strip()]


settings = Settings()
