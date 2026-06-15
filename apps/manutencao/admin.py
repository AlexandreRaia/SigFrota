from django.contrib import admin
from .models import (
    SMV, SMVEtapa, SMVChecklist, SMVOrcamento,
    SMVAprovacao, SMVNotaFiscal, SMVItemNF, SMVAnexo,
)


class SMVEtapaInline(admin.TabularInline):
    model = SMVEtapa
    extra = 0
    readonly_fields = ["data"]


class SMVChecklistInline(admin.TabularInline):
    model = SMVChecklist
    extra = 0
    readonly_fields = ["data"]


class SMVAnexoInline(admin.TabularInline):
    model = SMVAnexo
    extra = 0
    readonly_fields = ["enviado_em"]


class SMVOrcamentoInline(admin.StackedInline):
    model = SMVOrcamento
    extra = 0
    readonly_fields = ["versao", "valor_total", "criado_em"]


class SMVNotaFiscalInline(admin.StackedInline):
    model = SMVNotaFiscal
    extra = 0
    readonly_fields = ["criado_em"]


class SMVItemNFInline(admin.TabularInline):
    model = SMVItemNF
    extra = 0
    readonly_fields = ["valor_total"]


@admin.register(SMV)
class SMVAdmin(admin.ModelAdmin):
    list_display  = ["numero", "veiculo", "etapa", "urgencia", "solicitante", "dt_solicitacao"]
    list_filter   = ["etapa", "urgencia", "veiculo__secretaria"]
    search_fields = ["numero", "veiculo__placa", "solicitante__username"]
    readonly_fields = ["numero", "dt_solicitacao"]
    inlines = [SMVEtapaInline, SMVChecklistInline, SMVAnexoInline, SMVOrcamentoInline, SMVNotaFiscalInline]


@admin.register(SMVNotaFiscal)
class SMVNotaFiscalAdmin(admin.ModelAdmin):
    list_display = ["numero_nf", "smv", "data_emissao", "valor_total", "status"]
    inlines      = [SMVItemNFInline]


@admin.register(SMVOrcamento)
class SMVOrcamentoAdmin(admin.ModelAdmin):
    list_display  = ["smv", "versao", "fornecedor", "valor_total", "status", "criado_em"]
    readonly_fields = ["versao", "valor_total", "criado_em"]

