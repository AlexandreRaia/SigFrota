"""
Configurações de PRODUÇÃO — banco PostgreSQL.
Para usar: DJANGO_SETTINGS_MODULE=config.settings.production

Basta definir no .env:
    DATABASE_URL=postgres://user:password@host:5432/sigfrota
"""

import dj_database_url
from .base import *  # noqa: F401, F403

DEBUG = False

# ------------------------------------------------------------------
# Banco de dados — PostgreSQL via DATABASE_URL
# Trocar para SQLite3: basta alterar DJANGO_SETTINGS_MODULE para
# config.settings.development — nenhuma outra alteração necessária.
# ------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ------------------------------------------------------------------
# Segurança em produção
# ------------------------------------------------------------------
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
