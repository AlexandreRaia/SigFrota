"""
Configuração ASGI do SisGestaoFrota.

Expõe o callable ASGI como variável de módulo chamada ``application``.

Mais informações:
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_asgi_application()
