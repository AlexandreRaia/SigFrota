"""
URLs raiz do SisGestaoFrota.
Cada módulo/app tem suas próprias urls.py incluídas aqui.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Autenticação
    path("", include("apps.usuarios.urls")),

    # Grappelli — redireciona /grappelli/ para o admin e registra rotas auxiliares
    path("grappelli/", RedirectView.as_view(url='/admin/')),
    path("grappelli/", include("grappelli.urls")),

    # Painel administrativo Django
    path("admin/", admin.site.urls),

    # Módulos do sistema
    path("", include("apps.core.urls")),                         # M01 Dashboard / home
    path("veiculos/", include("apps.veiculos.urls")),            # M02
    path("api/veiculos/", include("apps.veiculos.api_urls")),    # API veículos
    path("condutores/", include("apps.condutores.urls")),        # M03
    path("manutencao/", include(("apps.manutencao.urls", "manutencao"))),  # M04 SMV
    path("preventiva/", include("apps.preventiva.urls")),        # M05
    path("agendamento/", include("apps.agendamento.urls")),      # M06
    path("abastecimento/", include("apps.abastecimento.urls")),  # M07
    path("despesas/", include("apps.despesas.urls")),            # M08
    path("multas/", include("apps.multas.urls")),                # M09
    path("relatorios/", include("apps.relatorios.urls")),        # M10
    path("chat/", include("apps.chat.urls")),                    # M12

    # API REST
    path("api/veiculos/", include("apps.veiculos.api_urls")),
    path("api/condutores/", include("apps.condutores.api_urls")),
    path("api/manutencao/", include("apps.manutencao.api_urls")),
    path("api/abastecimento/", include("apps.abastecimento.api_urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

