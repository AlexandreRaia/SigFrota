from django.contrib import admin
from .models import SMVMensagem, SMVMensagemLeitura


@admin.register(SMVMensagem)
class SMVMensagemAdmin(admin.ModelAdmin):
    list_display  = ["smv", "autor", "etapa", "enviada_em"]
    list_filter   = ["etapa"]
    search_fields = ["smv__numero", "autor__username", "texto"]
    readonly_fields = ["enviada_em"]


@admin.register(SMVMensagemLeitura)
class SMVMensagemLeituraAdmin(admin.ModelAdmin):
    list_display = ["mensagem", "usuario", "lida_em"]
    readonly_fields = ["lida_em"]

