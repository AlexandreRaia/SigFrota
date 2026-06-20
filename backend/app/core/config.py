from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

# Caminho absoluto para o .env na raiz do pacote backend/
_ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "SigFrota API"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://sigfrota:sigfrota_dev@localhost:5432/sigfrota"

    # Security
    SECRET_KEY: str = "dev-secret-key-troque-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS — use string no .env: "http://localhost:5173,http://localhost:3000"
    ALLOWED_ORIGINS_STR: str = "http://localhost:5173,http://localhost:3000"

    # Media
    MEDIA_DIR: str = "media"
    MAX_UPLOAD_SIZE_MB: int = 10

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS_STR.split(",") if o.strip()]


settings = Settings()
