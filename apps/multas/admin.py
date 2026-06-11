from django.contrib import admin
from .models import Multa, TipoMulta


@admin.register(TipoMulta)
class TipoMultaAdmin(admin.ModelAdmin):
    list_display  = ("codigo", "descricao", "natureza", "ativo")
    list_filter   = ("natureza", "ativo")
    search_fields = ("codigo", "descricao")


@admin.register(Multa)
class MultaAdmin(admin.ModelAdmin):
    list_display  = ("placa", "condutor", "data_infracao", "tipo_infracao", "pontos", "valor", "status", "data_vencimento")
    list_filter   = ("status", "tipo_infracao")
    search_fields = ("placa", "condutor__nome", "condutor__prontuario")
    date_hierarchy = "data_infracao"
    readonly_fields = ("criado_em", "atualizado_em")
    fieldsets = (
        ("Identificação",   {"fields": ("placa", "condutor")}),
        ("Infração",        {"fields": ("data_infracao", "tipo_infracao", "pontos", "valor")}),
        ("Situação/Prazos", {"fields": ("status", "data_vencimento", "prazo_indicacao", "prazo_defesa")}),
        ("Documentação",    {"fields": ("arquivo", "observacao")}),
        ("Auditoria",       {"fields": ("criado_em", "atualizado_em"), "classes": ("collapse",)}),
    )

