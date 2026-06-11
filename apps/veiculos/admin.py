from django.contrib import admin
from .models import Veiculo, TipoVeiculo, Marca, Modelo


@admin.register(TipoVeiculo)
class TipoVeiculoAdmin(admin.ModelAdmin):
    list_display  = ("nome", "ativo")
    list_filter   = ("ativo",)
    search_fields = ("nome",)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display  = ("nome", "ativo")
    search_fields = ("nome",)


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display  = ("nome", "marca", "tipo_veiculo", "ativo")
    list_filter   = ("marca", "tipo_veiculo", "ativo")
    search_fields = ("nome", "marca__nome")


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display  = ("placa", "marca", "modelo", "ano_fabricacao", "tipo_frota", "secretaria", "status")
    list_filter   = ("tipo_frota", "tipo_veiculo", "status", "combustivel", "secretaria")
    search_fields = ("placa", "marca", "modelo", "chassi", "renavam", "num_patrimonio", "prefixo")
    readonly_fields = ("criado_em", "atualizado_em")
    fieldsets = (
        ("Identificação",             {"fields": ("placa", "marca", "modelo", "chassi", "renavam", "prefixo", "num_patrimonio")}),
        ("Especificações Técnicas",   {"fields": ("tipo_veiculo", "ano_fabricacao", "motor_potencia", "combustivel", "cap_tanque", "consumo_ref", "cap_passageiros", "cor", "transmissao", "pneu_dim")}),
        ("Histórico e Estado",        {"fields": ("km_entrada", "ultimo_km", "estado_conservacao", "status")}),
        ("Informações Financeiras",   {"fields": ("valor_fipe", "tipo_frota", "locadora", "valor_aluguel", "dt_ini_contrato", "dt_fim_contrato")}),
        ("Informações Administrativas", {"fields": ("secretaria", "centro_custo")}),
        ("Documentação",              {"fields": ("crlv", "foto_frente", "foto_lateral_e", "foto_lateral_d", "foto_traseira", "foto_hodometro", "outros_docs")}),
        ("Equipamentos",              {"fields": ("eq_ar_condicionado", "eq_direcao_hidraulica", "eq_vidros_eletricos", "eq_som_multimidia", "eq_radio_comunicador", "eq_rodas_liga_leve", "eq_camera_re", "eq_sensor_estac", "eq_outros")}),
        ("Auditoria",                 {"fields": ("criado_em", "atualizado_em"), "classes": ("collapse",)}),
    )

