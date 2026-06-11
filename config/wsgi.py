"""
Configuração WSGI do SisGestaoFrota.

Expõe o callable WSGI como variável de módulo chamada ``application``.

Mais informações:
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
