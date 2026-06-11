from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


def _veiculo_upload(instance, filename, pasta):
    return f"veiculos/{instance.placa}/{pasta}/{filename}"

def _crlv_upload(instance, filename):        return _veiculo_upload(instance, filename, "crlv")
def _foto_frente_upload(instance, filename): return _veiculo_upload(instance, filename, "fotos")
def _foto_le_upload(instance, filename):     return _veiculo_upload(instance, filename, "fotos")
def _foto_ld_upload(instance, filename):     return _veiculo_upload(instance, filename, "fotos")
def _foto_tras_upload(instance, filename):   return _veiculo_upload(instance, filename, "fotos")
def _foto_hod_upload(instance, filename):    return _veiculo_upload(instance, filename, "fotos")
def _docs_upload(instance, filename):        return _veiculo_upload(instance, filename, "docs")


# ── Tabelas de lookup ────────────────────────────────────────────────────────

class TipoVeiculo(models.Model):
    nome = models.CharField(_("Nome"), max_length=50, unique=True)
    ativo = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name        = _("Tipo de Veículo")
        verbose_name_plural = _("Tipos de Veículo")
        ordering            = ["nome"]

    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField(_("Nome"), max_length=60, unique=True)
    ativo = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name        = _("Marca")
        verbose_name_plural = _("Marcas")
        ordering            = ["nome"]

    def __str__(self):
        return self.nome


class Modelo(models.Model):
    marca        = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelos", verbose_name=_("Marca"))
    nome         = models.CharField(_("Nome"), max_length=100)
    tipo_veiculo = models.ForeignKey(TipoVeiculo, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="modelos", verbose_name=_("Tipo padrão"))
    ativo        = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name        = _("Modelo")
        verbose_name_plural = _("Modelos")
        ordering            = ["marca__nome", "nome"]
        unique_together     = [["marca", "nome"]]

    def __str__(self):
        return f"{self.marca.nome} {self.nome}"


# ── Veículo ──────────────────────────────────────────────────────────────────

