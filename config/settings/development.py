"""
Configurações de DESENVOLVIMENTO — banco SQLite3.
Para usar: DJANGO_SETTINGS_MODULE=config.settings.development
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ------------------------------------------------------------------
# Banco de dados — SQLite3 (desenvolvimento / testes)
# Trocar para produção: basta alterar DJANGO_SETTINGS_MODULE para
# config.settings.production e definir DATABASE_URL no .env
# ------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Mostra e-mails no console durante o desenvolvimento
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Django Debug Toolbar (opcional — instale com: pip install django-debug-toolbar)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
# INTERNAL_IPS = ["127.0.0.1"]
