from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def _smv_upload(instance, filename, pasta):
    return f"manutencao/smv-{instance.smv.numero}/{pasta}/{filename}"

def _orcamento_upload(instance, filename):
    return f"manutencao/smv-{instance.smv.numero}/orcamentos/{filename}"

def _nf_upload(instance, filename):
    return f"manutencao/smv-{instance.smv.numero}/notas_fiscais/{filename}"

def _anexo_upload(instance, filename):
    return _smv_upload(instance, filename, "anexos")


def _proximo_numero_smv():
    """Gera número sequencial no formato ANO-NNNN (ex: 2026-0001)."""
    ano = timezone.now().year
    ultimo = SMV.objects.filter(numero__startswith=str(ano)).order_by("numero").last()
    if ultimo:
        seq = int(ultimo.numero.split("-")[1]) + 1
    else:
        seq = 1
    return f"{ano}-{seq:04d}"


# ── SMV — Solicitação de Manutenção Veicular ─────────────────────────────────

class SMV(models.Model):

    class Etapa(models.TextChoices):
        SOLICITACAO  = "SOLICITACAO",  _("Solicitação")
        RECEPCAO     = "RECEPCAO",     _("Recepção")
        DIAGNOSTICO  = "DIAGNOSTICO",  _("Diagnóstico")
        ORCAMENTO    = "ORCAMENTO",    _("Orçamento")
        APROVACAO    = "APROVACAO",    _("Aprovação")
        EXECUCAO     = "EXECUCAO",     _("Execução")
        RETIRADA     = "RETIRADA",     _("Retirada")
        EMISSAO_NF   = "EMISSAO_NF",   _("Emissão de NF")
        FINALIZADO   = "FINALIZADO",   _("Finalizado")

    class Urgencia(models.TextChoices):
        BAIXA = "BAIXA", _("Baixa")
        MEDIA = "MEDIA", _("Média")
        ALTA  = "ALTA",  _("Alta")

    # ── Identificação ──────────────────────────────────────────────────────
    numero      = models.CharField(_("Número"), max_length=10, unique=True, editable=False)
    veiculo     = models.ForeignKey(
        "veiculos.Veiculo",
        on_delete=models.PROTECT,
        related_name="smvs",
        verbose_name=_("Veículo"),
    )
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="smvs_solicitadas",
        verbose_name=_("Solicitante"),
    )

    # ── Etapa e urgência ───────────────────────────────────────────────────
    etapa   = models.CharField(_("Etapa atual"), max_length=15, choices=Etapa.choices, default=Etapa.SOLICITACAO)
    urgencia = models.CharField(_("Urgência"), max_length=10, choices=Urgencia.choices, default=Urgencia.MEDIA)

    # ── Solicitação ────────────────────────────────────────────────────────
    descricao_problema  = models.TextField(_("Descrição do problema / falha"))
    km_entrada          = models.PositiveIntegerField(_("KM na entrada"), null=True, blank=True)
    km_saida            = models.PositiveIntegerField(_("KM na saída"), null=True, blank=True)

    # ── Diagnóstico ────────────────────────────────────────────────────────
    diagnostico         = models.TextField(_("Diagnóstico técnico"), blank=True)
    tipos_servico       = models.CharField(
        _("Tipos de serviço identificados"), max_length=300, blank=True,
        help_text=_("Lista separada por vírgula: MECANICA, ELETRICA, FUNILARIA, etc.")
    )

    # ── Datas de controle ─────────────────────────────────────────────────
    dt_solicitacao  = models.DateTimeField(_("Data de solicitação"), auto_now_add=True)
    dt_recepcao     = models.DateTimeField(_("Data de recepção"), null=True, blank=True)
    dt_diagnostico  = models.DateTimeField(_("Data de diagnóstico"), null=True, blank=True)
    dt_inicio_exec  = models.DateTimeField(_("Início da execução"), null=True, blank=True)
    dt_retirada     = models.DateTimeField(_("Data de retirada"), null=True, blank=True)
    dt_finalizacao  = models.DateTimeField(_("Data de finalização"), null=True, blank=True)

    # ── Observações gerais ─────────────────────────────────────────────────
    observacoes = models.TextField(_("Observações gerais"), blank=True)

    class Meta:
        verbose_name        = _("SMV")
        verbose_name_plural = _("SMVs")
        ordering            = ["-numero"]
        permissions         = [
            ("pode_recepcionar", "Pode recepcionar SMV"),
            ("pode_diagnosticar", "Pode registrar diagnóstico"),
            ("pode_aprovar", "Pode aprovar orçamento (Fiscal do Contrato)"),
        ]

    def __str__(self):
        return f"SMV {self.numero} — {self.veiculo.placa}"

    def save(self, *args, **kwargs):
        if not self.numero:
            self.numero = _proximo_numero_smv()
        super().save(*args, **kwargs)

    @property
    def total_orcamentos(self):
        return self.orcamentos.aggregate(models.Sum("valor_total"))["valor_total__sum"] or 0

    @property
    def mensagens_nao_lidas(self):
        return self.mensagens.count()


