from django.urls import path
from . import views

app_name = "veiculos"

urlpatterns = [
    path("",                   views.lista,    name="lista"),
    path("novo/",              views.criar,    name="criar"),
    path("<int:pk>/",          views.detalhe,  name="detalhe"),
    path("<int:pk>/editar/",   views.editar,   name="editar"),
    path("<int:pk>/inativar/", views.inativar, name="inativar"),
]

