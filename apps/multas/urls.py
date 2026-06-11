from django.urls import path
from . import views

app_name = "multas"

urlpatterns = [
    # Multas — CRUD
    path("",                  views.lista,   name="lista"),
    path("nova/",             views.criar,   name="criar"),
    path("<int:pk>/",         views.detalhe, name="detalhe"),
    path("<int:pk>/editar/",  views.editar,  name="editar"),
    path("<int:pk>/excluir/", views.excluir, name="excluir"),
    # Tipos de Multa — CRUD
    path("tipos/",                    views.tipos_lista,   name="tipos_lista"),
    path("tipos/<int:pk>/editar/",    views.tipos_editar,  name="tipos_editar"),
    path("tipos/<int:pk>/excluir/",   views.tipos_excluir, name="tipos_excluir"),
]

