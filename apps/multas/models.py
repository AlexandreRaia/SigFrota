from django.db import models
from django.utils.translation import gettext_lazy as _


def _multa_upload(instance, filename):
    return f"multas/{instance.placa}/{filename}"


class TipoMulta(models.Model):
    """Tabela de tipos de infração de trânsito com código DENATRAN."""

    class Natureza(models.TextChoices):
        LEVE       = "LEVE",       _("Leve")
        MEDIA      = "MEDIA",      _("Média")
        GRAVE      = "GRAVE",      _("Grave")
        GRAVISSIMA = "GRAVISSIMA", _("Gravíssima")

    codigo    = models.CharField(_("Código DENATRAN"), max_length=20, unique=True)
    descricao = models.CharField(_("Descrição"), max_length=200)
    natureza  = models.CharField(_("Natureza"), max_length=12, choices=Natureza.choices)
    ativo     = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name         = _("Tipo de Multa")
        verbose_name_plural  = _("Tipos de Multa")
        ordering             = ["codigo"]

    def __str__(self):
        return f"{self.codigo} — {self.descricao}"


class Multa(models.Model):

    class Status(models.TextChoices):
        PENDENTE   = "PENDENTE",   _("Pendente")
        PAGA       = "PAGA",       _("Paga")
        CONTESTADA = "CONTESTADA", _("Contestada")
        VENCIDA    = "VENCIDA",    _("Vencida")

    # Identificação do veículo e condutor
    placa = models.CharField(_("Placa"), max_length=10)
    condutor = models.ForeignKey(
        "condutores.Condutor",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name=_("Condutor"),
        related_name="multas",
    )

    # Dados da infração
    tipo_infracao = models.ForeignKey(
        TipoMulta,
        on_delete=models.PROTECT,
        null=True, blank=True,
        verbose_name=_("Tipo de Infração"),
        related_name="multas",
    )
    pontos = models.PositiveSmallIntegerField(_("Pontos na CNH"), default=0)
    valor  = models.DecimalField(_("Valor (R$)"), max_digits=10, decimal_places=2)
    data_infracao = models.DateField(_("Data da infração"))

    # Situação e prazos
    status          = models.CharField(_("Status"), max_length=12, choices=Status.choices, default=Status.PENDENTE)
    data_vencimento = models.DateField(_("Vencimento pagamento"))
    prazo_indicacao = models.DateField(_("Prazo para indicação do condutor"), null=True, blank=True)
    prazo_defesa    = models.DateField(_("Prazo para defesa prévia"), null=True, blank=True)

    # Documentação
    arquivo    = models.FileField(_("Notificação (PDF)"), upload_to=_multa_upload, null=True, blank=True)
    observacao = models.TextField(_("Observação"), blank=True)

    # Auditoria
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = _("Multa")
        verbose_name_plural = _("Multas")
        ordering            = ["-data_infracao"]

    def __str__(self):
        tipo = self.tipo_infracao.descricao if self.tipo_infracao else "—"
        return f"{self.placa} — {tipo} ({self.data_infracao})"


