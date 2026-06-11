from django.urls import path
from . import views

app_name = "condutores"

urlpatterns = [
    path("",                      views.lista,          name="lista"),
    path("novo/",                 views.criar,          name="criar"),
    path("<int:pk>/",             views.detalhe,        name="detalhe"),
    path("<int:pk>/editar/",      views.editar,         name="editar"),
    path("<int:pk>/inativar/",    views.inativar,       name="inativar"),
    path("<int:pk>/suspender/",   views.suspender,      name="suspender"),
    # Histórico — adicionar
    path("<int:pk>/acidente/",    views.add_acidente,   name="add_acidente"),
    path("<int:pk>/infracao/",    views.add_infracao,   name="add_infracao"),
    path("<int:pk>/qualificacao/",views.add_qualificacao, name="add_qualificacao"),
    path("<int:pk>/penalidade/",  views.add_penalidade, name="add_penalidade"),
    path("<int:pk>/folga/",       views.add_folga,      name="add_folga"),
    # Qualificações — editar / excluir
    path("<int:pk>/qualificacao/<int:item_pk>/editar/",  views.edit_qualificacao, name="edit_qualificacao"),
    path("<int:pk>/qualificacao/<int:item_pk>/excluir/", views.del_qualificacao,  name="del_qualificacao"),
    # Penalidades — editar / excluir
    path("<int:pk>/penalidade/<int:item_pk>/editar/",    views.edit_penalidade,   name="edit_penalidade"),
    path("<int:pk>/penalidade/<int:item_pk>/excluir/",   views.del_penalidade,    name="del_penalidade"),
    # Férias/Folgas — editar / excluir
    path("<int:pk>/folga/<int:item_pk>/editar/",         views.edit_folga,        name="edit_folga"),
    path("<int:pk>/folga/<int:item_pk>/excluir/",        views.del_folga,         name="del_folga"),
]