class Veiculo(models.Model):

    # ── Choices que permanecem no código ─────────────────────────────────────

    class Combustivel(models.TextChoices):
        GASOLINA = "GASOLINA", _("Gasolina")
        DIESEL   = "DIESEL",   _("Diesel")
        FLEX     = "FLEX",     _("Flex")
        ELETRICO = "ELETRICO", _("Elétrico")
        GNV      = "GNV",      _("GNV")

    class Transmissao(models.TextChoices):
        MANUAL    = "MANUAL",    _("Manual")
        AUTOMATICA = "AUTOMATICA", _("Automática")
        CVT        = "CVT",        _("CVT")
        SEMI_AUTO  = "SEMI_AUTO",  _("Semi-automática")

    class EstadoConservacao(models.TextChoices):
        OTIMO   = "OTIMO",   _("Ótimo")
        BOM     = "BOM",     _("Bom")
        REGULAR = "REGULAR", _("Regular")
        RUIM    = "RUIM",    _("Ruim")
        PESSIMO = "PESSIMO", _("Péssimo")

    class Status(models.TextChoices):
        DISPONIVEL    = "DISPONIVEL",    _("Disponível")
        EM_MANUTENCAO = "EM_MANUTENCAO", _("Em Manutenção")
        INATIVO       = "INATIVO",       _("Inativo")

    class TipoFrota(models.TextChoices):
        PROPRIO  = "PROPRIO",  _("Próprio")
        LOCADO   = "LOCADO",   _("Locado")
        ESTADUAL = "ESTADUAL", _("Estadual")
        DOACAO   = "DOACAO",   _("Doação")

    # ── Grupo: Identificação ─────────────────────────────────────────────────

    placa = models.CharField(
        _("Placa"), max_length=10, unique=True,
        validators=[RegexValidator(
            r'^[A-Z]{3}[\-]?\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$',
            "Placa inválida. Use AAA-0000 ou Mercosul AAA0A00."
        )],
    )
    marca  = models.ForeignKey(Marca,      on_delete=models.PROTECT, verbose_name=_("Marca"),   related_name="veiculos", null=True, blank=True)
    modelo = models.ForeignKey(Modelo,     on_delete=models.PROTECT, verbose_name=_("Modelo"),  related_name="veiculos", null=True, blank=True)
    chassi         = models.CharField(_("Chassi"), max_length=17, unique=True)
    renavam        = models.CharField(_("RENAVAM"), max_length=11, unique=True)
    prefixo        = models.CharField(_("Prefixo"), max_length=20, blank=True)
    num_patrimonio = models.CharField(_("Nº de Patrimônio"), max_length=30, blank=True)

    # ── Grupo: Especificações Técnicas ───────────────────────────────────────

    tipo_veiculo    = models.ForeignKey(TipoVeiculo, on_delete=models.PROTECT, verbose_name=_("Tipo de Veículo"), related_name="veiculos", null=True, blank=True)
    ano_fabricacao  = models.PositiveSmallIntegerField(_("Ano de Fabricação"))
    motor_potencia  = models.CharField(_("Motor / Potência"), max_length=50, blank=True)
    combustivel     = models.CharField(_("Combustível"), max_length=10, choices=Combustivel.choices)
    cap_tanque      = models.DecimalField(_("Capacidade do Tanque (L)"), max_digits=6, decimal_places=1)
    consumo_ref     = models.DecimalField(_("Consumo de Referência (km/L)"), max_digits=5, decimal_places=2, null=True, blank=True)
    cap_passageiros = models.PositiveSmallIntegerField(_("Capacidade de Passageiros"), null=True, blank=True)
    cor             = models.CharField(_("Cor"), max_length=40, blank=True)
    transmissao     = models.CharField(_("Transmissão"), max_length=12, choices=Transmissao.choices, blank=True)
    pneu_dim        = models.CharField(_("Dimensão dos Pneus"), max_length=20, blank=True)

    # ── Grupo: Histórico e Estado ─────────────────────────────────────────────

    km_entrada         = models.PositiveIntegerField(_("KM de Entrada"))
    ultimo_km          = models.PositiveIntegerField(_("Último KM"), default=0)
    estado_conservacao = models.CharField(_("Estado de Conservação"), max_length=10, choices=EstadoConservacao.choices)
    status             = models.CharField(_("Status"), max_length=14, choices=Status.choices, default=Status.DISPONIVEL)

    # ── Grupo: Informações Financeiras ────────────────────────────────────────

    valor_fipe       = models.DecimalField(_("Valor FIPE (R$)"), max_digits=12, decimal_places=2, null=True, blank=True)
    tipo_frota       = models.CharField(_("Tipo de Frota"), max_length=10, choices=TipoFrota.choices)
    locadora         = models.CharField(_("Locadora / Proprietário"), max_length=100, blank=True)
    valor_aluguel    = models.DecimalField(_("Valor Aluguel/mês (R$)"), max_digits=10, decimal_places=2, null=True, blank=True)
    dt_ini_contrato  = models.DateField(_("Início do Contrato"), null=True, blank=True)
    dt_fim_contrato  = models.DateField(_("Fim do Contrato"), null=True, blank=True)

    # ── Grupo: Informações Administrativas ───────────────────────────────────

    secretaria   = models.ForeignKey(
        "usuarios.Secretaria",
        on_delete=models.PROTECT,
        verbose_name=_("Secretaria"),
        related_name="veiculos",
    )
    centro_custo = models.CharField(_("Centro de Custo"), max_length=50)

    crlv           = models.FileField(_("CRLV"),           upload_to=_crlv_upload,       null=True, blank=True)
    foto_frente    = models.ImageField(_("Foto — Frente"),  upload_to=_foto_frente_upload, null=True, blank=True)
    foto_lateral_e = models.ImageField(_("Foto — Lat. Esq."), upload_to=_foto_le_upload,  null=True, blank=True)
    foto_lateral_d = models.ImageField(_("Foto — Lat. Dir."), upload_to=_foto_ld_upload,  null=True, blank=True)
    foto_traseira  = models.ImageField(_("Foto — Traseira"), upload_to=_foto_tras_upload, null=True, blank=True)
    foto_hodometro = models.ImageField(_("Foto — Hodômetro"), upload_to=_foto_hod_upload, null=True, blank=True)
    outros_docs    = models.FileField(_("Outros Documentos"), upload_to=_docs_upload,     null=True, blank=True)

    # ── Grupo: Equipamentos ───────────────────────────────────────────────────

    eq_ar_condicionado    = models.BooleanField(_("Ar-condicionado"), default=False)
    eq_direcao_hidraulica = models.BooleanField(_("Direção hidráulica / elétrica"), default=False)
    eq_vidros_eletricos   = models.BooleanField(_("Vidros elétricos"), default=False)
    eq_som_multimidia     = models.BooleanField(_("Som / Multimídia"), default=False)
    eq_radio_comunicador  = models.BooleanField(_("Rádio comunicador"), default=False)
    eq_rodas_liga_leve    = models.BooleanField(_("Rodas de liga leve"), default=False)
    eq_camera_re          = models.BooleanField(_("Câmera de ré"), default=False)
    eq_sensor_estac       = models.BooleanField(_("Sensor de estacionamento"), default=False)
    eq_outros             = models.TextField(_("Outros equipamentos"), blank=True)

    # ── Auditoria ─────────────────────────────────────────────────────────────

    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = _("Veículo")
        verbose_name_plural = _("Veículos")
        ordering            = ["placa"]

    def __str__(self):
        marca  = self.marca.nome  if self.marca  else "—"
        modelo = self.modelo.nome if self.modelo else "—"
        return f"{self.placa} — {marca} {modelo}"

    @property
    def is_locado(self):
        return self.tipo_frota == self.TipoFrota.LOCADO

    @property
    def status_badge_class(self):
        return {
            "DISPONIVEL":    "badge-disponivel",
            "EM_MANUTENCAO": "badge-manutencao",
            "INATIVO":       "badge-inativo",
        }.get(self.status, "badge-inativo")

