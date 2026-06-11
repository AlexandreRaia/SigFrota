from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Secretaria


@admin.register(Secretaria)
class SecretariaAdmin(admin.ModelAdmin):
    list_display  = ("sigla", "nome", "ativa")
    list_filter   = ("ativa",)
    search_fields = ("nome", "sigla")


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Perfil SisGestaoFrota'), {
            'fields': ('perfil', 'secretaria', 'telefone', 'foto'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Perfil SisGestaoFrota'), {
            'fields': ('perfil', 'secretaria', 'telefone'),
        }),
    )
    list_display  = ("username", "get_full_name", "email", "perfil", "secretaria", "is_active")
    list_filter   = ("perfil", "secretaria", "is_active", "is_staff")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering      = ("first_name",)