# ── Histórico de etapas ───────────────────────────────────────────────────────

class SMVEtapa(models.Model):
    smv         = models.ForeignKey(SMV, on_delete=models.CASCADE, related_name="historico_etapas")
    etapa_de    = models.CharField(_("De"), max_length=15, choices=SMV.Etapa.choices, blank=True)
    etapa_para  = models.CharField(_("Para"), max_length=15, choices=SMV.Etapa.choices)
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Responsável"))
    observacao  = models.TextField(_("Observação"), blank=True)
    data        = models.DateTimeField(_("Data/hora"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Histórico de etapa")
        verbose_name_plural = _("Histórico de etapas")
        ordering            = ["data"]

    def __str__(self):
        return f"SMV {self.smv.numero}: {self.etapa_de} → {self.etapa_para}"


# ── Itens do diagnóstico (peças e serviços identificados) ─────────────────────

class SMVDiagnosticoItem(models.Model):

    class Tipo(models.TextChoices):
        PECA     = "PECA",     _("Peça")
        SERVICO  = "SERVICO",  _("Serviço / Mão de obra")

    smv         = models.ForeignKey(SMV, on_delete=models.CASCADE, related_name="itens_diagnostico")
    tipo        = models.CharField(_("Tipo"), max_length=10, choices=Tipo.choices, default=Tipo.PECA)
    descricao   = models.CharField(_("Descrição"), max_length=300)
    quantidade  = models.DecimalField(_("Quantidade"), max_digits=8, decimal_places=2, default=1)
    unidade     = models.CharField(_("Unidade"), max_length=20, default="pç",
                                   help_text=_("pç, m, l, h, kg, un, serv…"))
    observacao  = models.TextField(_("Observação"), blank=True)
    criado_por  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    verbose_name=_("Registrado por"))
    criado_em   = models.DateTimeField(_("Registrado em"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Item do diagnóstico")
        verbose_name_plural = _("Itens do diagnóstico")
        ordering            = ["tipo", "descricao"]

    def __str__(self):
        return f"{self.get_tipo_display()} — {self.descricao} ({self.quantidade} {self.unidade})"


# ── Checklist de entrada/saída ───────────────────────────────────────────────

class SMVChecklist(models.Model):

    class Tipo(models.TextChoices):
        ENTRADA = "ENTRADA", _("Entrada")
        SAIDA   = "SAIDA",   _("Saída")

    class Condicao(models.TextChoices):
        OK      = "OK",      _("OK")
        REGULAR = "REGULAR", _("Regular")
        RUIM    = "RUIM",    _("Ruim")
        NA      = "NA",      _("N/A")

    smv        = models.ForeignKey(SMV, on_delete=models.CASCADE, related_name="checklists")
    tipo       = models.CharField(_("Tipo"), max_length=7, choices=Tipo.choices)
    item       = models.CharField(_("Item"), max_length=100)
    condicao   = models.CharField(_("Condição"), max_length=8, choices=Condicao.choices, default=Condicao.OK)
    observacao = models.CharField(_("Observação"), max_length=255, blank=True)
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Responsável"))
    data        = models.DateTimeField(_("Data/hora"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Item de checklist")
        verbose_name_plural = _("Itens de checklist")
        ordering            = ["tipo", "item"]

    def __str__(self):
        return f"{self.get_tipo_display()} | {self.item} ({self.get_condicao_display()})"


# ── Recepção do veículo na oficina ────────────────────────────────────────

class SMVRecepcao(models.Model):

    class NivelCombustivel(models.TextChoices):
        RESERVA = "RESERVA", _("Reserva")
        UM_QUARTO = "1/4",   _("1/4")
        MEIO      = "1/2",   _("1/2")
        TRES_QUARTOS = "3/4",_("3/4")
        CHEIO     = "CHEIO", _("Cheio")

    smv              = models.OneToOneField(SMV, on_delete=models.CASCADE, related_name="recepcao")
    km_entrada       = models.PositiveIntegerField(_("KM de entrada"))
    nivel_combustivel = models.CharField(_("Nível do combustível"), max_length=10, choices=NivelCombustivel.choices)
    observacoes      = models.TextField(_("Observações gerais"), blank=True)
    responsavel      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Recepcionado por"))
    data_hora        = models.DateTimeField(_("Data/hora de entrada"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Recepção")
        verbose_name_plural = _("Recepções")

    def __str__(self):
        return f"Recepção SMV {self.smv.numero} — {self.data_hora:%d/%m/%Y %H:%M}"


# ── Orçamentos (múltiplos por SMV) ───────────────────────────────────────────

class SMVOrcamento(models.Model):

    class Status(models.TextChoices):
        EM_NEGOCIACAO = "EM_NEGOCIACAO", _("Em negociação")
        AGUARD_APROVA = "AGUARD_APROVA", _("Aguardando aprovação")
        APROVADO      = "APROVADO",      _("Aprovado")
        RECUSADO      = "RECUSADO",      _("Recusado")

    smv             = models.ForeignKey(SMV, on_delete=models.CASCADE, related_name="orcamentos")
    versao          = models.PositiveSmallIntegerField(_("Versão"))
    fornecedor      = models.CharField(_("Fornecedor / Oficina"), max_length=120)
    cnpj_fornecedor = models.CharField(_("CNPJ Fornecedor"), max_length=18, blank=True)
    valor_pecas     = models.DecimalField(_("Valor peças (R$)"), max_digits=12, decimal_places=2, default=0)
    valor_mo        = models.DecimalField(_("Valor mão de obra (R$)"), max_digits=12, decimal_places=2, default=0)
    valor_total     = models.DecimalField(_("Valor total (R$)"), max_digits=12, decimal_places=2, default=0)
    arquivo_pdf     = models.FileField(_("PDF do orçamento"), upload_to=_orcamento_upload, null=True, blank=True)
    status          = models.CharField(_("Status"), max_length=15, choices=Status.choices, default=Status.EM_NEGOCIACAO)
    observacoes     = models.TextField(_("Observações"), blank=True)
    criado_por      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Criado por"))
    criado_em       = models.DateTimeField(_("Criado em"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Orçamento")
        verbose_name_plural = _("Orçamentos")
        ordering            = ["smv", "versao"]
        unique_together     = [["smv", "versao"]]

    def __str__(self):
        return f"SMV {self.smv.numero} — Orçamento v{self.versao} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.versao:
            ultimo = SMVOrcamento.objects.filter(smv=self.smv).order_by("versao").last()
            self.versao = (ultimo.versao + 1) if ultimo else 1
        self.valor_total = self.valor_pecas + self.valor_mo
        super().save(*args, **kwargs)


# ── Aprovação do orçamento ───────────────────────────────────────────────────

class SMVAprovacao(models.Model):

    class StatusDocFisico(models.TextChoices):
        NAO_ENVIADO     = "NAO_ENVIADO",     _("Não enviado")
        ENVIADO_RESP    = "ENVIADO_RESP",     _("Enviado ao Resp. Técnico")
        ENVIADO_FISCAL  = "ENVIADO_FISCAL",   _("Enviado ao Fiscal da Pasta")
        ENVIADO_SECRET  = "ENVIADO_SECRET",   _("Enviado ao Secretário")
        RETORNADO       = "RETORNADO",        _("Retornado à Gestão")

    orcamento               = models.OneToOneField(SMVOrcamento, on_delete=models.CASCADE, related_name="aprovacao")
    status_doc_fisico       = models.CharField(_("Status doc. físico"), max_length=20,
                                               choices=StatusDocFisico.choices, default=StatusDocFisico.NAO_ENVIADO)
    # Responsável técnico
    resp_tecnico            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                                related_name="aprovacoes_resp", null=True, blank=True,
                                                verbose_name=_("Responsável técnico"))
    dt_envio_resp           = models.DateField(_("Envio ao Resp. Técnico"), null=True, blank=True)
    dt_assin_resp           = models.DateField(_("Assinatura Resp. Técnico"), null=True, blank=True)
    # Fiscal da pasta
    fiscal_pasta            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                                related_name="aprovacoes_fiscal_pasta", null=True, blank=True,
                                                verbose_name=_("Fiscal da pasta"))
    dt_envio_fiscal_pasta   = models.DateField(_("Envio ao Fiscal da Pasta"), null=True, blank=True)
    dt_assin_fiscal_pasta   = models.DateField(_("Assinatura Fiscal da Pasta"), null=True, blank=True)
    # Secretário
    secretario              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                                related_name="aprovacoes_secretario", null=True, blank=True,
                                                verbose_name=_("Secretário"))
    dt_envio_secretario     = models.DateField(_("Envio ao Secretário"), null=True, blank=True)
    dt_assin_secretario     = models.DateField(_("Assinatura Secretário"), null=True, blank=True)
    # Fiscal do contrato (aprovação final)
    fiscal_contrato         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                                related_name="aprovacoes_fiscal_contrato", null=True, blank=True,
                                                verbose_name=_("Fiscal do contrato"))
    dt_aprovacao_final      = models.DateTimeField(_("Data de aprovação final"), null=True, blank=True)
    observacoes             = models.TextField(_("Observações"), blank=True)

    class Meta:
        verbose_name        = _("Aprovação de orçamento")
        verbose_name_plural = _("Aprovações de orçamento")

    def __str__(self):
        return f"Aprovação — {self.orcamento}"

    @property
    def todas_assinaturas(self):
        return all([self.dt_assin_resp, self.dt_assin_fiscal_pasta, self.dt_assin_secretario])


# ── Notas Fiscais (múltiplas por SMV) ────────────────────────────────────────

class SMVNotaFiscal(models.Model):

    class Status(models.TextChoices):
        PENDENTE     = "PENDENTE",     _("Pendente de conferência")
        EM_CORRECAO  = "EM_CORRECAO",  _("Solicitada correção")
        CONFERIDA    = "CONFERIDA",    _("Conferida e aprovada")

    smv             = models.ForeignKey(SMV, on_delete=models.CASCADE, related_name="notas_fiscais")
    numero_nf       = models.CharField(_("Número da NF"), max_length=20)
    data_emissao    = models.DateField(_("Data de emissão"))
    cnpj_prestador  = models.CharField(_("CNPJ do prestador"), max_length=18)
    razao_social    = models.CharField(_("Razão social"), max_length=120, blank=True)
    valor_total     = models.DecimalField(_("Valor total (R$)"), max_digits=12, decimal_places=2)
    arquivo_pdf     = models.FileField(_("PDF da NF"), upload_to=_nf_upload, null=True, blank=True)
    status          = models.CharField(_("Status"), max_length=12, choices=Status.choices, default=Status.PENDENTE)
    criado_em       = models.DateTimeField(_("Criado em"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Nota Fiscal")
        verbose_name_plural = _("Notas Fiscais")
        ordering            = ["smv", "data_emissao"]

    def __str__(self):
        return f"NF {self.numero_nf} — SMV {self.smv.numero}"


# ── Itens da Nota Fiscal ──────────────────────────────────────────────────────

class SMVItemNF(models.Model):

    class Tipo(models.TextChoices):
        PECA     = "PECA",    _("Peça")
        SERVICO  = "SERVICO", _("Serviço")

    class TipoServico(models.TextChoices):
        MECANICA   = "MECANICA",   _("Mecânica geral")
        ELETRICA   = "ELETRICA",   _("Elétrica")
        FUNILARIA  = "FUNILARIA",  _("Funilaria / Pintura")
        HIDRAULICA = "HIDRAULICA", _("Hidráulica")
        PNEUS      = "PNEUS",      _("Pneus / Borracharia")
        AR_COND    = "AR_COND",    _("Ar-condicionado")
        VIDROS     = "VIDROS",     _("Vidros")
        REVISAO    = "REVISAO",    _("Revisão periódica")
        OUTRO      = "OUTRO",      _("Outro")

    nota_fiscal     = models.ForeignKey(SMVNotaFiscal, on_delete=models.CASCADE, related_name="itens")
    tipo            = models.CharField(_("Tipo"), max_length=8, choices=Tipo.choices)
    tipo_servico    = models.CharField(_("Tipo de serviço"), max_length=12, choices=TipoServico.choices, blank=True)
    descricao       = models.CharField(_("Descrição"), max_length=255)
    unidade         = models.CharField(_("Unidade"), max_length=10, default="UN")
    quantidade      = models.DecimalField(_("Quantidade"), max_digits=10, decimal_places=3)
    valor_unitario  = models.DecimalField(_("Valor unitário (R$)"), max_digits=12, decimal_places=2)
    valor_total     = models.DecimalField(_("Valor total (R$)"), max_digits=12, decimal_places=2, editable=False)
    horas_mo        = models.DecimalField(_("Horas de MO"), max_digits=6, decimal_places=2, null=True, blank=True,
                                          help_text=_("Preencher apenas para serviços"))

    class Meta:
        verbose_name        = _("Item de NF")
        verbose_name_plural = _("Itens de NF")
        ordering            = ["nota_fiscal", "tipo", "descricao"]

    def __str__(self):
        return f"{self.get_tipo_display()} | {self.descricao} ({self.quantidade} {self.unidade})"

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario
        super().save(*args, **kwargs)


# ── Anexos por etapa ─────────────────────────────────────────────────────────

class SMVAnexo(models.Model):

    class TipoAnexo(models.TextChoices):
        FOTO_ENTRADA = "FOTO_ENTRADA", _("Foto de entrada")
        FOTO_SAIDA   = "FOTO_SAIDA",   _("Foto de saída")
        FOTO_PECA    = "FOTO_PECA",    _("Foto de peça substituída")
        LAUDO        = "LAUDO",        _("Laudo técnico")
        TESTE        = "TESTE",        _("Resultado de teste")
        OUTRO        = "OUTRO",        _("Outro")

    smv         = models.ForeignKey(SMV, on_delete=models.CASCADE, related_name="anexos")
    etapa       = models.CharField(_("Etapa"), max_length=15, choices=SMV.Etapa.choices)
    tipo        = models.CharField(_("Tipo"), max_length=12, choices=TipoAnexo.choices, default=TipoAnexo.OUTRO)
    descricao   = models.CharField(_("Descrição"), max_length=200, blank=True)
    arquivo     = models.FileField(_("Arquivo"), upload_to=_anexo_upload)
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_("Enviado por"))
    enviado_em  = models.DateTimeField(_("Enviado em"), auto_now_add=True)

    class Meta:
        verbose_name        = _("Anexo")
        verbose_name_plural = _("Anexos")
        ordering            = ["etapa", "enviado_em"]

    def __str__(self):
        return f"SMV {self.smv.numero} | {self.get_tipo_display()} — {self.descricao or self.arquivo.name}"
