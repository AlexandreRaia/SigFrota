from django.contrib import admin
from .models import Condutor, Acidente, Infracao, Qualificacao, Penalidade, FolgaFerias


class AcidenteInline(admin.TabularInline):
    model = Acidente
    extra = 0


class InfracaoInline(admin.TabularInline):
    model = Infracao
    extra = 0


class QualificacaoInline(admin.TabularInline):
    model = Qualificacao
    extra = 0


class PenalidadeInline(admin.TabularInline):
    model = Penalidade
    extra = 0


class FolgaFeriasInline(admin.TabularInline):
    model = FolgaFerias
    extra = 0


@admin.register(Condutor)
class CondutorAdmin(admin.ModelAdmin):
    list_display   = ("prontuario", "nome", "cpf", "secretaria", "cnh_categoria", "cnh_vencimento", "status")
    list_filter    = ("status", "secretaria", "cnh_categoria")
    search_fields  = ("nome", "cpf", "cnh_numero", "prontuario")
    readonly_fields = ("criado_em", "atualizado_em")
    inlines        = [AcidenteInline, InfracaoInline, QualificacaoInline, PenalidadeInline, FolgaFeriasInline]

    fieldsets = (
        ("Identificação", {"fields": ("prontuario", "foto", "status")}),  # prontuario = matrícula funcional
        ("Dados Pessoais", {"fields": ("nome", "data_nascimento", "cpf", "rg", "orgao_emissor", "cargo")}),
        ("Contato",        {"fields": ("telefone", "email", "endereco")}),
        ("Lotação",        {"fields": ("secretaria", "unidade")}),
        ("CNH",            {"fields": ("cnh_categoria", "cnh_numero", "cnh_emissao", "cnh_vencimento", "cnh_orgao", "cnh_arquivo")}),
        ("Auditoria",      {"fields": ("criado_em", "atualizado_em"), "classes": ("collapse",)}),
    )
