from django.urls import path
from . import views

app_name = "manutencao"

urlpatterns = [
    path("",                                          views.lista,             name="lista"),
    path("nova/",                                     views.criar,             name="criar"),
    path("<int:pk>/",                                 views.detalhe,           name="detalhe"),
    path("<int:pk>/recepcao/",                        views.recepcao,          name="recepcao"),
    path("<int:pk>/diagnostico/",                     views.diagnostico,       name="diagnostico"),
    path("<int:pk>/orcamento/",                       views.orcamento,         name="orcamento"),
    path("<int:pk>/orcamento/<int:orc_pk>/recusar/",  views.recusar_orcamento, name="recusar_orcamento"),
    path("<int:pk>/orcamento/<int:orc_pk>/aprovar/",   views.aprovar_orcamento,  name="aprovar_orcamento"),
    path("<int:pk>/avancar/",                         views.avancar_etapa,     name="avancar_etapa"),
    path("<int:pk>/mensagem/",                        views.enviar_mensagem,   name="enviar_mensagem"),
    path("<int:pk>/anexo/",                           views.upload_anexo,      name="upload_anexo"),
]
